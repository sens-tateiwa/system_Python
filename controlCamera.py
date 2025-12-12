from pypylon import pylon

import datetime
import time
import glob

import math
count =0

import os
import multiprocessing
#import threading

import cv2

import imageProcessing
import controlMirror
import sharedFlag

#videoDirで指定した動画を分割しrootDirに複数枚の画像として保存する
def divisionVideo2Image(timeout_ms,timelimit_s,videoDir,rootDir):
    #ビデオの読み込み
    cap = cv2.VideoCapture(videoDir)
    if not cap.isOpened():
        print("video can't open")
        return
    os.makedirs(os.path.dirname(rootDir),exist_ok=True)        #分割するビデオの保存ディレクトリの作成
    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))   #画像名をゼロパディングするように総フレーム数の桁数を取得

    fps = cap.get(cv2.CAP_PROP_FPS)
    start_frame = 0
    step_frame = 1
    stop_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print("fps = "+str(fps))
    print("step_frame = "+str(step_frame))
    print("stop_frame = "+str(stop_frame))

    #0フレームから1フレームステップで全フレーム分の画像を保存
    for n in range(start_frame,stop_frame,step_frame):
        cap.set(cv2.CAP_PROP_POS_FRAMES,n)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('{}_{}.{}'.format(rootDir+'/image', str(n).zfill(digit), 'png'), frame)
        else:
            break
    return fps

#画像のリストimage_list内の画像をtimeout_ms間隔で繋ぎ合わせ動画を作成する
def createVideo(image_list,fps,videoName):#fpsはフレームレート
    if len(image_list[0].shape) ==2:
        height, width = image_list[0].shape
        isConvert2Color = True
    else:
        height, width, _ = image_list[0].shape
        isConvert2Color = False

    size = (width, height)
    name = videoName+'.mp4'

    out = cv2.VideoWriter('C:/Users/yuto/Documents/system_python/data/'+name, cv2.VideoWriter_fourcc(*'mp4v'), fps, size,isColor=True)

    for image in image_list:
        if isConvert2Color:
            image = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
        out.write(image)
    out.release()
    return

#Baslerのカメラからtimelimit_s間timeout_ms間隔で画像を取得し続ける
def getCameraImage(event, laser_point, timeout_ms,timelimit_s=10,isPlotMatchpoint=False):

    # トランスポートレイヤーインスタンスを取得
    tl_factory = pylon.TlFactory.GetInstance()

    # InstantCameraオブジェクトの作成
    camera = pylon.InstantCamera()

    # 最初に見つかったデバイスをアタッチ
    camera.Attach(tl_factory.CreateFirstDevice())

    # カメラを開く
    camera.Open()

    # 露光時間を設定（単位はマイクロ秒）
    exposuretime_ms = 1.5
    camera.ExposureTime.SetValue(exposuretime_ms*1000)

    #camera.Gain.SetValue(10.0)
    camera.Gain.SetValue(18.0)

    image_list = []

    X=0
    Y=0
    intervalX = 0.01/126
    intervalY = 0.01/126
    mre2 = controlMirror.setMirror()
    controlMirror.changeAngle(X,Y,mre2)

    now = datetime.datetime.now()
    videoname = now.strftime("%Y%m%d_%H%M%S")

    radius = 120    
    image_template = imageProcessing.createTemplateCircleImage(radius)

    #撮影を開始---
    event.set()
    #sharedFlag.set_CameraGrabbing_flag(True)
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    t1 = time.time()
    while camera.IsGrabbing():                                                                 #カメラの起動
        grab = camera.RetrieveResult(timeout_ms, pylon.TimeoutHandling_ThrowException) #timeout_msミリ秒のタイムアウト #起動しているカメラから画像を撮影
        if grab and grab.GrabSucceeded():
            image = grab.GetArray()     #撮影した画像を配列に格納
            
            #print(timelimit_s -(time.time()-t1))

            #取得した画像の処理を実行
            image = imageProcessing.changeScale(image)
            image,distance = imageProcessing.calculateCentor2FingerDistance(image,  image_template, laser_point, isPlotMatchpoint)

            image_list.append(image)
            
            #X += distance[0]*intervalX/10*7
            #Y -= distance[1]*intervalY/10*7

            #X += distance[0]*intervalX/10*5
            #Y -= distance[1]*intervalY/10*5

            X -= distance[0]*intervalX/10*5
            Y -= distance[1]*intervalY/10*5

            """
            #ラグ確認用、円起動
            global count
            X = 0.1*math.cos(count/100*math.pi)
            Y = 0.1*math.sin(count/100*math.pi)
            count +=1
            """
            
            
            
            
            controlMirror.changeAngle(X,Y,mre2)

            grab.Release()
        t2 = time.time()
        #print(f"isDataAcquiringFlag:{sharedFlag.isDataAcquiring}")
        #cv2.imwrite('C:/Users/yuto/Documents/system_python/data/'+str(datetime.datetime.now())+'.png', img)    #取得した配列を名前を付けてコンピュータに保存
        if((not sharedFlag.isDataAcquiring)or((t2-t1)>timelimit_s)):#timelimit秒後
            camera.StopGrabbing()
            print("camera stop grabbing")
        #sharedFlag.set_CameraGrabbing_flag(True)
        
    #sharedFlag.set_CameraGrabbing_flag(False)    
    #---撮影の終了
    print(f"cameragrab start time is {t1}")
    print(f"cameragrab end time is {t2}")
    controlMirror.changeAngle(0,0,mre2)
    alpha_ms = 0.4  #pylon Viewerから推定した読み取り時間＋その他の内部処理時間
    fps = int(min(525, 1000/(exposuretime_ms+alpha_ms)))
    fps = int(len(image_list)/(t2-t1))
    #fps = int(fps/10)
    print("start creating video")
    createVideo(image_list,fps,videoname)
    print("created video")
    print("videoname : "+videoname)

    #カメラにおける全ての処理が終了したのでカメラを閉じる
    camera.Close()
    cv2.destroyAllWindows()
    return


def getCameraImage_endless(startLDVFlag,cameraGrabingFinish, laser_point, timeout_ms,timelimit_s=30,isPlotMatchpoint=False):
    # トランスポートレイヤーインスタンスを取得
    tl_factory = pylon.TlFactory.GetInstance()

    # InstantCameraオブジェクトの作成
    camera = pylon.InstantCamera()

    # 最初に見つかったデバイスをアタッチ
    camera.Attach(tl_factory.CreateFirstDevice())

    # カメラを開く
    camera.Open()

    # 露光時間を設定（単位はマイクロ秒）
    exposuretime_ms = 1.5
    camera.ExposureTime.SetValue(exposuretime_ms*1000)

    camera.Gain.SetValue(18.0)

    image_list = []

    X=0
    Y=0
    intervalX = 0.01/126
    intervalY = 0.01/126
    mre2 = controlMirror.setMirror()
    controlMirror.changeAngle(X,Y,mre2)

    now = datetime.datetime.now()
    videoname = now.strftime("%Y%m%d_%H%M%S")

    radius = 120    
    image_template = imageProcessing.createTemplateCircleImage(radius)


    #撮影を開始---
    startLDVFlag.set()
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    t1 = time.time()
    while (not cameraGrabingFinish.is_set()):                                                  #カメラの起動
        grab = camera.RetrieveResult(timeout_ms, pylon.TimeoutHandling_ThrowException) #timeout_msミリ秒のタイムアウト #起動しているカメラから画像を撮影
        if grab and grab.GrabSucceeded():
            image = grab.GetArray()     #撮影した画像を配列に格納
            

            #取得した画像の処理を実行
            image = imageProcessing.changeScale(image)
            image,distance = imageProcessing.calculateCentor2FingerDistance(image,  image_template, laser_point, isPlotMatchpoint)

            image_list.append(image)
            
            
            """
            #ラグ確認用、円起動
            global count
            X = 0.1*math.cos(count/100*math.pi)
            Y = 0.1*math.sin(count/100*math.pi)
            count +=1
            """
            X -= distance[0]*intervalX/10*5
            Y -= distance[1]*intervalY/10*5
            
            controlMirror.changeAngle(X,Y,mre2)

            grab.Release()
        t2 = time.time()

        #cv2.imwrite('C:/Users/yuto/Documents/system_python/data/'+str(datetime.datetime.now())+'.png', img)    #取得した配列を名前を付けてコンピュータに保存
        if((t2-t1)>timelimit_s):#timelimit秒後
            camera.StopGrabbing()
            cameraGrabingFinish.set()
            print("camera stop grabbing")

    #---撮影の終了
    #print(f"cameragrab start time is {t1}")
    #print(f"cameragrab end time is {t2}")
    print(f"camera grabing time: {t2-t1}[s]")
    controlMirror.changeAngle(0,0,mre2)
    alpha_ms = 0.4  #pylon Viewerから推定した読み取り時間＋その他の内部処理時間
    fps = int(min(525, 1000/(exposuretime_ms+alpha_ms)))
    fps = int(len(image_list)/(t2-t1))
    #fps = int(fps/10)
    print("create video")
    createVideo(image_list,fps,videoname)
    print("created video")
    print("videoname is "+videoname)

    #カメラにおける全ての処理が終了したのでカメラを閉じる
    camera.Close()
    cv2.destroyAllWindows()
    return

#取得した録画を画像に分割し、fpsやマッチングの特徴点を描画するか否かを変更して再度動画にまとめる
#分割した画像も保存する
if __name__ == "__main__":
    timeout_ms = 5
    timelimit_s = 10
    #getCameraImage(timelimit_s,timeout_ms)
    videoname = "20251208_180346"
    videoDir = 'C:/Users/yuto/Documents/system_python/data/'+videoname+'.mp4'
    rootDir = 'C:/Users/yuto/Documents/system_python/data/'+videoname+'_list'
    try:
        os.makedirs(rootDir)
    except FileExistsError:
        pass

    
    laserImage = 'Image__2025-11-13__16-05-34.png'

    laser_point = imageProcessing.calculateLaserPoint('C:/Users/yuto/Documents/system_python/'+laserImage)

    fps = divisionVideo2Image(timeout_ms,timelimit_s,videoDir,rootDir)
    print(f"fps is {fps}")
    image_list = []
    result_videoName = videoname+'_slow'
    
    radius = 120    
    image_template = imageProcessing.createTemplateCircleImage(radius)

    files = glob.glob(rootDir+"/*.png")
    for file in files:
        image = cv2.imread(file, cv2.IMREAD_COLOR)
        #image = imageProcessing.changeScale(image)
        image,_ = imageProcessing.calculateCentor2FingerDistance(image,image_template,laser_point,isPlotMatchpoint=True)
        image_list.append(image)

    createVideo(image_list,fps,result_videoName)
