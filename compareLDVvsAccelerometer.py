import matplotlib
matplotlib.use('TkAgg') # GUIを使わないAggバックエンドを指定

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import matplotlib.patheffects as path_effects
from matplotlib.animation import FuncAnimation
import random
import collections
from scipy import integrate
import scipy
from scipy import signal
import os
import datetime

time_col   = 0
x_axis_col = 1
y_axis_col = 2
z_axis_col = 3
group_num = 3

def butter_highpass_fillter(x, N, Wn,fs):
    #N = フィルタ次数
    #Wn = カットオフ周波数
    #btype = フィルタのタイプ（highpass, lowpass, bandpass, bandstop）
    #analog = False, True
    #output = 出力のタイプ(ba, sos, zpk)
    #fs = デジタルフィルタの場合、サンプリング周波数
    btype = "highpass"
    analog = False
    output = "sos"
    sos = scipy.signal.butter(N, Wn, btype, analog, output, fs)

    #sos = butterの戻り値
    #x = 対象の波形
    #axis = どの軸に沿ってフィルタをかけるか
    #padtype = パディングのタイプ？
    #padlen = パディングの長さ？
    x = scipy.signal.sosfiltfilt(sos, x, axis=-1, padtype='odd', padlen=None)
    return x

def compute_welch_psd_LDV(file_name, sampling_rate, window_length, overlap_samples=None):
    
    signal_data_np = np.loadtxt(file_name+'.txt')
    signal_data_np = signal_data_np * (10**6)#mからμmに単位変換
    Wn = 50#カットオフ周波数
    order = 4#次数
    signal_data_np = butter_highpass_fillter(signal_data_np, order, Wn,sampling_rate)

    # 引数の型チェックとデフォルト値の設定
    if not isinstance(signal_data_np, np.ndarray):
        raise TypeError("Input signal_data_np must be a NumPy array.")

    if overlap_samples is None:
        overlap_samples = window_length // 2

    # 信号の基本情報
    num_samples = signal_data_np.shape[0] # 信号の総サンプル数
    win = np.hanning(window_length) # ハニング窓を生成 

    # STFT/Welch法計算のためのパラメータ
    num_freq_bins = window_length // 2 + 1 # rfftの結果の有効な周波数ビンの数 (DC成分とナイキスト周波数成分を含む)
    hop_size = window_length - overlap_samples # 窓の移動量 (ホップサイズ)
    
    if hop_size <= 0:
        raise ValueError("Hop size must be positive. window_length must be greater than overlap_samples.")

    # 計算されるフレームの総数を決定
    # 信号長が窓長より短い場合は1フレームとして扱う
    if num_samples < window_length:
        num_frames = 1
    else:
        # 窓が完全に収まる最後の位置までのフレーム数 + 1 (最初のフレーム)
        num_frames = (num_samples - window_length) // hop_size + 1
    
    if num_frames <= 0 and num_samples > 0: # 信号があるのにフレーム数が0になる非常に短い信号の場合
        num_frames = 1

    # 各フレームのパワースペクトル（ピリオドグラム）を一時的に格納するリスト
    periodograms = []

    print(f"Calculating Welch PSD:")
    print(f"  Total Samples: {num_samples}")
    print(f"  Sampling Rate: {sampling_rate} Hz")
    print(f"  Window Length (Lf): {window_length} samples")
    print(f"  Overlap Samples: {overlap_samples}")
    print(f"  Hop Size: {hop_size} samples")
    print(f"  Number of Frames: {num_frames}")
    #print(f"  Nyquist Frequency (Mf): {num_freq_bins}")

    # STFTの計算ループとピリオドグラムの収集
    for n in range(num_frames):
        start_idx = n * hop_size
        end_idx = start_idx + window_length

        current_frame = np.zeros(window_length) # ゼロで埋めたフレームを作成
        
        # 実際にデータがある部分をコピーし、窓長に満たない部分はゼロパディングされる
        data_to_copy_len = min(window_length, num_samples - start_idx)
        
        if data_to_copy_len <= 0: # 処理すべきデータがもうない場合
            break

        current_frame[:data_to_copy_len] = signal_data_np[start_idx : start_idx + data_to_copy_len]
        
        windowed_frame = current_frame * win # 窓関数を適用
        
        fft_result = np.fft.rfft(windowed_frame, n=window_length, axis=0) # 実数入力用FFT
        delta_f = sampling_rate/window_length
        periodogram = (np.abs(fft_result) / window_length)**2 # 各セグメントのパワースペクトル（ピリオドグラム）を計算、周期信号が対象
        periodogram = periodogram/delta_f # 各セグメントのパワースペクトル密度を計算、連続ランダム信号が対象
        periodogram[1:-1] *=2.0
        periodograms.append(periodogram)

    if not periodograms:
        print("Error: No frames could be processed. Check signal length and window parameters.")
        return

    # スペクトル平均化 (Welch法の中核)
    # 収集した全てのピリオドグラムを周波数ビンごとに平均化する
    averaged_psd = np.mean(periodograms, axis=0)
    
    # パワースペクトルをdBスケールに変換 (0の対数を避けるため微小値1e-18を加算)
    P_welch_db = 10 * np.log10(averaged_psd + 1e-18) 
    
    #P_welch_db = averaged_psd

    # 周波数軸の生成
    freq_axis = np.fft.rfftfreq(window_length, 1/sampling_rate)

    return P_welch_db, freq_axis

def file_open(file_name,axis_col):
    data = np.loadtxt(file_name+'.txt')
    data_target_col = data[:,axis_col] * 9.80665
    data_time = data[:,0]
    return data_target_col,data_time

def compute_welch_psd_Accel(file_name,acc_data_slice, sampling_rate, window_length, overlap_samples=None):

    print(f"file_name: {file_name}")
    acc_data,time = file_open(file_name,z_axis_col)
    acc_data = acc_data[acc_data_slice[0]:acc_data_slice[1]]#相互相関関数の最大値から算出した振動の同期ポイント
    time = time[acc_data_slice[0]:acc_data_slice[1]]
    vel_data = integrate.cumulative_trapezoid(acc_data, x=time, initial=0)
    pos_data = integrate.cumulative_trapezoid(vel_data, x=time, initial=0)
    signal_data_np = pos_data * (10**6)#mからμmに単位変換

    Wn = 50#カットオフ周波数
    order = 4#次数
    signal_data_np = butter_highpass_fillter(signal_data_np, order, Wn,sampling_rate)

    # 引数の型チェックとデフォルト値の設定
    if not isinstance(signal_data_np, np.ndarray):
        raise TypeError("Input signal_data_np must be a NumPy array.")

    if overlap_samples is None:
        overlap_samples = window_length // 2

    # 信号の基本情報
    num_samples = signal_data_np.shape[0] # 信号の総サンプル数
    win = np.hanning(window_length) # ハニング窓を生成 

    # STFT/Welch法計算のためのパラメータ
    num_freq_bins = window_length // 2 + 1 # rfftの結果の有効な周波数ビンの数 (DC成分とナイキスト周波数成分を含む)
    hop_size = window_length - overlap_samples # 窓の移動量 (ホップサイズ)
    
    if hop_size <= 0:
        raise ValueError("Hop size must be positive. window_length must be greater than overlap_samples.")

    # 計算されるフレームの総数を決定
    # 信号長が窓長より短い場合は1フレームとして扱う
    if num_samples < window_length:
        num_frames = 1
    else:
        # 窓が完全に収まる最後の位置までのフレーム数 + 1 (最初のフレーム)
        num_frames = (num_samples - window_length) // hop_size + 1
    
    if num_frames <= 0 and num_samples > 0: # 信号があるのにフレーム数が0になる非常に短い信号の場合
        num_frames = 1

    # 各フレームのパワースペクトル（ピリオドグラム）を一時的に格納するリスト
    periodograms = []

    print(f"Calculating Welch PSD:")
    print(f"  Total Samples: {num_samples}")
    print(f"  Sampling Rate: {sampling_rate} Hz")
    print(f"  Window Length (Lf): {window_length} samples")
    print(f"  Overlap Samples: {overlap_samples}")
    print(f"  Hop Size: {hop_size} samples")
    print(f"  Number of Frames: {num_frames}")
    #print(f"  Nyquist Frequency (Mf): {num_freq_bins}")

    # STFTの計算ループとピリオドグラムの収集
    for n in range(num_frames):
        start_idx = n * hop_size
        end_idx = start_idx + window_length

        current_frame = np.zeros(window_length) # ゼロで埋めたフレームを作成
        
        # 実際にデータがある部分をコピーし、窓長に満たない部分はゼロパディングされる
        data_to_copy_len = min(window_length, num_samples - start_idx)
        
        if data_to_copy_len <= 0: # 処理すべきデータがもうない場合
            break

        current_frame[:data_to_copy_len] = signal_data_np[start_idx : start_idx + data_to_copy_len]
        
        windowed_frame = current_frame * win # 窓関数を適用
        
        fft_result = np.fft.rfft(windowed_frame, n=window_length, axis=0) # 実数入力用FFT
        delta_f = sampling_rate/window_length
        periodogram = (np.abs(fft_result) / window_length)**2 # 各セグメントのパワースペクトル（ピリオドグラム）を計算、周期信号が対象
        periodogram = periodogram/delta_f # 各セグメントのパワースペクトル密度を計算、連続ランダム信号が対象
        periodogram[1:-1] *=2.0
        periodograms.append(periodogram)

    if not periodograms:
        print("Error: No frames could be processed. Check signal length and window parameters.")
        return

    # スペクトル平均化 (Welch法の中核)
    # 収集した全てのピリオドグラムを周波数ビンごとに平均化する
    averaged_psd = np.mean(periodograms, axis=0)
    
    # パワースペクトルをdBスケールに変換 (0の対数を避けるため微小値1e-18を加算)
    P_welch_db = 10 * np.log10(averaged_psd + 1e-18) 

    # 周波数軸の生成
    freq_axis = np.fft.rfftfreq(window_length, 1/sampling_rate)

    return P_welch_db, freq_axis


def plot_welch_psd(freq_1,psd_1,freq_2,psd_2,rootdir):
    
    # --- プロット設定 ---
    figsize = (8, 6) 
    dpi = 150
    fig = plt.figure(figsize=figsize, dpi=dpi)

    # Matplotlibのスタイル設定
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['xtick.top'] = True
    plt.rcParams['xtick.major.size'] = 6
    plt.rcParams['xtick.minor.size'] = 3
    plt.rcParams['xtick.minor.visible'] = True
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['ytick.right'] = True
    plt.rcParams['ytick.major.size'] = 6
    plt.rcParams['ytick.minor.size'] = 3
    plt.rcParams['ytick.minor.visible'] = True
    plt.rcParams["font.size"] = 20 
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['agg.path.chunksize'] = 10000
    plt.rcParams['path.simplify_threshold'] = 0.12
    
    #ax_psd = fig.add_axes([0.1, 0.10, 0.8, 0.40]) # PSDプロット領域
    ax_psd = fig.add_axes([0.1, 0.30, 0.8, 0.5]) # プロット領域の座標 [left, bottom, width, height]
    
    # 周波数軸の表示範囲設定
    # 論文の記述「frequency components below 50 Hz are ignored」に合わせて、プロット開始点を50Hzに設定
    freq_min_plot = 50 # 表示開始周波数 (Hz)
    freq_max_plot = 600 # ナイキスト周波数まで表示 (Hz)はしてない
    
    ax_psd.set_xlim(freq_min_plot, freq_max_plot)
    ax_psd.set_xlabel('Freq [Hz]')
    ax_psd.tick_params(labelbottom=True, labelsize=16)
    #ax_psd.set_ylabel('Power Spectral Density [dB]')
    #ax_psd.set_title("Power Spectral Density (Welch's Method)")
    #ax_psd.set_ylim(40,100)
    ax_psd.set_ylim(-80,20)
    ax_psd.set_ylabel('Power Spectral [dB]')
    ax_psd.set_title("Power Spectral Density(Welch's Method)")
    
    # PSDのY軸範囲は自動調整が基本だが、必要に応じて固定値も設定可能 (例: ax_psd.set_ylim(-150, 0))

    ax_psd.plot(freq_1, psd_1, c='blue',label='LDV') # PSDを線グラフでプロット
    ax_psd.plot(freq_2, psd_2, c='red',label='Accelerometer')

    
    # 出力ディレクトリが存在しない場合は作成
    #os.makedirs(output_dir, exist_ok=True)
    #output_full_path = os.path.join(output_dir, f"{base_filename}.png")
    
    output_full_path = rootdir+'compare_welch_psd_LDV_vs_Accel.png'
    plt.savefig(output_full_path)
    plt.show()

def welch_method(file_name, acc_data_slice):
    rootdir = 'C:/Users/yuto/Documents/system_python/data/'
    file_name_LDV = rootdir+'LDVdata/'+file_name+'_1'
    file_name_Accel = rootdir+'AccelerometerData/'+file_name+'_acceleration'+'_1'

    dt_LDV = 1/218750
    window_length_LDV = 2**15

    dt_Accel = 0.0005
    window_length_Accel = 2**8

    psd_LDV,freq_LDV = compute_welch_psd_LDV(file_name_LDV,1/dt_LDV,window_length_LDV)
    psd_Accel,freq_Accel = compute_welch_psd_Accel(file_name_Accel, acc_data_slice, 1/dt_Accel,window_length_Accel)

    plot_welch_psd(freq_LDV,psd_LDV,freq_Accel,psd_Accel,rootdir)

def NCC(data_1,data_2,dt_LDV,dt_Accel):
    if len(data_1)>len(data_2):
        num_samples = int(len(data_1)/(1/dt_LDV)*(1/dt_Accel))
        data_1 = signal.resample(data_1,num_samples)
    else:
        num_samples = int(len(data_2)/(1/dt_LDV)*(1/dt_Accel))
        data_2 = signal.resample(data_2,num_samples)

    min_len = min(len(data_1),len(data_2))
    data_1 = data_1[:min_len]
    data_2 = data_2[:min_len]

    maxlag = 80
    
    lags, c, line, b = plt.xcorr(data_1, data_2, maxlags=maxlag)
    #plt.xticks(np.arange(-80,81,40),np.arange(-80*0.0005,81*0.0005,40*0.0005))
    plt.xticks(np.arange((-1)*maxlag,maxlag+1,10))
    plt.xlabel("lag")
    plt.ylabel("correlation coefficient")
    plt.show()

    max_idx = np.argmax(c)
    max_lag = lags[max_idx]
    print(f"相互相関が最大となるラグ：{max_lag}")
    print(f"最大の相関係数：{c[max_idx]}")


    return max_lag

def plot_pos_data(data_1,data_2,dt_LDV,dt_Accel):
    if len(data_1)>len(data_2):
        num_samples = int(len(data_1)/(1/dt_LDV)*(1/dt_Accel))
        data_1 = signal.resample(data_1,num_samples)
    else:
        num_samples = int(len(data_2)/(1/dt_LDV)*(1/dt_Accel))
        data_2 = signal.resample(data_2,num_samples)

    min_len = min(len(data_1),len(data_2))
    data_1 = data_1[:min_len]
    data_2 = data_2[:min_len]
    
    # --- プロット設定 ---
    figsize = (8, 6) 
    dpi = 150
    fig = plt.figure(figsize=figsize, dpi=dpi)

    # Matplotlibのスタイル設定
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['xtick.top'] = True
    plt.rcParams['xtick.major.size'] = 6
    plt.rcParams['xtick.minor.size'] = 3
    plt.rcParams['xtick.minor.visible'] = True
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['ytick.right'] = True
    plt.rcParams['ytick.major.size'] = 6
    plt.rcParams['ytick.minor.size'] = 3
    plt.rcParams['ytick.minor.visible'] = True
    plt.rcParams["font.size"] = 20 
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['agg.path.chunksize'] = 10000
    plt.rcParams['path.simplify_threshold'] = 0.12

    len_data = len(data_1)
    
    ax1 = fig.add_axes([0.1, 0.3, 0.8, 0.5]) # プロット領域の座標 [left, bottom, width, height]
    #ax1.set_xlim(0.0, len_data*dt_Accel) # 時間軸の表示範囲を信号全体に設定
    ax1.set_xlim(len_data*dt_Accel/4, len_data*dt_Accel/4*2)
    ax1.set_xlabel('Time [s]')
    ax1.tick_params(labelbottom=True, labelsize=16)
    #ax1.set_ylim(-15,15)
    ax1.set_ylim(-5,5)
    ax1.set_ylabel('Pos [μm]')
    
    time_axis_signal = np.linspace(0, len_data*dt_Accel, num=len_data)
    ax1.plot(time_axis_signal, data_1, c='blue')
    ax1.plot(time_axis_signal, data_2, c='red')
    ax1.set_title("Time-Domain Displacement Signal")
    
    # PSDのY軸範囲は自動調整が基本だが、必要に応じて固定値も設定可能 (例: ax_psd.set_ylim(-150, 0))
    
    # 出力ディレクトリが存在しない場合は作成
    #os.makedirs(output_dir, exist_ok=True)
    #output_full_path = os.path.join(output_dir, f"{base_filename}.png")
    
    #output_full_path = rootdir+'_welch_ps.png'
    #plt.savefig(output_full_path)
    plt.show()

def NCC_method(file_name):
    rootdir = 'C:/Users/yuto/Documents/system_python/data/'
    file_name_LDV = rootdir+'LDVdata/'+file_name+'_1'
    file_name_Accel = rootdir+'AccelerometerData/'+file_name+'_acceleration'+'_1'

    dt_LDV = 1/218750
    window_length_LDV = 2**15
    
    dt_Accel = 0.0005
    window_length_Accel = 2**8

    data_LDV = np.loadtxt(file_name_LDV+'.txt')
    data_LDV = data_LDV * (10**6)#mからμmに単位変換
    Wn = 50#カットオフ周波数
    order = 4#次数
    data_LDV = butter_highpass_fillter(data_LDV, order, Wn,1/dt_LDV)

    acc_data,time = file_open(file_name_Accel,z_axis_col)

    #計測結果から予想した同期の計測開始時間、(加速度センサの開始時)-(LDVの開始時)=0.1373706、0.1373706/0.0005=274.7412、274+(131072点*(1/218750 s))/0.0005=1483.1138
    acc_data_first_idx = 274
    acc_data_last_idx = 1473
    acc_data_slice = [acc_data_first_idx,acc_data_last_idx]

    acc_data_sliced = acc_data[acc_data_slice[0]:acc_data_slice[1]]
    time_sliced = time[acc_data_slice[0]:acc_data_slice[1]]

    vel_data = integrate.cumulative_trapezoid(acc_data_sliced, x=time_sliced, initial=0)
    pos_data = integrate.cumulative_trapezoid(vel_data, x=time_sliced, initial=0)
    data_Accel = pos_data * (10**6)#mからμmに単位変換

    data_Accel = butter_highpass_fillter(data_Accel, order, Wn,1/dt_Accel)

    max_lag = NCC(data_LDV,data_Accel,dt_LDV,dt_Accel)

    #相互相関関数の結果から、最も相関が高くなったラグ分だけデータをずらす
    acc_data_slice = [idx - max_lag for idx in acc_data_slice ]
    acc_data_sliced = acc_data[acc_data_slice[0]:acc_data_slice[1]]
    time_sliced = time[acc_data_slice[0]:acc_data_slice[1]]
    vel_data = integrate.cumulative_trapezoid(acc_data_sliced, x=time_sliced, initial=0)
    pos_data = integrate.cumulative_trapezoid(vel_data, x=time_sliced, initial=0)
    data_Accel = pos_data * (10**6)#mからμmに単位変換    
    data_Accel = butter_highpass_fillter(data_Accel, order, Wn,1/dt_Accel)

    plot_pos_data(data_LDV,data_Accel,dt_LDV,dt_Accel)

    return acc_data_slice





if __name__ == "__main__":
    filename = "0928_03スラブ_60mms/20260928_1944"
    #filename = "0928_02帆布11号_60mms/20260928_1919"
    #filename = "0928_04撥水無地クロス_60mms/20260928_1950"
    filename = "0928_05プリンセスサテン凹凸少向き_60mms/20260928_1955"
    
    acc_data_slice = NCC_method(filename)
    welch_method(filename, acc_data_slice)
    
     