import controlMirror
class ButtonWindow:
    def __init__(self,MirrorAngle_queue,prepareLaserPosition,cameraGrabingFinish):
        self.root = None
        self.MirrorAngle_queue = MirrorAngle_queue
        self.X = 0
        self.Y = 0
        self.prepareLaserPosition = prepareLaserPosition
        self.cameraFinishFlag = cameraGrabingFinish

    def on_button_start_click(self):
        print("開始")
        self.prepareLaserPosition.put((self.X,self.Y))

    def on_button_end_click(self):
        print("終了")
        self.cameraFinishFlag.set()

    def on_button_up_click(self):
        #print("上クリック")
        self.Y += 0.03
        #controlMirror.changeAngle(self.X,self.Y,self.mre2)
        self.MirrorAngle_queue.put((self.X,self.Y))

    def on_button_left_click(self):
        #print("左クリック")
        self.X -= 0.03
        #controlMirror.changeAngle(self.X,self.Y,self.mre2)
        self.MirrorAngle_queue.put((self.X,self.Y))

    def on_button_right_click(self):
        #print("右クリック")
        self.X += 0.03
        #controlMirror.changeAngle(self.X,self.Y,self.mre2)
        self.MirrorAngle_queue.put((self.X,self.Y))

    def on_button_down_click(self):
        #print("下クリック")
        self.Y -= 0.03
        #controlMirror.changeAngle(self.X,self.Y,self.mre2)
        self.MirrorAngle_queue.put((self.X,self.Y))


    def run(self):
        import tkinter as tk
        self.root = tk.Tk()
        self.root.title("test")

        #windowの位置を調整
        window_width = 180
        window_height = 280
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_pos = screen_width - window_width - 30
        y_pos = 0 + 30

        self.root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        font_style = ("Arial", 10, "bold")

        button_up = tk.Button(self.root, text="↑",command=self.on_button_up_click, font=font_style, width=5, height=2)
        button_up.grid(row=0, column=1, padx=5, pady=5)

        button_left = tk.Button(self.root, text="←",command=self.on_button_left_click, font=font_style, width=5, height=2)
        button_left.grid(row=1, column=0, padx=5, pady=5)

        button_right = tk.Button(self.root, text="→",command=self.on_button_right_click, font=font_style, width=5, height=2)
        button_right.grid(row=1, column=2, padx=5, pady=5)

        button_down = tk.Button(self.root, text="↓",command=self.on_button_down_click, font=font_style, width=5, height=2)
        button_down.grid(row=2, column=1, padx=5, pady=5)

        button_start = tk.Button(self.root, text="開始",command=self.on_button_start_click, font=font_style, width=15, height=2)
        button_start.grid(row=3, column=0, columnspan=3, pady=5)

        button_end = tk.Button(self.root, text="終了",command=self.on_button_end_click, font=font_style, width=15, height=2)
        button_end.grid(row=4, column=0, columnspan=3, pady=5)

        self.root.mainloop()


