import tkinter as tk
import os
import sys
from python_can import sender
import threading

steering = 0
brake_var = 0
throttle_var = 0

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)

        self.master.title("Scaleの作成")     # ウィンドウタイトル

        #---------------------------------------------------------------
        # Scaleの作成

        # Scale（デフォルトで作成）
        # scaleV = tk.Scale( self.master)
        # scaleV.pack(side = tk.RIGHT)

        # Scale（オプションをいくつか設定）
        l = tk.Label(
            root,
            text="左    ステアリング    右",   #表示文字
            )
        l.pack()

        # スライドバー : https://imagingsolution.net/program/python/tkinter/scale_trackbar/
        self.scal_steering_var = tk.DoubleVar()
        scaleH_steering = tk.Scale( self.master, 
                    variable = self.scal_steering_var, 
                    command = self.slider_scroll,
                    orient=tk.HORIZONTAL,   # 配置の向き、水平(HORIZONTAL)、垂直(VERTICAL)
                    length = 300,           # 全体の長さ
                    width = 20,             # 全体の太さ
                    sliderlength = 20,      # スライダー（つまみ）の幅
                    from_ = -1,            # 最小値（開始の値）
                    to = 1,               # 最大値（終了の値）
                    resolution=0.1,         # 変化の分解能(初期値:1)
                    tickinterval=50         # 目盛りの分解能(初期値0で表示なし)
                    )
        scaleH_steering.pack()

        l = tk.Label(
            root,
            text="踏んでない<-    ブレーキ    ->踏んでる",   #表示文字
            )
        l.pack()

        #---------------------------------------------------------------
        self.scal_brake_var = tk.DoubleVar()
        scaleH_brake = tk.Scale( self.master, 
                    variable = self.scal_brake_var, 
                    command = self.slider_scroll,
                    orient=tk.HORIZONTAL,   # 配置の向き、水平(HORIZONTAL)、垂直(VERTICAL)
                    length = 300,           # 全体の長さ
                    width = 20,             # 全体の太さ
                    sliderlength = 20,      # スライダー（つまみ）の幅
                    from_ = 1,            # 最小値（開始の値）
                    to = 0,               # 最大値（終了の値）
                    resolution=0.1,         # 変化の分解能(初期値:1)
                    tickinterval=50         # 目盛りの分解能(初期値0で表示なし)
                    )
        scaleH_brake.pack()


        l = tk.Label(
            root,
            text="踏んでない<-    スロットル    ->踏んでる",   #表示文字
            )
        l.pack()

        self.scal_throttle_var = tk.DoubleVar()
        scaleH_throttle = tk.Scale( self.master, 
                    variable = self.scal_throttle_var, 
                    command = self.slider_scroll,
                    orient=tk.HORIZONTAL,   # 配置の向き、水平(HORIZONTAL)、垂直(VERTICAL)
                    length = 300,           # 全体の長さ
                    width = 20,             # 全体の太さ
                    sliderlength = 20,      # スライダー（つまみ）の幅
                    from_ = 1,            # 最小値（開始の値）
                    to = -1,               # 最大値（終了の値）
                    resolution=0.1,         # 変化の分解能(初期値:1)
                    tickinterval=50         # 目盛りの分解能(初期値0で表示なし)
                    )
        scaleH_throttle.pack()



    def slider_scroll(self, event=None):
        '''スライダーを移動したとき'''
        print(str(self.scal_steering_var.get()))
        print(str(self.scal_brake_var.get()))
        print(str(self.scal_throttle_var.get()))


def can_sender():
    global steering
    global brake_var
    global throttle_var
    # どういった操作を行うかのシナリオの定義
    emulation_scenrio = {"axi0" : steering, "axi2" : brake_var, "axi3" : throttle_var}

    # ループ
    active = True
    handleControllerCommand = sender.HandleControllerCommand()
    while active:

        # print を入れると、CANの送信処理が正しく走らなくなるのでデバッグ時以外はprint を消す
        # print('十時キー:', joystick.get_axis(0), joystick.get_axis(1), joystick.get_axis(2), joystick.get_axis(3))
        
        # ハンドルは軸0
        handle = emulation_scenrio["axi0"]
        
        # ブレーキペダルが軸3
        # 全く踏んでいない状態が 1 で、完全に踏むと 0 になる ので、それを
        # 全く踏んでいない状態 : 0 -> 完全に踏むと 1 に補正している。
        break_pedal_raw = 1- emulation_scenrio["axi3"]
        
        # アクセルペダルが軸2
        # 全く踏んでいない状態が 1 で、完全に踏むと -1 になるので、それを
        # 全く踏んでいない状態 : 0 -> 完全に踏むと 1 に補正している。
        accel_pedal = ((-1) * (emulation_scenrio["axi2"]) + 1 ) / 2
        brake_pedal = 0
        
        # ブレーキペダルがごくわずかにしか踏まれていないときは、踏んでいない状態とするようにする
        if break_pedal_raw > 0.02:
            brake_pedal = break_pedal_raw
        handleControllerCommand.setHandleControllerCommandSend(handle, accel_pedal, brake_pedal)
        handleControllerCommand.startCanSend()
        if handleControllerCommand.sendFlag == False:
            handleControllerCommand.sendFlag = True

if __name__ == "__main__":
    thread1 = threading.Thread(target=can_sender)
    thread1.start()
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()