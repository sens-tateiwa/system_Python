import cv2
import numpy as np
def create_real_velocity():
    # ==========================================
    # 【重要】ここを使用するモニターに合わせて書き換えてください:ノートPCのサイズに設定
    # ==========================================
    MONITOR_WIDTH_MM = 310.0   # 画面の物理的な横幅 (ミリメートル) ※定規で測る
    RESOLUTION_X = 1920        # 画面の横解像度 (ピクセル)
    RESOLUTION_Y = 1080        # 画面の縦解像度 (ピクセル)

    TARGET_SPEED_MM_S = 80  # 作りたい速度 (mm/s)
    FPS = 60                   # フレームレート (60推奨)
    DURATION_SEC = 5.0         # 動画の長さ (秒)
    # ==========================================

    # 1mmあたりのピクセル数を計算 (Pixels Per Millimeter)
    pixels_per_mm = RESOLUTION_X / MONITOR_WIDTH_MM

    # 目標速度をピクセル単位に変換
    speed_px_per_s = TARGET_SPEED_MM_S * pixels_per_mm
    speed_px_per_frame = speed_px_per_s / FPS

    print(f"モニター設定: 幅 {MONITOR_WIDTH_MM}mm / 解像度 {RESOLUTION_X}px")
    print(f"変換係数: 1mm = {pixels_per_mm:.2f} pixel")
    print(f"移動速度: {TARGET_SPEED_MM_S} mm/s -> {speed_px_per_s:.2f} px/s")

    # 動画保存の準備
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    rootDir = 'C:/Users/yuto/Documents/system_python'
    filename = f'move_{TARGET_SPEED_MM_S}mm_s.mp4'
    out = cv2.VideoWriter(rootDir+"/"+filename, fourcc, FPS, (RESOLUTION_X, RESOLUTION_Y))

    # 初期位置 (画面左外からスタートさせたい場合はマイナス値を設定)
    pos_x = 0.0
    pos_y = RESOLUTION_Y // 2

    # 色設定 (BGR)
    bg_color = (0, 0, 0)       # 黒背景
    point_color = (0, 0, 255)  # 赤い点
    ruler_color = (255, 255, 255) # 白い定規

    total_frames = int(DURATION_SEC * FPS)

    print("動画生成中...")

    for i in range(total_frames):
        # 背景塗りつぶし
        frame = np.zeros((RESOLUTION_Y, RESOLUTION_X, 3), dtype=np.uint8)
        
        # --- 1. 点の移動 ---
        if  pos_x >= RESOLUTION_X:
            pos_x = 0
        pos_x += speed_px_per_frame
        
        # 画面内にある時だけ描画
        if -50 <= pos_x <= RESOLUTION_X + 50:
            cv2.circle(frame, (int(pos_x), int(pos_y)), 15, point_color, -1)

        # --- 2. サイズ確認用定規の描画 (画面下部) ---
        # 実際の定規を画面に当てて、この白い線がぴったり10cmなら速度も正しいです
        ruler_len_mm = 100.0 # 100mm = 10cm
        ruler_len_px = int(ruler_len_mm * pixels_per_mm)
        
        ruler_start_x = 50
        ruler_y = RESOLUTION_Y - 50
        
        # 10cmの線
        cv2.line(frame, (ruler_start_x, ruler_y), (ruler_start_x + ruler_len_px, ruler_y), ruler_color, 2)
        # 目盛り (始点と終点)
        cv2.line(frame, (ruler_start_x, ruler_y-10), (ruler_start_x, ruler_y+10), ruler_color, 2)
        cv2.line(frame, (ruler_start_x + ruler_len_px, ruler_y-10), (ruler_start_x + ruler_len_px, ruler_y+10), ruler_color, 2)
        
        # テキスト
        cv2.putText(frame, "Check: 100mm (10cm)", (ruler_start_x, ruler_y - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, ruler_color, 2)
        
        # 速度表示
        info_text = f"Speed: {TARGET_SPEED_MM_S} mm/s"
        cv2.putText(frame, info_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

        out.write(frame)

    out.release()
    print(f"完了: {filename} を保存しました。")
    print("【注意】再生時は必ず「全画面表示(100%ズーム)」にしてください。")


if __name__ == "__main__":
    create_real_velocity()