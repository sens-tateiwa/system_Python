import numpy as np
import os
import datetime
import time
import winsound
import itertools
import queue
from scipy import integrate

import matplotlib
matplotlib.use('TkAgg')  # または 'Qt5Agg', 'QtAgg' など

import matplotlib.pyplot as plt
from matplotlib import animation

import signalProcessing

from Polytec_Python.acquisition_examples import acquire_streaming
from Polytec_Python.acquisition_examples.acquisition_control import acquireData
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

class UseLDV:
    def __init__(self,cameraGrabingFinish,sample_count, new_bandwidth,new_range,lastdata_queue):
        self.ip_address = "192.168.137.1"

        self.cameraFinishFlag = cameraGrabingFinish

        self.new_bandwidth = new_bandwidth
        self.new_range = new_range

        self.dt = 1/218750
        self.N=sample_count

        self.theta = -10
        self.last_frame= -1

        self.anime = None
        self.velocity = ""
        self.lastdata = lastdata_queue
        self.buffer_list=[]

        self.device_communication = None
        self.data_acquisition = None
        self.block_size = None
        self.limited_active_channels = None
        self.base_samples_chunk_size = None

    def cleanup(self):
        print("終了処理を開始します...")
        
        # 1. まずデータ取得オブジェクトを消す（これで __del__ が走る）
        # 通信(device_communication)はまだ生きているので、エラーにならない
        if self.data_acquisition is not None:
            del self.data_acquisition 
            self.data_acquisition = None

        # 2. その後に通信オブジェクトを消す
        if self.device_communication is not None:
            del self.device_communication
            self.device_communication = None

    def _init_draw(self):
        return self.line,

    def _dataAquisition(self):
        #接続されているデバイスから速度のデータを受け取る
        #
        
        #data_acquisition: 接続されているデバイスの情報
        #N: 計測するサンプル数
        #block_size: daq_config.block_size if is_block_mode else sample_count: 多分streamingモードなのでサンプル数(N)になる
        #limited_active_channels: 元は複数あるチャンネルの内今回用いるvelocity, datavalidityのみの制限されたチャンネルのみからデータを取得
        #base_samples_chunk_size: The amount of base samples to read at once from a device

        #velocity_list = acquire_streaming.run(self.ip_address,self.N)
        velocity_list = acquireData._acquire_data_ver3(self.data_acquisition, self.N, self.block_size,self.limited_active_channels, self.base_samples_chunk_size)
        

        return velocity_list

    def __update(self,frame,t,line):
        #if frame == self.last_frame:
        #    return line,

        #カメラ追従を終了した時、グラフの更新も停止する
        if self.cameraFinishFlag.is_set() == True:
            print("アニメーションの終了")
            try:
                """
                # 現在のデータを取得
                x = line.get_xdata()
                y = line.get_ydata()
                """
                send_data = np.array(self.buffer_list)
                # 古いデータが残っていれば捨てて（念の為）、新しいデータを入れる
                # ※ maxsize=1設定なら、putの前にget_nowaitする
                try:
                    while not self.lastdata.empty():
                        self.lastdata.get_nowait()
                except queue.Empty:
                    pass
                #self.lastdata.put((x,y))#Queueにデータを送信し、メインプロセスでこれを取得する
                self.lastdata.put(send_data)
                print("Queueにデータを送信しました")

            except Exception as e:
                print(f"データ送信エラー：{e}")
            
            self.anime.event_source.stop()#アニメーションの停止
            self.cleanup()
            plt.close(self.fig)#pltの終了、plt.closeでplt.showを終わらせる
            return line,
  
        print(f'frame: {frame}')#現在のフレームを確認

        winsound.Beep(440,250)#400Hzを250ms鳴らす
        winsound.Beep(493,250)
        now_1 = time.perf_counter()
        new_y_data = self._dataAquisition()#LDVからデータ取得
        now_2 = time.perf_counter()
        winsound.Beep(523,250)
        print(f"Time: {now_2 - now_1:.6f}秒")

        line.set_ydata(new_y_data)#lineに取得した変位データをset
        self.buffer_list.append(new_y_data)#バッファに変位データを蓄積（あとでメインプロセスにn計測回分まとめて送信）
        #self.last_frame = frame
        return line,

    def animate(self):
        try:
            changeBandwidthandRange.run(self.ip_address, self.new_bandwidth,self.new_range)
        except:
            print("change bandwidth and range error")
            return
        
        self.device_communication, self.data_acquisition, self.block_size,self.limited_active_channels, self.base_samples_chunk_size = acquire_streaming.connect_device(self.ip_address,self.N)
        
        self.fig= plt.figure()
        plt.xlabel('time [s]')
        plt.ylabel('Velocity [m/s]')
        #plt.ylabel('Displacement [m]')
        plt.xlim(0,self.N*self.dt+0.01)
        #plt.ylim(-0.003,0.003)
        #plt.ylim(-0.0007,0.0007)
        """
        plt.xlim(0,6.3)
        plt.ylim(-1.2,1.2)
        t = np.linspace(0,2*np.pi,100)
        initial_y = np.sin(t*self.theta)
        self.line, = plt.plot(t,initial_y)
        """
        t = np.linspace(0,self.dt*self.N,self.N)
        initial_y = np.sin(t*self.theta)
        self.line, = plt.plot(t,initial_y)
        #plt.plot(t, csv_velocity) # 入力信号
        interval_margin_ms = 1000
        data_time_interval = self.dt
        interval_ms = self.N * self.dt * 1000 + interval_margin_ms
        #interval_ms = 100
        frames = itertools.count(1,1) #フレーム番号を無限に生成itertools.count(start=1, step=1)
        #frames = range(5)               #5回だけ実行、テスト用

        params = {
            'fig':self.fig,                                  #描画する下地
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
        print("DataAquisition process finished")

    


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