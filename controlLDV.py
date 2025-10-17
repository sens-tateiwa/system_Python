import numpy as np
import os
import datetime
import time
import winsound
import matplotlib.pyplot as plt
import itertools
from matplotlib import animation

import sharedFlag
import signalProcessing

from Polytec_Python.acquisition_examples import acquire_streaming
from Polytec_Python.acquisition_examples import changeBandwidthandRange



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

