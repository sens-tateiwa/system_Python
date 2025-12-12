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

def gamma(freq):
    values=[[20 , 1.30], 
            [50 , 1.24],
            [100, 1.10],
            [200, 1.08],
            [250, 1.10],
            [300, 1.20],
            [500, 1.11],
            [1000,1.27]]
    #print(f"freq = {freq}")
    
    match freq:
        case freq if freq<20:
            return 0
        case freq if freq<50:
            x_1 = values[0][0]
            y_1 = values[0][1]
            x_2 = values[1][0]
            y_2 = values[1][1]
        case freq if freq<100:
            x_1 = values[1][0]
            y_1 = values[1][1]
            x_2 = values[2][0]
            y_2 = values[2][1]
        case freq if freq<200:
            x_1 = values[2][0]
            y_1 = values[2][1]
            x_2 = values[3][0]
            y_2 = values[3][1]
        case freq if freq<250:
            x_1 = values[3][0]
            y_1 = values[3][1]
            x_2 = values[4][0]
            y_2 = values[4][1]
        case freq if freq<300:
            x_1 = values[4][0]
            y_1 = values[4][1]
            x_2 = values[5][0]
            y_2 = values[5][1]
        case freq if freq<500:
            x_1 = values[5][0]
            y_1 = values[5][1]
            x_2 = values[6][0]
            y_2 = values[6][1]
        case freq if freq<1000:
            x_1 = values[6][0]
            y_1 = values[6][1]
            x_2 = values[7][0]
            y_2 = values[7][1]
    #print(f"x_1 = {x_1}")
    #print(f"y_1 = {y_1}")
    #print(f"x_2 = {x_2}")
    #print(f"y_2 = {y_2}")
    try:
        value = (y_1*(x_2-freq)+y_2*(freq-x_1))/(x_2-x_1)
        #print(f"gamma value = {value}")
    except:
        value = 0
        #print(f"gamma value is always 0")
    return value

def correct_data(file_name,x,r,sample_count,dt):
    x = x*(10**6)#xはμm単位、今回はmで計測しているため変換
    X = np.fft.fft(x)
    X[0] = 0
    f = np.fft.fftfreq(sample_count,dt)
    data = [X_i*(r**gamma(freq)) for (X_i,freq) in zip(X,f)]#元信号xはμm、rはmmで計算する
    corrected_x=np.fft.ifft(data)
    

    N = sample_count
    plt.figure()
    plt.xlabel('time [s]')
    plt.ylabel('Displacement [μm]')
    #plt.ylim(-12,12)
    #plt.tick_params(labelsize=45)
    #plt.subplots_adjust(0.2,0.15,0.97,0.95)
    t = np.linspace(0,dt*N,N)
    #plt.plot(t, csv_velocity) # 入力信号
    plt.plot(t,x)
    plt.savefig(file_name+'_補正前.png')

    plt.figure()
    plt.xlabel('time [s]')
    plt.ylabel('Displacement [μm]')
    #plt.ylim(-12,12)
    #plt.tick_params(labelsize=45)
    #plt.subplots_adjust(0.2,0.15,0.97,0.95)
    t = np.linspace(0,dt*N,N)
    #plt.plot(t, csv_velocity) # 入力信号
    plt.plot(t,corrected_x)
    plt.savefig(file_name+'_補正後.png')

    corrected_x = corrected_x/(10**6) #xをmからμmに戻す
    return corrected_x.real

def fftplt_indiv(file_name, sample_count, dt):
    #rootdir = 'C:/Users/yuto/Documents/optotune/measuredData/'
    #dt = 4.57142857*10**(-6)#得られたデータのtimestampの間隔
    f_s = 1/dt
    #N = 1000#run2のsmplecountに合わせる
    N = sample_count

    
    df = []
    """
    df = pd.read_csv(file_name)    
    text=df.to_string()

    text = text.split('\n')
    
    for j in range(0,N,1):
        text[j] = text[j].split(";")
    text = text[0:N]
    try:
        csv_velocity = [float(x[1]) for x in text]
    except:
        csv_velocity = [float(x[0]) for x in text]
    X=np.fft.fft(csv_velocity)
    """
    
    df = np.loadtxt(file_name+'.txt')
    r_mm = 30
    #df = correct_data(file_name,df,r_mm,sample_count,dt)

    X=np.fft.fft(df)
    

    #print(f"X[0] = {X[0]}")
    X[0] = 0
            
    f = np.fft.fftfreq(N,dt)
    
    #plt.rcParams["font.size"]=60
    plt.figure()
    plt.xlabel('time [s]')
    plt.ylabel('Displacement m')
    plt.ylim(-0.012,0.012)
    #plt.tick_params(labelsize=45)
    plt.subplots_adjust(0.2,0.15,0.97,0.95)
    t = np.linspace(0,dt*N,N)
    #plt.plot(t, csv_velocity) # 入力信号
    plt.plot(t,df)
    plt.savefig(file_name+'_Displacement_元データ.png')
    
    #plt.rcParams["font.size"]=60
    plt.figure()
    plt.xlabel('Frequency [Hz]')
    #plt.xlim(f[1],500)
    plt.xlim(f[0],50)
    plt.ylabel('Amplitude')
    #plt.ylim(0,0.25)
    #plt.tick_params(labelsize=45)
    plt.subplots_adjust(0.2,0.15,0.97,0.95)
    #plt.plot(f[1:int(N/2)],np.abs((X)/(N/2))[1:int(N/2)])
    plt.plot(f[0:int(N/2)],np.abs((X)/np.sqrt(N))[0:int(N/2)])
    plt.savefig(file_name+'_frequency1-50.png')

    plt.figure()
    plt.xlabel('Frequency [Hz]')
    plt.xlim(f[0],600)
    #plt.xlim(f[1],50)
    plt.ylabel('Amplitude')
    #plt.ylim(0,0.3)
    #plt.tick_params(labelsize=45)
    plt.subplots_adjust(0.2,0.15,0.97,0.95)
    #plt.plot(f[1:int(N/2)],np.abs((X)/(N/2))[1:int(N/2)])
    plt.plot(f[0:int(N/2)],np.abs((X)/np.sqrt(N))[0:int(N/2)])
    plt.savefig(file_name+'_frequency1-500.png')

    #plt.show()

def butter_highpass_fillter(x, N, Wn, btype, analog, output,fs):
    #N = フィルタ次数
    #Wn = カットオフ周波数
    #btype = フィルタのタイプ（highpass, lowpass, bandpass, bandstop）
    #analog = False, True
    #output = 出力のタイプ(ba, sos, zpk)
    #fs = デジタルフィルタの場合、サンプリング周波数
    sos = scipy.signal.butter(N, Wn, btype, analog, output, fs)

    #sos = butterの戻り値
    #x = 対象の波形
    #axis = どの軸に沿ってフィルタをかけるか
    #padtype = パディングのタイプ？
    #padlen = パディングの長さ？
    x = scipy.signal.sosfiltfilt(sos, x, axis=-1, padtype='odd', padlen=None)
    return x
    


def STFT(sample_count, dt,file_name, Lf, noverlap=None):
    #Lf = 切り出す窓の長さ
    N = sample_count
    fs = 1/dt
    #df = pd.read_csv(file_name)

    s = np.loadtxt(file_name+'.txt')
    velocity_list = s
    Wn = 50#カットオフ周波数
    order = 4#次数
    filtered_data = butter_highpass_fillter(velocity_list, order, Wn, 'highpass', False, 'sos',fs)
    r_mm = 30
    #corrected_data = correct_data(file_name,filtered_data,r_mm,sample_count,dt)
    
    
    #text=df.to_string()

    #print(text)
    #text = text.split('\n')


    """
    for j in range(0,N,1):
        text[j] = text[j].split(";")
    text = text[0:N]
    s = [float(x[1]) for x in text]  

    
    #速度を変位に変換---
    velocity_list = s
    
    #台形法
    displacement = 0
    displacement_list = []
    displacement += (0 + velocity_list[0])*dt/2
    displacement_list.append(displacement)
    for j in range(1,sample_count,1):
        displacement += (velocity_list[j-1] + velocity_list[j])*dt/2
        displacement_list.append(displacement)
    
    s = displacement_list
    #---速度を変位に変換
    """
    #s = [float(x) for x in text]  

    #s=corrected_data
    periodograms = []
    
    if noverlap==None:
        noverlap = Lf//2
    l = sample_count
    win = np.hanning(Lf)
    Mf = Lf//2 + 1
    print(f"周波数データの点数：{Mf}")
    Nf = int(np.ceil((l-noverlap)/(Lf-noverlap)))-1
    print(f"窓数：{Nf}")
    S = np.empty([Mf, Nf], dtype=np.complex128)
    for n in (range(Nf)):
        S[:,n] = np.fft.rfft(s[(Lf-noverlap)*n:(Lf-noverlap)*n+Lf] * win, n=Lf, axis=0)
        periodogram = (np.abs(S[:,n]))**2
        periodograms.append(periodogram)
        S[0,n] = 0
    
     # スペクトル平均化 (Welch法の中核)
    # 収集した全てのピリオドグラムを周波数ビンごとに平均化する
    averaged_psd = np.mean(periodograms, axis=0) 
    
    # パワースペクトルをdBスケールに変換 (0の対数を避けるため微小値1e-18を加算)
    P_welch_db = 10 * np.log10(averaged_psd + 1e-18)

    freq_sp = np.fft.rfftfreq(Lf, dt)
    
    """
    S = S + 1e-18
    P = 20 * np.log10(np.abs(S))
    P = P - np.max(P) # normalization
    vmin = -150
    if np.min(P) > vmin:
        vmin = np.min(P)
    m = np.linspace(0, sample_count*dt, num=P.shape[1])
    k = np.linspace(0, fs/2, num=P.shape[0])
    plt.figure()
    plt.pcolormesh(m, k, P, cmap = 'jet', vmin=-150, vmax=0)
    plt.title("Spectrogram of Sound")
    plt.xlabel("time[s]")
    plt.ylabel("frequency[Hz]")
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(file_name+'_spectrogram.png')
    """
    
    S = S + 1e-18
    #P = 20 * np.log10(np.abs(S))      #振幅スペクトル
    P = 10 * np.log10((np.abs(S))**2) #パワースペクトル
    #P = P - np.max(P) # normalization
    #sp_abs = np.abs(S)
    sp_abs = P
    
    freq_sp = np.fft.rfftfreq(Lf, dt)
    freq_bottum = 50
    freq_upper = 600
    tm = np.linspace(0,dt*N,N)
    frame_start_indices = np.arange(Nf) * (Lf - noverlap)
    # 各フレームの中心時刻
    tm_sp = (frame_start_indices + Lf / 2) * dt

    vmin=(sp_abs[(freq_bottum <freq_sp) & (freq_sp < freq_upper), :]).min()
    vmax=(sp_abs[(freq_bottum <freq_sp) & (freq_sp < freq_upper), :]).max()
    #vmin = -100
    #vmax = 5

    #print((sp).shape)
    #print(type(sp_abs[1,1]))
    #print(f"min: {np.min(sp_abs)}")
    #print(f"max: {np.max(sp_abs)}")
    #print(f"mean: {np.mean(sp_abs)}")
    #sp_abs[sp_abs < 0.01] = 2
    #print((sp_abs).shape)

    #sp_abs = np.where(sp_abs is None,vmax,sp_abs)
    #sp_abs = np.where(sp_abs < np.float64(0.001),np.float64(random.uniform(0.001,0.02)),np.float64(sp_abs))


    
    #print((sp_abs).shape)


    #------------------------------------------------------------------------------
    # 解析結果の可視化
    figsize = (16, 9)
    dpi = 150
    fig = plt.figure(figsize=figsize, dpi=dpi)

    # --- 図の設定 (全体)
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
    plt.rcParams["font.size"] = 40
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['agg.path.chunksize'] = 10000  # チャンクサイズを増やす
    plt.rcParams['path.simplify_threshold'] = 0.12  # パス簡略化の閾値を増やす

    # 窓関数幅をプロット上部に記載
    #fig.text(0.10, 0.95, f't_wndw = {t_wndw} s, ')

    # プロット枠 (axes) の設定
    ax1 = fig.add_axes([0.15, 0.62, 0.70, 0.35])
    ax_sp1 = fig.add_axes([0.15, 0.12, 0.70, 0.35])
    cb_sp1 = fig.add_axes([0.87, 0.12, 0.02, 0.35])

    # 元データのプロット
    #ax1.set_xlim(tms, tme)
    ax1.set_xlim(0.0,1.3)
    ax1.set_xlabel('time [s]')
    ax1.tick_params(labelbottom=True)
    plt.tick_params(labelsize=20)
    ax1.set_ylabel('Displacement [m]')
    ax1.set_ylim(-0.00001,0.00001)#10μm、bensmaiaに合わせた
    #ax1.set_ylim(-0.075,0.01)
    nyquist = fs / 2
    cutoff = 100  # あなたが設定したいカットオフ周波数

    print(f"サンプリング周波数 fs: {fs} Hz")
    print(f"ナイキスト周波数 nyq: {nyquist} Hz")
    print(f"指定カットオフ cutoff: {cutoff} Hz")
    print(f"正規化周波数 Wn: {cutoff / nyquist}") # これが 1.0 を超えていませんか？
    #ax1.plot(tm, velocity_list, c='black')
    filtered_data = velocity_list#フィルタをかけない場合、これの下がハイパスをかける場合
    Wn = 50#カットオフ周波数
    order = 4#次数
    filtered_data = butter_highpass_fillter(velocity_list, order, Wn, 'highpass', False, 'sos',fs)

    ax1.plot(tm, filtered_data, c='black')

    # スペクトログラムのプロット
    ax_sp1.set_xlim(0.0, 1.3)
    ax_sp1.set_xlabel('time [s]')
    ax_sp1.tick_params(labelbottom=True)
    plt.tick_params(labelsize=20)
    ax_sp1.set_ylim(freq_bottum, freq_upper)
    ax_sp1.set_ylabel('Frequency\n[Hz]')
    
    norm = mpl.colors.Normalize(vmin, vmax)
    print("min = "+ str(vmin))
    print("max = "+ str(vmax))
    #norm = mpl.colors.Normalize(0, 10)
    cmap = mpl.cm.jet
    #cmap = mpl.cm.viridis
    #cmap = mpl.cm.gray
    
    ax_sp1.contourf(tm_sp, freq_sp, (sp_abs), 
                     norm=norm,
                     levels=512, 
                     cmap=cmap)
    

    ax_sp1.text(0.99, 0.97, "spectrogram", color='white', ha='right', va='top',
                  path_effects=[path_effects.Stroke(linewidth=2, foreground='black'),
                                path_effects.Normal()], 
                  transform=ax_sp1.transAxes)

    mpl.colorbar.ColorbarBase(cb_sp1, cmap=cmap,
                              
                              norm=norm,
                              orientation="vertical",
                              label='Amplitude')
    
    #ax_sp1.plot(freq_sp, P_welch_db, c='blue') # PSDを線グラフでプロット

    #plt.gray
    

    plt.savefig(file_name+f'_displacement_spectrogram_{freq_bottum}-{freq_upper}.png')
    #plt.show()
    #plt.savefig(file_name+f'_displacement_periodogram_{freq_bottum}-{freq_upper}.png')


def compute_welch_psd_and_plot(file_name, sampling_rate, window_length, overlap_samples=None):
    
    signal_data_np = np.loadtxt(file_name+'.txt')
    Wn = 50#カットオフ周波数
    order = 4#次数
    signal_data_np = butter_highpass_fillter(signal_data_np, order, Wn, 'highpass', False, 'sos',sampling_rate)
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
    print(f"  Nyquist Frequency (Mf): {num_freq_bins}")

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
        periodogram = (np.abs(fft_result))**2 # 各セグメントのパワースペクトル（ピリオドグラム）を計算
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
    ax1.set_ylabel('Displacement [m]')
    
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
    ax_psd.set_xlabel('Frequency [Hz]')
    ax_psd.tick_params(labelbottom=True, labelsize=16)
    ax_psd.set_ylabel('Power Spectral Density [dB]')
    ax_psd.set_title("Power Spectral Density (Welch's Method)")
    
    # PSDのY軸範囲は自動調整が基本だが、必要に応じて固定値も設定可能 (例: ax_psd.set_ylim(-150, 0))

    ax_psd.plot(freq_axis, P_welch_db, c='blue') # PSDを線グラフでプロット

    
    # 出力ディレクトリが存在しない場合は作成
    #os.makedirs(output_dir, exist_ok=True)
    #output_full_path = os.path.join(output_dir, f"{base_filename}.png")
    
    output_full_path = file_name+'_welch_psd.png'
    plt.savefig(output_full_path)
    #plt.show()



def convertVelocity2Displacement(file_name, sample_count, dt):
    df = []
    df = pd.read_csv(file_name)    
    text=df.to_string()

    text = text.split('\n')
    
    for j in range(0,sample_count,1):
        text[j] = text[j].split(";")
    text = text[0:sample_count]
    velocity_list = [float(x[1]) for x in text]
    plt.figure()
    plt.xlabel('time [s]')
    plt.ylabel('Velocity [m/s]')
    #plt.ylim(-0.011,0.011)
    #plt.tick_params(labelsize=45)
    plt.subplots_adjust(0.2,0.15,0.97,0.95)
    t = np.linspace(0,dt*sample_count,sample_count)
    plt.plot(t, velocity_list) # 入力信号
    plt.savefig(file_name+'_velocity.png')

    displacement = 0
    displacement_list = []

    displacement += (0 + velocity_list[0])*dt/2
    displacement_list.append(displacement)
    for j in range(1,sample_count,1):
        displacement += (velocity_list[j-1] + velocity_list[j])*dt/2
        displacement_list.append(displacement)
    
    plt.figure()
    plt.xlabel('time [s]')
    plt.ylabel('displacement [m]')
    #plt.ylim(-0.011,0.011)
    #plt.tick_params(labelsize=45)
    plt.subplots_adjust(0.2,0.15,0.97,0.95)
    #t = np.linspace(0,dt*sample_count,sample_count)
    plt.plot(t, displacement_list) # 入力信号
    plt.savefig(file_name+'_displacement.png')

def fftplt_indiv_endless(data, sample_count, dt):
    #rootdir = 'C:/Users/yuto/Documents/optotune/measuredData/'

    N = sample_count

    text = data.split('\n')
    
    for j in range(0,sample_count,1):
        text[j] = text[j].split(";")
    text = text[0:sample_count]
    velocity_list = [float(x[1]) for x in text]
    displacement = 0
    displacement_list = []

    displacement += (0 + velocity_list[0])*dt/2
    displacement_list.append(displacement)
    for j in range(1,sample_count,1):
        displacement += (velocity_list[j-1] + velocity_list[j])*dt/2
        displacement_list.append(displacement)

    X=np.fft.fft(displacement_list)

    X[0] = 0
            
    f = np.fft.fftfreq(N,dt)

    plt.xlabel('Frequency [Hz]')
    plt.xlim(f[0],600)
    plt.ylabel('Amplitude')
    plt.ylim(0,0.3)
    plt.subplots_adjust(0.2,0.15,0.97,0.95)
    plt.plot(f[0:int(N/2)],np.abs((X)/np.sqrt(N))[0:int(N/2)])


"""
if __name__ == "__main__":
    sample_count = 2**18
    dt = 1/218750
    rootDir = 'C:/Users/yuto/Documents/system_python/data/LDVdata/'
    file_name = "20250715_171108(ミラーなし波長板あり).txt"
    #file_name1 = "20250703_170110.txt"
    STFT(sample_count, dt, rootDir+file_name, 2**15)
    #STFT(sample_count, dt, rootDir+file_name1, 2**15)
    fftplt_indiv(rootDir+file_name, sample_count, dt)

    N = sample_count
    fs = 1/dt
    df = pd.read_csv(rootDir+file_name)    
    text=df.to_string()

    text = text.split('\n')
    
    for j in range(0,N,1):
        text[j] = text[j].split(";")
    text = text[0:N]
    velocity_data_from_file = [float(x[1]) for x in text] 
    # --- 速度から変位への変換 (台形法) ---
    # ユーザーの元のコードの台形積分ロジックを再現
    displacement = 0.0
    displacement_list_temp = []
    
    if len(velocity_data_from_file) > 0:
        # 最初の点を特別扱い (元のコードの `displacement += (0 + velocity_list[0])*dt/2` に対応)
        # 厳密な累積台形積分は SciPy の `integrate.cumulative_trapezoid` がより適切だが、元のロジックを優先
        displacement += (0.0 + velocity_data_from_file[0]) * dt / 2
        displacement_list_temp.append(displacement)
        # 残りの点をループで積分
        for j in range(1, len(velocity_data_from_file)):
            displacement += (velocity_data_from_file[j-1] + velocity_data_from_file[j]) * dt / 2
            displacement_list_temp.append(displacement)
    
    # 積分結果をNumPy配列に変換し、これがWelch法への入力となる
    displacement_data_np = np.array(displacement_list_temp, dtype=np.float64)
    velocity_data_np = np.array(velocity_data_from_file, dtype=np.float64)
    window_length = 2**16
    overlap_samples = window_length//2
    compute_welch_psd_and_plot(displacement_data_np, 1/dt,window_length, overlap_samples, rootDir+file_name, '_welch_psd_dis')
    compute_welch_psd_and_plot(velocity_data_np, 1/dt,window_length, overlap_samples, rootDir+file_name, '_welch_psd_vel')
    #convertVelocity2Displacement(rootDir+file_name, sample_count, dt)
    #convertVelocity2Displacement(rootDir+file_name1, sample_count, dt)
"""

#周波数空間ではなく、速度-時間データを機械学習で接触判定、分類もあり


if __name__ == "__main__":
    sample_count = 2**17
    dt = 1/218750
    window_length = 2**14
    rootDir = 'C:/Users/yuto/Documents/system_python/data/LDVdata/'
    file_name = "20251208_1804_3"
    STFT(sample_count, dt, rootDir+file_name, 2**14)
    fftplt_indiv(rootDir+file_name, sample_count, dt)
    compute_welch_psd_and_plot(rootDir+file_name, 1/dt, window_length, overlap_samples=None)