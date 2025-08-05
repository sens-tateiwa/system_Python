import numpy as np
import os
import datetime
import time
import winsound

import sharedFlag
import signalProcessing

from Polytec_Python.acquisition_examples import acquire_streaming
from Polytec_Python.acquisition_examples import changeBandwidthandRange



def run(sample_count=2**17, new_bandwidth="100 kHz", new_range="10 mm/s"):
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

def run_endless(sample_count=2**17, new_bandwidth="100 kHz", new_range="10 mm/s"):
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

