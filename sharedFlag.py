import cv2
import winsound
import time

DataAcquiring = False
CameraGrabbing = False

def set_DataAcquiring_flag(bool):
    global DataAcquiring
    if(bool == True):
        DataAcquiring = True
    else:
        DataAcquiring = False
    return

def isDataAcquiring():
    global DataAcquiring
    return DataAcquiring

def set_CameraGrabbing_flag(bool):
    global CameraGrabbing
    if(bool == True):
        CameraGrabbing = True
    else:
        CameraGrabbing = False
    return

def isCameraGrabbing():
    global CameraGrabbing
    return CameraGrabbing

laser_point =(0,0)

def test(event, theta):
    event.clear()
    """
    for i in range(3):
        print(f"theta:{theta}, i:{i}")
        time.sleep(1)
    """
    time.sleep(0.5)
    event.set()



