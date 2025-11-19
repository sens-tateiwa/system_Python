class ButtonWindow:
    def __init__(self,cameraGrabingFinish):
        self.root = None

        self.cameraFinishFlag = cameraGrabingFinish

    def on_button1_click(self):
        print("ボタン1クリック")
        self.cameraFinishFlag.set()

    def on_button2_click(self):
        print("ボタン2クリック")

    def run(self):
        import tkinter as tk
        self.root = tk.Tk()
        self.root.title("test")
        button1 = tk.Button(self.root, text="please click1",command=self.on_button1_click)
        button1.pack()

        button2 = tk.Button(self.root, text="please click2",command=self.on_button2_click)
        button2.pack()

        self.root.mainloop()


