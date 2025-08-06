import imageProcessing
import controlCamera
import controlLDV
import sharedFlag

#import threading
import multiprocessing

event = multiprocessing.Event()
#event = threading.Event()

def event_controlLDV(event, sample_count, new_bandwidth, new_range):
    event.wait()
    controlLDV.run(sample_count, new_bandwidth, new_range)

if __name__ == "__main__":
    #print("Hello world")
    timeout_ms = 5
    timelimit_s = 10
    sample_count=2**18 #2^17 = 131,072
    new_bandwidth="1 kHz"
    new_range="10 mm/s"
    isPlotMatchpoint=False
    rootDir = 'C:/Users/yuto/Documents/system_python'
    laserImage = 'Image__2025-07-14__13-03-18.png'

    laser_point = imageProcessing.calculateLaserPoint(rootDir+'/'+laserImage)
    input('start')
    
    controlCameraProcess = multiprocessing.Process(target=controlCamera.getCameraImage, args=(event,laser_point,timeout_ms,timelimit_s,isPlotMatchpoint))
    event_controlLDVProcess = multiprocessing.Process(target=event_controlLDV, args=(event, sample_count, new_bandwidth, new_range))
    sharedFlag.set_DataAcquiring_flag(True)   #これがTureであればCamera追従が機能する、Falseで止まる
    #print(f"set DataAcquiringFlag:{sharedFlag.isDataAcquiring}")
    sharedFlag.set_CameraGrabbing_flag(False) #camera追従が機能している間True、二種のフラグはcamera追従してからデータ取得を行うための処理

    controlCameraProcess.start()
    event_controlLDVProcess.start()
    
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
