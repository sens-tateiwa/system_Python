#!/usr/bin/env python3

import time
from xarm.wrapper import XArmAPI
import multiprocessing

class UseRobotArm:
    def __init__(self,cameraGrabingFinish, isArmMoving):
        self.arm = None

        self.x_1 = 170
        self.x_2 = -30

        self.cameraGrabingFinish = cameraGrabingFinish
        self.isArmMoving = isArmMoving

    def hangle_err_warn_changed(self,item):
        print('ErrorCode: {}, WarnCode: {}'.format(item['error_code'], item['warn_code']))
        # TODO：Do different processing according to the error code

    def connect(self):
        self.arm = XArmAPI('192.168.1.214')
        self.arm.register_error_warn_changed_callback(self.hangle_err_warn_changed)
        time.sleep(0.5)

        #clean error and warn
        if self.arm.warn_code != 0:
            self.arm.clean_warn()
        if self.arm.error_code != 0:
            self.arm.clean_error()

        #Enable the robot
        self.arm.motion_enable(enable=True)
         #set mode and state
        self.arm.set_mode(0)
        self.arm.set_state(0)

        self.arm.set_position(x=self.x_1, y=-340, z=-500, roll=180, pitch=0, yaw=0, speed=100, wait=True)

    def move(self):
        if not self.arm: self.connect()
        #clean error and warn
        if self.arm.warn_code != 0:
            self.arm.clean_warn()
        if self.arm.error_code != 0:
            self.arm.clean_error()

        #Enable the robot
        self.arm.motion_enable(enable=True)

        #set mode and state
        self.arm.set_mode(0)
        self.arm.set_state(0)
        
        
        #arm.set_position(x=300, y=0, z=200, roll=180, pitch=0, yaw=0, speed=100, wait=True)
        
        self.isArmMoving.wait()#controlLDVからロボットを動かす指令が来るまで待機

        t_1 = time.time()
        self.arm.set_position(x=self.x_2, y=-340, z=-500, roll=180, pitch=0, yaw=0, speed=85, wait=True)
        t_2 = time.time()

        self.arm.set_position(x=self.x_1, y=-340, z=-500, roll=180, pitch=0, yaw=0, speed=100, wait=True)

        self.isArmMoving.clear()

        print(f"{(self.x_1-self.x_2)/(t_2-t_1)} mm/s")
    
    def close(self):
        self.arm.move_gohome(wait=True)
        self.arm.disconnect()
    
    def update(self):
        while(not self.cameraGrabingFinish.is_set()):
            self.move()
        self.close()

def run_robot_process(cameraGrabingFinish, isArmMoving):
    useRobotArm = UseRobotArm(cameraGrabingFinish, isArmMoving)
    useRobotArm.update()


if __name__ == "__main__":
    cameraGrabingFinish = multiprocessing.Event()
    isArmMoving = multiprocessing.Event()

    xarm = UseRobotArm(cameraGrabingFinish, isArmMoving)
    xarm.move()
    xarm.close()
