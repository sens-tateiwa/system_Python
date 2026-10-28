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
import os
import datetime
import csv
from scipy import integrate

time_col   = 0
x_axis_col = 1
y_axis_col = 2
z_axis_col = 3
group_num = 4


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

def plot_group_comparison_ver2(freq, group, file_num, labels=None):
    """
    freq: 周波数軸 (長さ N の1次元配列)
    group_data_list: 各グループのデータ配列 (形状 (M, N)) が格納されたリスト
    group_num: 比較するグループの数 (len(group_data_list) と等しい)
    labels: 各グループのラベルのリスト (オプション。未指定の場合は Group 1, 2... になります)
    """

    # 比較する数に合わせて自動で綺麗に色分けするためのカラーマップを設定
    # (数が多い場合は 'tab10' や 'jet' などを使い分けると便利です)
    cmap = plt.get_cmap('tab10')

    # labelsが指定されていない、あるいは個数が合わない場合のデフォルトラベル作成
    if labels is None or len(labels) < file_num:
        labels = [f"Group {i+1}" for i in range(file_num)]

    plt.figure(figsize=(16, 9))
    
    # --- グループ数 (group_num) に応じたループ処理 ---
    for i in range(file_num):
        data = group[i*group_num:(i+1)*group_num]
        label = labels[i]
        color = cmap(i)  # グループ番号に応じたカラーを自動取得
        
        # 1. 各グループの平均と標準偏差を計算 (axis=0 は「データセット方向」)
        mean_val = np.mean(data, axis=0)
        std_val = np.std(data, axis=0)
        
        # 2. 平均値を実線でプロット
        plt.plot(freq, mean_val, color=color, label=f"{label} (Mean)")
        
        # 3. 平均 ± 標準偏差 の範囲を塗りつぶす
        plt.fill_between(
            freq, 
            mean_val - std_val, 
            mean_val + std_val, 
            color=color, 
            alpha=0.15,  # グループ数が多いときは重なりを考慮してalphaを少し薄め(0.15など)にするのがおすすめ
            label=f"{label} (Std Dev)"
        )
    
    # --- グラフの装飾 ---
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Power Spectral [dB]')
    #plt.xlim(50, 1000)
    plt.xlim(50, 600)
    #plt.ylim(40, 100)
    plt.ylim(-80,20)
    plt.title('Comparison of Spectral Characteristics (Mean ± SD)')
    plt.legend()
    plt.grid(True)
    
    # タイムスタンプ付きで保存
    now = datetime.datetime.now()
    name = now.strftime("%Y%m%d_%H%M")
    save_path = f'C:/Users/yuto/Documents/system_python/data/Accelerometerdata/Comparison_of_Spectral_{name}.png'
    plt.savefig(save_path)
    
    #plt.show()

#group_num個ずつのデータ(file_name_{i:(1~10)}.txt)を持ったfile_nameを2つ準備する。そのfile_name2つをリストにしたfile_name_listを渡す
def group_comparison(file_name_list, window_length, labels=None, overlap_samples=None):
    #rootDir = "C:/Users/yuto/Downloads/cluster_haptic_texture_dataset_mini/cluster_haptic_texture_dataset_mini/sensor_data/accel/0"
    rootDir = 'C:/Users/yuto/Documents/system_python/data/AccelerometerData'
    group = []
    group_A = []
    group_B = []
    file_num = 0
    Wn = 50#カットオフ周波数
    order = 4#次数
    for file in file_name_list:
        for num in range(group_num):
            file_name = rootdir+'/'+file+f"_{num+1}"
            print(f"file_name: {file_name}")
            acc_data,time = file_open(file_name,z_axis_col)
            acc_data = acc_data[274:1473]#計測した計測開始タイム、(加速度センサの開始時)-(LDVの開始時)=0.1373706、0.1373706/0.0005=274.7412、274+(131072点*(1/218750 s))/0.0005=1483.1138
            time = time[274:1473]
            vel_data = integrate.cumulative_trapezoid(acc_data, x=time, initial=0)
            pos_data = integrate.cumulative_trapezoid(vel_data, x=time, initial=0)


            pos_data = pos_data * (10**6)#mからμmに単位変換
            intervals_sec = np.diff(time)
            mean_interval_sec = np.mean(intervals_sec)
            print(f"dt = {mean_interval_sec}")
            sampling_rate = 1/mean_interval_sec

            
            dt = 0.0005
            fftplt_indiv(file_name,pos_data, dt)
            compute_welch_psd_and_plot(file_name,pos_data, sampling_rate, window_length, overlap_samples=None)

            print(f"sampling rate = {sampling_rate}")
            pos_data = butter_highpass_fillter(pos_data, order, Wn, sampling_rate)
            if overlap_samples is None:
                overlap_samples = window_length // 2

            # 信号の基本情報
            num_samples = len(pos_data) # 信号の総サンプル数
            win = np.hanning(window_length) # ハニング窓を生成 

            # STFT/Welch法計算のためのパラメータ
            num_freq_bins = window_length // 2 + 1 # rfftの結果の有効な周波数ビンの数 (DC成分とナイキスト周波数成分を含む)
            hop_size = window_length - overlap_samples # 窓の移動量 (ホップサイズ)
            if num_samples < window_length:
                num_frames = 1
            else:
                # 窓が完全に収まる最後の位置までのフレーム数 + 1 (最初のフレーム)
                num_frames = (num_samples - window_length) // hop_size + 1
            
            if num_frames <= 0 and num_samples > 0: # 信号があるのにフレーム数が0になる非常に短い信号の場合
                num_frames = 1

            # 各フレームのパワースペクトル（ピリオドグラム）を一時的に格納するリスト
            periodograms = []
            # STFTの計算ループとピリオドグラムの収集
            for n in range(num_frames):
                start_idx = n * hop_size
                end_idx = start_idx + window_length

                current_frame = np.zeros(window_length) # ゼロで埋めたフレームを作成
                
                # 実際にデータがある部分をコピーし、窓長に満たない部分はゼロパディングされる
                data_to_copy_len = min(window_length, num_samples - start_idx)
                
                if data_to_copy_len <= 0: # 処理すべきデータがもうない場合
                    break

                current_frame[:data_to_copy_len] = pos_data[start_idx : start_idx + data_to_copy_len]
                
                windowed_frame = current_frame * win # 窓関数を適用
                
                fft_result = np.fft.rfft(windowed_frame, n=window_length, axis=0) # 実数入力用FFT
                delta_f = sampling_rate/window_length
                periodogram = (np.abs(fft_result) / window_length)**2 # 各セグメントのパワースペクトル（ピリオドグラム）を計算、周期信号が対象
                periodogram = periodogram/delta_f # 各セグメントのパワースペクトル密度を計算、連続ランダム信号が対象
                periodogram[1:-1] *=2.0
                periodograms.append(periodogram)
            # スペクトル平均化 (Welch法の中核)
            # 収集した全てのピリオドグラムを周波数ビンごとに平均化する
            averaged_psd = np.mean(periodograms, axis=0)
                
            # パワースペクトルをdBスケールに変換 (0の対数を避けるため微小値1e-18を加算)
            P_welch_db = 10 * np.log10(averaged_psd + 1e-18) 
            
            #P_welch_db = averaged_psd

            group.append(P_welch_db)
        file_num += 1

    # 周波数軸の生成
    freq_axis = np.fft.rfftfreq(window_length, 1/sampling_rate)
    
    plot_group_comparison_ver2(freq_axis, group,file_num,labels)
    return 0

def file_csv_open(rootdir,file_name,axis_col):
    with open(rootdir+'/'+file_name+'.csv', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        file = []
        file_time  = []
        for row in reader:
            #print(row)
            file.append(float(row[axis_col])*9.80665)#g(重力加速度)で記録されているためm/s^2に変換
            file_time.append(float(row[time_col]))
    return file,file_time

def file_open(file_name,axis_col):
    data = np.loadtxt(file_name+'.txt')
    data_target_col = data[:,axis_col] * 9.80665
    data_time = data[:,0]
    return data_target_col,data_time

def file_open_full(file_name):
    data = np.loadtxt(file_name+'.txt')
    data_x = data[:,x_axis_col] * 9.80665
    data_y = data[:,y_axis_col] * 9.80665
    data_z = data[:,z_axis_col] * 9.80665
    data_time = data[:,0]
    return data_time,data_x,data_y,data_z

def plot_and_save_3axis(file_name):
  data_time, data_x, data_y, data_z = file_open_full(file_name)

  # 3行1列のサブプロット作成（横10インチ、縦8インチ、横軸を共有）
  fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

  # X軸プロット
  axes[0].plot(data_time, data_x, color='tab:red', label='X-axis')
  axes[0].set_ylabel('Acc X [m/s²]')
  axes[0].grid(True)
  axes[0].legend(loc='upper right')

  # Y軸プロット
  axes[1].plot(data_time, data_y, color='tab:green', label='Y-axis')
  axes[1].set_ylabel('Acc Y [m/s²]')
  axes[1].grid(True)
  axes[1].legend(loc='upper right')

  # Z軸プロット
  axes[2].plot(data_time, data_z, color='tab:blue', label='Z-axis')
  axes[2].set_ylabel('Acc Z [m/s²]')
  axes[2].set_xlabel('Time [s]')
  axes[2].grid(True)
  axes[2].legend(loc='upper right')

  # タイトル設定とレイアウト調整
  fig.suptitle(f'3-Axis Acceleration: {os.path.basename(file_name)}')
  plt.tight_layout()

  # 保存とメモリ解放
  save_path = f'{file_name}_3axis_acceleration.png'
  plt.savefig(save_path, dpi=300)
  plt.close(fig)
  

def compute_welch_psd_and_plot(file_name,data, sampling_rate, window_length, overlap_samples=None):
    
    signal_data_np = data
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

    # --- プロット設定 ---
    figsize = (16, 12) 
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

    # --- 元データのプロット (上段) ---
    ax1 = fig.add_axes([0.1, 0.60, 0.8, 0.35]) # プロット領域の座標 [left, bottom, width, height]
    ax1.set_xlim(0.0, num_samples/sampling_rate) # 時間軸の表示範囲を信号全体に設定
    ax1.set_xlabel('Time [s]')
    ax1.tick_params(labelbottom=True, labelsize=16)
    ax1.set_ylim(-15,15)
    ax1.set_ylabel('Pos [μm]')
    
    time_axis_signal = np.linspace(0, num_samples/sampling_rate, num=num_samples)
    ax1.plot(time_axis_signal, signal_data_np, c='black')
    ax1.set_title("Time-Domain Displacement Signal")

    # --- Welch PSDのプロット (下段) ---
    ax_psd = fig.add_axes([0.1, 0.10, 0.8, 0.40]) # PSDプロット領域
    
    # 周波数軸の表示範囲設定
    # 論文の記述「frequency components below 50 Hz are ignored」に合わせて、プロット開始点を50Hzに設定
    freq_min_plot = Wn # 表示開始周波数 (Hz)
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

    ax_psd.plot(freq_axis, P_welch_db, c='blue') # PSDを線グラフでプロット

    
    # 出力ディレクトリが存在しない場合は作成
    #os.makedirs(output_dir, exist_ok=True)
    #output_full_path = os.path.join(output_dir, f"{base_filename}.png")
    
    output_full_path = file_name+'_welch_ps.png'
    plt.savefig(output_full_path)
    #plt.show()

def fftplt_indiv(file_name, data, dt):
    f_s = 1.0 / dt
    N = len(data)  # ★ハードコード値ではなく、実際のデータ長から取得

    df = np.array(data, dtype=np.float64)
    Wn = 50  # カットオフ周波数
    order = 4  # 次数
    filtered_data = butter_highpass_fillter(df, order, Wn, f_s)

    X = np.fft.fft(filtered_data)
    X = np.abs(X) ** 2 
    X[0] = 0

    f = np.fft.fftfreq(N, dt)

    plt.figure()
    plt.xlabel('time [s]')
    #plt.ylabel('Pos [μm]')
    plt.ylabel('Pos [mm]')
    #plt.ylim(-50, 100)
    #plt.xlim(0.0,0.7)

    # ★ N点に合わせた時間軸を生成 (0 〜 (N-1)*dt)
    t = np.arange(N) * dt
    plt.plot(t, df/(10**3))
    plt.savefig(file_name + '_Displacement_元データ.png')
    plt.close()  # メモリ解放のため close を推奨

    freq_min = 50
    freq_max = 600

    plt.figure()
    plt.xlabel('Freq [Hz]')
    plt.xlim(freq_min, freq_max)
    plt.ylabel('Power spectol [μm^2]')
    plt.plot(f[0 : int(N / 2)], X[0 : int(N / 2)])
    plt.savefig(file_name + f'_frequency{freq_min}-{freq_max}.png')
    plt.close()

if __name__ == "__main__":
    #rootdir = "C:/Users/yuto/Downloads/cluster_haptic_texture_dataset_mini/cluster_haptic_texture_dataset_mini/sensor_data/accel/0"
    rootdir = "C:/Users/yuto/Documents/system_python/data/AccelerometerData"
    
    file_list_csv = ["0_0_60_500","0_0_60_1000"]   #y軸
    #file_list_csv = ["0_90_60_500","0_90_60_1000"] #x軸
    file_list_csv = ["20260917_1642_acceleration"]
    file_list_csv = ["0928_01フェルト_60mms/20260928_1735_acceleration"]
    file_list_csv = ["0928_01フェルト_60mms/20260928_1735_acceleration","0928_02帆布11号_60mms/20260928_1919_acceleration","0928_03スラブ_60mms/20260928_1944_acceleration","0928_04撥水無地クロス_60mms/20260928_1950_acceleration",
                 "0928_05プリンセスサテン凹凸少向き_60mms/20260928_1955_acceleration","0928_06プリンセスサテン凹凸多向き_60mms/20260928_2001_acceleration"]
    labels = ["Felt","canvas","Slab","Cloth","Satin (right side)","Satin (wrong side)"]
    window_length = 2**8
    group_comparison(file_list_csv, window_length, labels=labels, overlap_samples=None)
    #plot_and_save_3axis(rootdir+'/'+'20260924_1941_acceleration_1')
    
    """
    sample_count = 2**17
    dt = 1/218750
    window_length = 2**15
    group_comparison(file_list,1/dt, window_length, overlap_samples=None)
    """