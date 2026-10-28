import matplotlib
matplotlib.use('TkAgg')
import imageProcessing
import controlCamera
import controlLDV
import sharedFlag
import controlGUI
import signalProcessing
import controlMirror
import controlRobotArm
import controlArduino

import sys
import datetime
import numpy as np
from scipy import integrate

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

def run_endless(withRobot):
    timeout_ms = 5
    timelimit_s = 50
    sample_count=2**17 #2^17 = 131,072
    dt = 1/218750
    new_bandwidth="100 kHz" #[bandwidth_selection] Available items: 100 kHz, 50 kHz, 25 kHz, 10 kHz, 5 kHz, 1 kHz
    new_range="200 mm/s"    #[range_selection]     Available items: 2 m/s, 1 m/s, 500mm/s, 200 mm/s, 100 mm/s, 50 mm/s, 20 mm/s, 10 mm/s
    isPlotMatchpoint=False
    rootDir = 'C:/Users/yuto/Documents/system_python'
    laserImage = 'Image__2026-09-28__17-29-56.png'
    laser_point = imageProcessing.calculateLaserPoint(rootDir+'/'+laserImage)


    startLDV = multiprocessing.Event()           #LDVの計測を開始させるフラグ、カメラ追従が起動したらsetする
    cameraGrabingFinish = multiprocessing.Event()#カメラの連続撮影が終了したかどうかのフラグ
    prepareMirror = multiprocessing.Event()      #ミラーが追従開始位置にセットされたかどうかのフラグ
    isArmMoving = multiprocessing.Event()        #ロボットアームが動いている間はsetするフラグ、ロボットが動いていない時はclearする
    AccelerometerStartAcquiring = multiprocessing.Event() #加速度センサの計測を行うフラグ、ロボットアームの動きと同期させるためのもの


    prepareLaserPosition = multiprocessing.Queue(maxsize=1)#開始前にGUIで設定したミラーの角度（レーザの位置）を共有するためのqueue

    MirrorAngle_queue = multiprocessing.Queue(maxsize=1)
    lastdata_queue = multiprocessing.Queue(maxsize=1)#共有のQueueを作成、できるならshared_memoryの方がよい
    AccelerometerData_queue = multiprocessing.Queue(maxsize=1)#加速度センサで取得したデータを共有するためのQueue

    try:
        dataAquisition = controlLDV.UseLDV(cameraGrabingFinish,sample_count,new_bandwidth,new_range,lastdata_queue,isArmMoving,withRobot)
        dataAquisition_process=multiprocessing.Process(target=dataAquisition.animate, args=())

        buttonWindow = controlGUI.ButtonWindow(MirrorAngle_queue,prepareLaserPosition,cameraGrabingFinish)
        button_process = multiprocessing.Process(target=buttonWindow.run,args=())
        
        controlMirror_process = multiprocessing.Process(target=controlMirror.mirror_server,args=(MirrorAngle_queue, prepareMirror))

        controlCamera_process = multiprocessing.Process(target=controlCamera.getCameraImage_endless, args=(MirrorAngle_queue,prepareLaserPosition,startLDV, cameraGrabingFinish, laser_point,timeout_ms,timelimit_s,isPlotMatchpoint))

        if withRobot:
            useRobotArm_process = multiprocessing.Process(target=controlRobotArm.run_robot_process, args= (cameraGrabingFinish, isArmMoving,AccelerometerStartAcquiring))
            useRobotArm_process.start()
            controlArduino_process = multiprocessing.Process(target=controlArduino.run,args=(AccelerometerStartAcquiring,cameraGrabingFinish,AccelerometerData_queue))
            controlArduino_process.start()
        
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
        # 計測開始前に終了するなどのデータがないことを想定した機能が必要であるが未実装
        acquired_data = lastdata_queue.get()#データを受け取るまで次の行に進まない
        num_data_chunk = acquired_data.shape[0]
        num_one_data = acquired_data.shape[1]
        print(f"num_data_chunck = {num_data_chunk}")
        print(f"num_one_data = {num_one_data}")

        if withRobot:
            acquired_Accelerometer_data = AccelerometerData_queue.get()#データを受け取るまで次の行に進まない
            print("Accelerometer data got")
            num_Accelerometer_data_chunk = len(acquired_Accelerometer_data)
            if num_Accelerometer_data_chunk > 0:
                num_Accelerometer_one_data = acquired_Accelerometer_data[0].shape[0]
            else:
                num_Accelerometer_one_data = 0
            print(f"num_Accelerometer_data_chunck = {num_Accelerometer_data_chunk}")
            print(f"num_Accelerometer_one_data = {num_Accelerometer_one_data}")

        #print(x)
        #print(y)

        button_process.terminate()
        button_process.join()
        controlMirror_process.terminate()
        controlMirror_process.join()

        if withRobot:
            useRobotArm_process.terminate()
            useRobotArm_process.join()

        while controlCamera_process.is_alive():
            print("creating video")
            time.sleep(1)
        controlCamera_process.join()

        while dataAquisition_process.is_alive():
            print("creating queue")
            time.sleep(1)
        dataAquisition_process.join()#メインプロセスに終わったことを通知する（メインプロセスに合流する）

        if withRobot:
            while controlArduino_process.is_alive():
                print("creating Accelerometer_queue")
                time.sleep(1)
            controlArduino_process.join()
        
        rootDir = 'C:/Users/yuto/Documents/system_python/data/LDVdata'
        now = datetime.datetime.now()
        name = now.strftime("%Y%m%d_%H%M")
        x = np.linspace(0,dt*sample_count,sample_count)
        chunk=1
        for chunk_data in acquired_data:
            file_name = rootDir + '/' + name + f'_{chunk}'
            file_name_velocity = rootDir + '/' + name + '_velocity' +f'_{chunk}'
            y = chunk_data
            displacement_list = integrate.cumulative_trapezoid(y, dx=dt,initial=0 )
            np.savetxt(file_name+'.txt', displacement_list,fmt='%s')
            np.savetxt(file_name_velocity+'.txt',y,fmt='%s')
            fig= plt.figure()
            plt.xlabel('time [s]')
            #plt.ylabel('Displacement [m]')
            plt.ylabel('Velocity [m/s]')
            plt.xlim(0,sample_count*dt+0.01)
            #plt.ylim(-0.0007,0.0007)
            plt.ylim(-0.1,0.1)
            #plt.tight_layout()
            plt.plot(x,y)
            plt.tight_layout()
            plt.savefig(file_name+'.png')#フィルタリング処理をしていないvelocity
            window_length = 2**15
            signalProcessing.STFT(sample_count, dt, file_name, 2**14)
            signalProcessing.fftplt_indiv(file_name, sample_count, dt)
            signalProcessing.compute_welch_psd_and_plot(file_name, 1/dt, window_length, overlap_samples=None)
            #signalProcessing.velocity_average(file_name_velocity, sample_count, dt)
            chunk += 1

        if withRobot:
            rootDir_Accelerometer = 'C:/Users/yuto/Documents/system_python/data/AccelerometerData'
            chunk_Accelerometer=1
            for chunk_Accelerometer_data in acquired_Accelerometer_data:
                file_name_acceleration = rootDir_Accelerometer + '/' + name + '_acceleration' + f'_{chunk_Accelerometer}'
                file_name_velocity = rootDir_Accelerometer + '/' + name + '_velocity' +f'_{chunk_Accelerometer}'
                #y = chunk_Accelerometer_data
                Accelerometer_data = np.asarray(chunk_Accelerometer_data,dtype=np.float64)
                t_Accelerometer = Accelerometer_data[:,0]
                axyz_Accelerometer = Accelerometer_data[:,1:4]
                diff_t = np.diff(t_Accelerometer)
                mean_dt_Accelerometer = float(np.mean(diff_t))
                print(f'mean_dt_Accelerometer = {mean_dt_Accelerometer} s')
                print(f'sampling rate of Accelerometer = {1/mean_dt_Accelerometer} Hz' )

                dt_intervals = diff_t[:,np.newaxis]
                trapezoids = 0.5*(axyz_Accelerometer[:-1,:]+axyz_Accelerometer[1:,:])*dt_intervals
                initial_zeros = np.zeros((1,3))
                velocity = np.vstack([initial_zeros,np.cumsum(trapezoids,axis=0)])
                velocity_data = np.hstack([t_Accelerometer[:,np.newaxis],velocity])

                np.savetxt(file_name_acceleration+'.txt', Accelerometer_data,fmt='%s')
                np.savetxt(file_name_velocity+'.txt',velocity_data,fmt='%s')
                chunk_Accelerometer += 1
        
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
        if withRobot:
            controlArduino_process.terminate()
            controlArduino_process.join()
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

    withRobot = True
    withRobot = False
    run_endless(withRobot)