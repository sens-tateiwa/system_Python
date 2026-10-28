#!/usr/bin/env python3

import time
from xarm.wrapper import XArmAPI
import multiprocessing
import keyboard
import sys

class UseRobotArm:
    def __init__(self,cameraGrabingFinish, isArmMoving,AccelerometerStartAcquiring):
        self.arm = None

        self.x_1 = 70 # mm
        self.x_2 = -130

        
        # 実指を固定し素材をスライドさせる計測方法での位置---
        # x=70 ~ -130 mm, y=-340 mm, z=-500 mm, roll=180, pitch=0, yaw=0
        self.home_pos = (70, -340, -500, 180, 0, 0)
        self.home_pos_down = (70, -340, -500, 180, 0, 0)#上と同じで必要ないが、下の条件でのコードと合わせるために設定
        self.target_pos = (-130, -340, -500, 180, 0, 0)
        # ---実指を固定し素材をスライドさせる計測方法での位置


        # 素材を固定して模型指をロボットに装着しスライドさせる計測方法での位置---
        # x=70 ~ -130 mm, y=-340 mm, z=-500 mm, roll=180, pitch=0, yaw=0
        self.home_pos      = (-86, -350.4, -386, -162.2, 16.7, 76)
        self.home_pos_down = (-86, -350.4, -392, -162.2, 16.7, 76)
        self.target_pos    = (114, -350.4, -392, -162.2, 16.7, 76)
        # ---素材を固定して模型指をロボットに装着しスライドさせる計測方法での位置

        # 素材を固定して模型指をロボットに装着しスライドさせる計測方法(ゴム円柱の指模型を垂直に接触させる時)での位置---
        # x=70 ~ -130 mm, y=-340 mm, z=-500 mm, roll=180, pitch=0, yaw=0
        self.home_pos      = (100, -224, -421, 180, 0, 0)
        self.home_pos_down = (100, -224, -425, 180, 0, 0)
        self.target_pos    = (250, -224, -425, 180, 0, 0)
        # ---素材を固定して模型指をロボットに装着しスライドさせる計測方法での位置

        #テスト用
        #self.home_pos      = (100, -224, -417, 180, 0, 0)
        #self.home_pos_down = (100, -224, -421, 180, 0, 0)
        #self.target_pos    = (250, -224, -421, 180, 0, 0)


        #speed 64で59.3 mm/s, 89で80.4 mm/s, 118で100.2 mm/s, 149で120.4 mm/s
        self.speed = 64

        self.cameraGrabingFinish = cameraGrabingFinish
        self.isArmMoving = isArmMoving
        self.AccelerometerStartAcquiring = AccelerometerStartAcquiring
        if(self.isArmMoving.is_set()):
            self.isArmMoving.clear()
        if(self.AccelerometerStartAcquiring.is_set()):
                    self.AccelerometerStartAcquiring.clear()

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

        #ロボットアームとの接続が確立された時点で、ロボットアームを移動開始位置に移動させ待機
        self.arm.set_position(*self.home_pos, speed=100, wait=True)

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
        
        self.isArmMoving.wait()#controlLDVからロボットを動かす指令が来るまで待機
        
        #speed 64で59.3 mm/s, 89で80.4 mm/s, 118で100.2 mm/s, 149で120.4 mm/s
        self.arm.set_position(*self.home_pos_down, speed=self.speed, wait=True)
        self.AccelerometerStartAcquiring.set()
        t_1 = time.perf_counter()
        self.arm.set_position(*self.target_pos, speed=self.speed, wait=True)
        t_2 = time.perf_counter()
        self.AccelerometerStartAcquiring.clear()
        time.sleep(1)
        
        
        self.arm.set_position(*self.home_pos, speed=100, wait=True)

        self.isArmMoving.clear()

        print(f"{abs(self.home_pos[0]-self.target_pos[0])/(t_2-t_1)} mm/s, {t_2-t_1} s")
        
    def close(self):
        #self.arm.move_gohome(wait=True)
        self.arm.set_position(*self.home_pos, speed=100, wait=True)
        self.arm.disconnect()
    
    def update(self):
        while(not self.cameraGrabingFinish.is_set()):
            self.move()
        self.close()

def run_robot_process(cameraGrabingFinish, isArmMoving,AccelerometerStartAcquiring):
    useRobotArm = UseRobotArm(cameraGrabingFinish, isArmMoving,AccelerometerStartAcquiring)
    useRobotArm.update()


if __name__ == "__main__":
    cameraGrabingFinish = multiprocessing.Event()
    isArmMoving = multiprocessing.Event()
    AccelerometerStartAcquiring = multiprocessing.Event()
    
    useRobotArm_process = multiprocessing.Process(target=run_robot_process, args= (cameraGrabingFinish, isArmMoving,AccelerometerStartAcquiring))
    useRobotArm_process.start()
    print("1:move, 2:stop")
    while(1):
        #print("1: move,  2: stop")
        if keyboard.is_pressed("1"):
            isArmMoving.set()
            time.sleep(0.3)
        elif keyboard.is_pressed("2"):
            cameraGrabingFinish.set()
            print("finish")
            break
        time.sleep(0.01)
        
    useRobotArm_process.terminate()
    useRobotArm_process.join()
    
    sys.exit(0)