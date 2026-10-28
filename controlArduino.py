import serial
import time
from collections import deque
import numpy as np
import queue
import multiprocessing
import struct
import keyboard
import sys
import datetime


PORT = "COM5"       # ポート番号
BAUDRATE = 500000
WINDOW_SIZE = 200
SCALE_FACTOR = 0.0039
TIMEOUT = 1

PACKET_SIZE = 9
HEADER = b'\xaa\x55'


def run(AccelerometerStartAcquiring,cameraGrabingFinish,AccelerometerData_queue):
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT)
        print(f"Connected to {PORT} at {BAUDRATE} bps")
        
        time.sleep(2)
        ser.reset_input_buffer()
        print("Starting measurement... (Press Ctrl+C to stop)\n")

        timestamps = deque(maxlen=WINDOW_SIZE)
        last_print_time = time.time()
        last_data = None
        fps = 0.0
        buffer = bytearray()

        data_Accelerometer = []
        data_Accelerometer_list = []
        prev_flag = False
        flag = False

        initial_time = 0

        while_flag = True

        while while_flag:
            if ser.in_waiting > 0:
                #line = ser.readline().decode("utf-8", errors="ignore").strip()
                buffer.extend(ser.read(ser.in_waiting))
                current_time = time.time()


                # バッファ内に1パケット分以上のデータがある間ループ
                while len(buffer) >= PACKET_SIZE:
                    # ヘッダ探索
                    if buffer[0] == 0xAA and buffer[1] == 0x55:
                        # 終端フッタの確認
                        if buffer[8] == 0x0A:
                            current_time = time.time()
                            
                            # ペイロード（int16 × 3）を展開: リトルエンディアン '<hhh'
                            raw_x, raw_y, raw_z = struct.unpack('<hhh', buffer[2:8])
                            
                            ax = raw_x * SCALE_FACTOR
                            ay = raw_y * SCALE_FACTOR
                            az = raw_z * SCALE_FACTOR

                            timestamps.append(current_time)

                            #加速度センサの計測開始のフラグがセットされている場合の処理（ロボットアームの稼働と同タイミングのため同じフラグで代用）
                            #加速度センサから送られてきたデータを、フラグがセットされている間だけリストに追加する,フラグがセットされていない時はリストを空に保つ
                            flag = AccelerometerStartAcquiring.is_set()
                            if not prev_flag and flag:
                                #print("立ち上がり検出")
                                initial_time = current_time
                                time_stamp = 0
                                data = [0,ax,ay,az] #(ax,ay,az)→(time,ax,ay,az)に変更,timestampの先頭要素は0
                                data_Accelerometer.append(data)
                            elif flag:
                                #data = [current_time-initial_time,ax,ay,az] #(ax,ay,az)→(time,ax,ay,az)に変更,timestampの先頭以外はflag立ち上がり時からの現在の時間の差分
                                time_stamp += 0.0005
                                data = [time_stamp,ax,ay,az]
                                data_Accelerometer.append(data)#1試行分の計測データをまとめるリスト
                            elif prev_flag and not flag:
                                print("立ち下がり検出")
                                print(f"加速度センサ time: {initial_time} s")
                                data_Accelerometer_list.append(data_Accelerometer)#1試行単位でまとめた計測データリストをn試行分まとめるリスト   
                                data_Accelerometer=[]
                            
                            prev_flag = flag#フラグの立ち上がり・立ち下がり検出用、前回のフラグの状態を保存
                            
                            #終了時の処理を以下に記述、
                            # listのlistであるdata_Accelerometer_list((time,ax,ay,az)を束ねたデータ列を1なぞり分取得したlist、を複数なぞり分まとめたlist)をmain.pyに送信
                            # 終了条件は未定
                            
                            if cameraGrabingFinish.is_set():
                                while_flag = False
                                print("camera Grabing Finished")
                                try:
                                    send_data = [np.array(trial,dtype=np.float64)for trial in data_Accelerometer_list]
                                    print("Make send data")
                                    # 古いデータが残っていれば捨てて（念の為）、新しいデータを入れる
                                    # ※ maxsize=1設定なら、putの前にget_nowaitする
                                    """
                                    while not AccelerometerData_queue.empty():
                                        try:
                                            AccelerometerData_queue.get_nowait()
                                        except queue.Empty:                                                    
                                            break
                                    """
                                    print("Queueに加速度センサデータを送信します")
                                    AccelerometerData_queue.put(send_data)
                                    AccelerometerData_queue.close()
                                    AccelerometerData_queue.join_thread()
                                    print("Queueに加速度センサデータを送信しました")
                                    time.sleep(0.2)
                                    break               
                                except Exception as e:
                                    print(f"データ送信エラー：{e}")
                                    break#送信でループを抜けて終了
                            """
                            # サンプリング周波数の算出
                            if len(timestamps) >= 2:
                                dt_total = timestamps[-1] - timestamps[0]
                                if dt_total > 0:
                                    fps = (len(timestamps) - 1) / dt_total

                            # 0.2秒ごとに実測サンプリング周波数と加速度を表示
                            if current_time - last_print_time >= 0.2:
                                print(f"\r[Sampling Rate: {fps:6.1f} Hz]  ax: {ax:6.3f} g | ay: {ay:6.3f} g | az: {az:6.3f} g", end="", flush=True)
                                last_print_time = current_time
                            """
                            del buffer[:PACKET_SIZE]
                        else:
                            # フッタ不一致による同期ズレ復帰
                            del buffer[0]
                    else:
                        # ヘッダ不一致時は1バイト進める
                        del buffer[0]


    except serial.SerialException as e:
        print(f"\nSerial Error: {e}")
    except KeyboardInterrupt:
        print("\n\nFinished.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")
    

if __name__ == "__main__":
    temp_AccelerometerStartAcquiring = multiprocessing.Event()
    temp_AccelerometerStartAcquiring.clear()

    temp_cameraGrabingFinish = multiprocessing.Event()
    temp_cameraGrabingFinish.clear()

    temp_AccelerometerData_queue = multiprocessing.Queue(maxsize=1)

    main_process = multiprocessing.Process(target=run,args=(temp_AccelerometerStartAcquiring,temp_cameraGrabingFinish,temp_AccelerometerData_queue))
    main_process.start()
    print("1:move, 2:stop")
    while(1):
        if keyboard.is_pressed("1"):
            temp_AccelerometerStartAcquiring.set()
            time.sleep(2.8)
            temp_AccelerometerStartAcquiring.clear()
        elif keyboard.is_pressed("2"):
            temp_cameraGrabingFinish.set()
            print("finish")
            break
        time.sleep(0.01)

    acquired_Accelerometer_data = temp_AccelerometerData_queue.get()#データを受け取るまで次の行に進まない

    while main_process.is_alive():
        print("creating Accelerometer_queue")
        time.sleep(1)
    main_process.join()

    
    print("Accelerometer data got")
    num_Accelerometer_data_chunk = len(acquired_Accelerometer_data)
    if num_Accelerometer_data_chunk > 0:
        num_Accelerometer_one_data = acquired_Accelerometer_data[0].shape[0]
    else:
        num_Accelerometer_one_data = 0
    print(f"num_Accelerometer_data_chunck = {num_Accelerometer_data_chunk}")
    print(f"num_Accelerometer_one_data = {num_Accelerometer_one_data}")
    now = datetime.datetime.now()
    name = now.strftime("%Y%m%d_%H%M")
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

        
    sys.exit(0)
            
    