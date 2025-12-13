import matplotlib
matplotlib.use('TkAgg')
import imageProcessing
import controlCamera
import controlLDV
import sharedFlag
import controlGUI
import signalProcessing
import controlMirror
import sys
import datetime
import numpy as np

import matplotlib.pyplot as plt


import time

#import threading
import multiprocessing

event = multiprocessing.Event()
#event = threading.Event()

def event_controlLDV(event, sample_count, new_bandwidth, new_range):
    event.wait()
    controlLDV.run(sample_count, new_bandwidth, new_range)

def run():
    timeout_ms = 5
    timelimit_s = 10
    sample_count=2**18 #2^17 = 131,072
    new_bandwidth="1 kHz"
    new_range="10 mm/s"
    isPlotMatchpoint=False
    rootDir = 'C:/Users/yuto/Documents/system_python'
    laserImage = 'Image__2025-11-13__16-05-34.png'

    laser_point = imageProcessing.calculateLaserPoint(rootDir+'/'+laserImage)

    input('start')
    
    controlCameraProcess = multiprocessing.Process(target=controlCamera.getCameraImage, args=(event,laser_point,timeout_ms,timelimit_s,isPlotMatchpoint))
    event_controlLDVProcess = multiprocessing.Process(target=event_controlLDV, args=(event, sample_count, new_bandwidth, new_range))
    sharedFlag.set_DataAcquiring_flag(True)   #これがTrueであればCamera追従が機能する、Falseで止まる
    #print(f"set DataAcquiringFlag:{sharedFlag.isDataAcquiring}")
    sharedFlag.set_CameraGrabbing_flag(False) #camera追従が機能している間True、二種のフラグはcamera追従してからデータ取得を行うための処理

    controlCameraProcess.start()
    event_controlLDVProcess.start()

    controlCameraProcess.join()
    event_controlLDVProcess.join()
    
    """
    controlCameraThread = threading.Thread(target=controlCamera.getCameraImage, args=(event ,timeout_ms,timelimit_s,isPlotMatchpoint))
    event_controlLDVThread = threading.Thread(target=event_controlLDV, args=(event, sample_count, new_bandwidth, new_range))
    sharedFlag.set_DataAcquiring_flag(True)   #これがTureであればCamera追従が機能する、Falseで止まる
    sharedFlag.set_CameraGrabbing_flag(False) #camera追従が機能している間True、二種のフラグはcamera追従してからデータ取得を行うための処理

    controlCameraThread.start()
    #controlLDVThread = threading.Thread(target=controlLDV.run, args=(sample_count, new_bandwidth, new_range))
    #controlLDVThread.start()
    event_controlLDVThread.start()
    """

def event_controlLDV_endless(event, sample_count, new_bandwidth, new_range):
    event.wait()
    controlLDV.run_endless(sample_count, new_bandwidth, new_range)

#動作未確認
def run_endless():
    timeout_ms = 5
    timelimit_s = 30
    sample_count=2**17 #2^17 = 131,072
    dt = 1/218750
    new_bandwidth="1 kHz"
    new_range="10 mm/s"
    isPlotMatchpoint=False
    rootDir = 'C:/Users/yuto/Documents/system_python'
    laserImage = 'Image__2025-12-13__16-23-45.png'
    laser_point = imageProcessing.calculateLaserPoint(rootDir+'/'+laserImage)


    startLDV = multiprocessing.Event()           #LDVの計測を開始させるフラグ、カメラ追従が起動したらsetする
    cameraGrabingFinish = multiprocessing.Event()#カメラの連続撮影が終了したかどうかのフラグ
    prepareMirror = multiprocessing.Event()      #ミラーが追従開始位置にセットされたかどうかのフラグ

    prepareLaserPosition = multiprocessing.Queue(maxsize=1)#開始前にGUIで設定したミラーの角度（レーザの位置）を共有するためのqueue

    MirrorAngle_queue = multiprocessing.Queue(maxsize=1)
    lastdata_queue = multiprocessing.Queue(maxsize=1)#共有のQueueを作成、できるならshared_memoryの方がよい

    try:
        dataAquisition = controlLDV.DataAquisition(cameraGrabingFinish,sample_count,new_bandwidth,new_range,lastdata_queue)
        dataAquisition_process=multiprocessing.Process(target=dataAquisition.animate, args=())

        
        buttonWindow = controlGUI.ButtonWindow(MirrorAngle_queue,prepareLaserPosition,cameraGrabingFinish)
        button_process = multiprocessing.Process(target=buttonWindow.run,args=())
        
        controlMirror_process = multiprocessing.Process(target=controlMirror.mirror_server,args=(MirrorAngle_queue, prepareMirror))

        controlCamera_process = multiprocessing.Process(target=controlCamera.getCameraImage_endless, args=(MirrorAngle_queue,prepareLaserPosition,startLDV, cameraGrabingFinish, laser_point,timeout_ms,timelimit_s,isPlotMatchpoint))
        
        #buttonの子プロセスでミラーの初期位置を設定しようとしていたが、
        # 2つの子プロセスで同時にミラー（ハードウェア）に接続しようとするとエラーが発生し、片方を初期設定後に切断できなかったため、
        # メインプロセスから2つのプロセス（カメラとGUI）を実行するのではなく、GUIを子プロセスではなく、カメラプロセス内でimportして
        # カメラプロセス（頻繁に高速でミラー制御を行う方のプロセス）内でGUI（ボタン）を表示するclassを実行するように変更した
        controlMirror_process.start()
        prepareMirror.wait()#ミラーの接続が確立されるまで待機

        button_process.start()
        
        controlCamera_process.start()

        #現状：計測を開始する合図はカメラが起動する直前である。カメラ起動前にGUIが表示される
        #GUIによってカメラ起動（計測開始:startLDV.set()）する前に「終了」すると、
        # この下の「startLDV.wait()」は永遠にset()されないEventを待機し続けるため、終了操作を行えない

        startLDV.wait()#カメラが起動するまで待機
        
        dataAquisition_process.start()
        
        cameraGrabingFinish.wait()
        print("cameraGrabingFinishFlag is set")

        #下のQueueを受け取る部分もデータがあること前提であるため、
        # 計測開始前に終了するなどのデータがないことを想定した動作が必要
        acquired_data = lastdata_queue.get()
        num_data_chunk = acquired_data.shape[0]
        num_one_data = acquired_data.shape[1]
        print(f"num_data_chunck = {num_data_chunk}")
        print(f"num_one_data = {num_one_data}")

        #print(x)
        #print(y)

        button_process.terminate()
        button_process.join()
        controlMirror_process.terminate()
        controlMirror_process.join()
        while controlCamera_process.is_alive():
            print("creating video")
            time.sleep(0.5)
        controlCamera_process.join()

        while dataAquisition_process.is_alive():
            print("creating queue")
            time.sleep(0.5)
        dataAquisition_process.join()#メインプロセスに終わったことを通知する（メインプロセスに合流する）

        rootDir = 'C:/Users/yuto/Documents/system_python/data/LDVdata'
        now = datetime.datetime.now()
        name = now.strftime("%Y%m%d_%H%M")
        x = np.linspace(0,dt*sample_count,sample_count)
        chunk=1
        for chunk_data in acquired_data:
            file_name = rootDir + '/' + name + f'_{chunk}'
            y = chunk_data
            np.savetxt(file_name+'.txt', y,fmt='%s')
            fig= plt.figure()
            plt.xlabel('time [s]')
            plt.ylabel('Displacement [m]')
            plt.xlim(0,sample_count*dt+0.01)
            plt.ylim(-0.0007,0.0007)
            plt.plot(x,y)
            plt.savefig(file_name+'.png')
            signalProcessing.STFT(sample_count, dt, file_name, 2**15)
            signalProcessing.fftplt_indiv(file_name, sample_count, dt)
            chunk += 1
        
        """
        fig= plt.figure()
        plt.xlabel('time [s]')
        plt.ylabel('Displacement [m]')
        plt.xlim(0,sample_count*dt+0.01)
        plt.ylim(-0.0007,0.0007)
        plt.plot(x,y)
        plt.show()
        """
        sys.exit(0)
        
    except KeyboardInterrupt:
        
        #すべての子プロセスを強制終了

        dataAquisition_process.terminate()
        dataAquisition_process.join()
        #button_process.terminate()
        #button_process.join()
        sys.exit(0)

        #process_queueから最新のデータを取り出す処理（またはいくつかのデータを順に取り出してappendでlistにまとめる処理）をここにかく
    except Exception as e:
        if dataAquisition_process and dataAquisition_process.is_alive():
            dataAquisition_process.terminate()
            dataAquisition_process.join()

if __name__ == "__main__":
    #print("Hello world")
    #run()
    run_endless()