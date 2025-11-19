import numpy as np
import os
import datetime
import time
import winsound
import itertools

import matplotlib
matplotlib.use('TkAgg')  # または 'Qt5Agg', 'QtAgg' など

import matplotlib.pyplot as plt
from matplotlib import animation

import sharedFlag
import signalProcessing

from Polytec_Python.acquisition_examples import acquire_streaming
from Polytec_Python.acquisition_examples import changeBandwidthandRange

import multiprocessing




def run(sample_count=2**17, new_bandwidth="1 kHz", new_range="10 mm/s"):
    ip_address = "192.168.137.1"
    rootDir = 'C:/Users/yuto/Documents/system_python/data/LDVdata'
    now = datetime.datetime.now()
    name = now.strftime("%Y%m%d_%H%M%S")
    file_name = rootDir + '/' + name + '.txt'
    try:
        os.makedirs(rootDir)
    except FileExistsError:
        pass
    
    changeBandwidthandRange.run(ip_address, new_bandwidth,new_range)

    velocity = ""
    
    #sample_count = 2**17 # 2^17 = 131,072
    data_time_interval = 1/218750
        
    #sharedFlag.set_DataAcquiring_flag(True)
    winsound.Beep(400,500)#400Hzを500ms
    time.sleep(0.5)

    start = time.time()
    velocity += acquire_streaming.run(ip_address,sample_count)
    end = time.time()

    winsound.Beep(400,500)#400Hzを500ms
    #sharedFlag.set_DataAcquiring_flag(False)
    #print(f"set DataAcquiringFlag:{sharedFlag.isDataAcquiring}")
  
    print(f"acquired time is {end - start}")
    print(f"acquired start time is {start}")
    print(f"acquired end time is {end}")
    print(f"expected time is {data_time_interval*(sample_count-1)}")

    text = velocity.split('\n')
    text = text[0:sample_count]
    #print(text)
    #velocity = [float(x) for x in text[0:sample_count]]

    np.savetxt(file_name, text,fmt='%s')
    
    signalProcessing.fftplt_indiv(file_name, sample_count,data_time_interval)
    signalProcessing.STFT(sample_count,data_time_interval,file_name,2**15)

    return file_name

def _update(frame,sample_count,data_time_interval): 
    ip_address = "192.168.137.1"

    velocity = ""
    velocity += acquire_streaming.run(ip_address,sample_count)

    plt.cla()

    signalProcessing.fftplt_indiv_endless(velocity, sample_count, data_time_interval)

class DataAquisition:
    def __init__(self,cameraGrabingFinish,new_bandwidth,new_range):
        ip_address = "192.168.137.1"

        self.cameraFinishFlag = cameraGrabingFinish
    
        #changeBandwidthandRange.run(ip_address, new_bandwidth,new_range)

        self.dt = 1/218750
        self.N=2**17

        self.theta = -10
        self.last_frame= -1

        self.isnotDataAquiring = multiprocessing.Event()
        self.isnotDataAquiring.set()

        self.anime = None

        #winsound.Beep(400,500)#400Hzを500ms
        #time.sleep(0.5)

    def _init_draw(self):
        return self.line,

    def __update(self,frame,t,line):
        #if frame == self.last_frame:
        #    return line,
        if self.cameraFinishFlag.is_set() == True:
            print("アニメーションの終了")
            self.anime.event_source.stop()
        self.isnotDataAquiring.wait()#データを取得する関数の初めにisnotDataAquiring.clear()で__update()しないように待機させる、データを取得し終わるとisnotDataAquiring.set()で__update()を起動
        self.theta = 1 + frame
        print(f'theta = {self.theta}')
        
        sharedFlag.test(self.isnotDataAquiring,self.theta) 

        new_y_data = np.sin(t * self.theta)
        line.set_ydata(new_y_data)
        self.last_frame = frame
        return line,

    def animate(self):
        fig= plt.figure()
        plt.xlabel('time [s]')
        plt.ylabel('Velocity [m/s]')
        plt.xlim(0,6.3)
        plt.ylim(-1.2,1.2)
        #plt.tick_params(labelsize=45)
        #plt.subplots_adjust(0.2,0.15,0.97,0.95)
        #t = np.linspace(0,self.dt*self.N,self.N)
        t = np.linspace(0,2*np.pi,100)
        initial_y = np.sin(t*self.theta)
        self.line, = plt.plot(t,initial_y)
        #plt.plot(t, csv_velocity) # 入力信号
        interval_margin_ms = 500
        sample_count = self.N
        data_time_interval = self.dt
        #interval_ms = sample_count * data_time_interval * 1000 + interval_margin_ms
        interval_ms = 100
        frames = itertools.count(0,0.1) #フレーム番号を無限に生成
        #frames = range(5)               #5回だけ実行、テスト用

        params = {
            'fig':fig,                                  #描画する下地
            'func':self.__update,                             #グラフを更新する関数
            'fargs':(t, self.line),  #関数の引数
            'interval':interval_ms,                     #更新間隔(ミリ秒)
            'frames':frames,                            #フレーム番号
            'init_func':self._init_draw,
            'blit':True,                               #アニメーション高速化のため推奨
            'repeat':False
        }

        self.anime = animation.FuncAnimation(**params)
        
        plt.show()


#run_endless 動作未確認(_update,fftplt?indiv_endlessも同様に動作未確認)
def run_endless(sample_count=2**15, new_bandwidth="1 kHz", new_range="10 mm/s"):
    ip_address = "192.168.137.1"
    
    changeBandwidthandRange.run(ip_address, new_bandwidth,new_range)

    data_time_interval = 1/218750

    #winsound.Beep(400,500)#400Hzを500ms
    #time.sleep(0.5)

    fig= plt.figure()

    interval_margin_ms = 500
    interval_ms = sample_count * data_time_interval * 1000 + interval_margin_ms
    frames = itertools.count(0,0.1) #フレーム番号を無限に生成
    frames = range(5)               #5回だけ実行、テスト用

    params = {
        'fig':fig,                                  #描画する下地
        'func':_update,                             #グラフを更新する関数
        'fargs':(sample_count,data_time_interval),  #関数の引数
        'interval':interval_ms,                     #更新間隔(ミリ秒)
        'frames':frames,                            #フレーム番号
    }

    anime = animation.FuncAnimation(**params)

    plt.show()
    #plt.close()

if __name__ == "__main__":
    ip_address = "192.168.137.1"
    rootDir = 'C:/Users/yuto/Documents/system_python/data/LDVdata'
    now = datetime.datetime.now()
    name = now.strftime("%Y%m%d_%H%M%S")
    try:
        os.makedirs(rootDir)
    except FileExistsError:
        pass
    
    changeBandwidthandRange.run(ip_address, "100 kHz")
    print("changeBandwidthandRange was Done\n")

    velocity = ""
    
    sample_count = 2**17 # 2^17 = 131,072
    data_time_interval = 1/218750
    
    #start = time.time()
    velocity += acquire_streaming.run(ip_address,sample_count)
    #end = time.time()
    print("acquisition was Done\n")
    #print(f"time is {end - start}")
    print(f"expected time is {data_time_interval*(sample_count-1)}")

    text = velocity.split('\n')
    text = text[0:sample_count]
    #print(text)
    #velocity = [float(x) for x in text[0:sample_count]]

    np.savetxt(rootDir + "/" + name + ".txt", text,fmt='%s')
    print("savetxt was Done\n")
    
    signalProcessing.fftplt_indiv(rootDir+"/"+name + ".txt", sample_count,data_time_interval)

