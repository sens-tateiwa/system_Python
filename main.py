import matplotlib
matplotlib.use('TkAgg')
import imageProcessing
import controlCamera
import controlLDV
import sharedFlag
import controlGUI
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
    sample_count=2**15 #2^17 = 131,072
    dt = 1/218750
    new_bandwidth="1 kHz"
    new_range="10 mm/s"
    isPlotMatchpoint=False
    rootDir = 'C:/Users/yuto/Documents/system_python'
    laserImage = 'Image__2025-11-13__16-05-34.png'
    laser_point = imageProcessing.calculateLaserPoint(rootDir+'/'+laserImage)

    startLDV = multiprocessing.Event()           #LDVの計測を開始させるフラグ、カメラ追従が起動したらsetする
    cameraGrabingFinish = multiprocessing.Event()#カメラの連続撮影が終了したかどうかのフラグ

    lastdata_queue = multiprocessing.Queue(maxsize=1)#共有のQueueを作成、できるならshared_memoryの方がよい

    try:
        dataAquisition = controlLDV.DataAquisition(cameraGrabingFinish,sample_count,new_bandwidth,new_range,lastdata_queue)
        dataAquisition_process=multiprocessing.Process(target=dataAquisition.animate, args=())

        buttonWindow = controlGUI.ButtonWindow(cameraGrabingFinish)
        button_process = multiprocessing.Process(target=buttonWindow.run,args=())
        
        controlCamera_process = multiprocessing.Process(target=controlCamera.getCameraImage_endless, args=(startLDV, cameraGrabingFinish, laser_point,timeout_ms,timelimit_s,isPlotMatchpoint))
        controlCamera_process.start()

        startLDV.wait()#カメラが起動するまで待機
        
        dataAquisition_process.start()
        button_process.start()
        #子プロセスの起動
        #process_queue = multiprocessing.Queue()#共有のQueueを作成
        #process = multiprocessing.Process(target=hoge,args=(ho,ge,process_queue))#プロセスの引数に共有のQueueを渡す
        #process.start()
        
        cameraGrabingFinish.wait()
        print("cameraGrabingFinishFlag is set")

        
        acquired_data = lastdata_queue.get()
        num_data_chunk = acquired_data.shape[0]
        num_one_data = acquired_data.shape[1]
        print(f"num_data_chunck = {num_data_chunk}")
        print(f"num_one_data = {num_one_data}")

        #print(x)
        #print(y)

        button_process.terminate()
        button_process.join()
        while controlCamera_process.is_alive():
            print("creating video")
            time.sleep(0.5)
        controlCamera_process.join()

        while dataAquisition_process.is_alive():
            print("creating queue")
            time.sleep(0.5)
        dataAquisition_process.join()#メインプロセスに終わったことを通知する（メインプロセスに合流する）

        rootDir = 'C:/Users/yuto/Documents/system_python/data/LDVdata'
        x = np.linspace(0,dt*sample_count,sample_count)
        chunk=1
        for chunk_data in acquired_data:
            now = datetime.datetime.now()
            name = now.strftime(f"%Y%m%d_%H%M%S_{chunk}")
            file_name = rootDir + '/' + name + '.txt'
            y = chunk_data
            np.savetxt(file_name, y,fmt='%s')
            chunk += 1
        
        fig= plt.figure()
        plt.xlabel('time [s]')
        plt.ylabel('Displacement [m]')
        plt.xlim(0,sample_count*dt+0.01)
        plt.ylim(-0.0007,0.0007)
        plt.plot(x,y)
        plt.show()

        sys.exit(0)
        
    except KeyboardInterrupt:
        
        #すべての子プロセスを強制終了

        dataAquisition_process.terminate()
        dataAquisition_process.join()
        button_process.terminate()
        button_process.join()
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