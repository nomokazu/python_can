import pygame
from pygame.locals import *
import os
import sys
import sender
# from ..python_can import sender

# 参考 : https://note.com/npaka/n/n7b799597e706

# ジョイスティックの初期化
pygame.joystick.init()
try:
    # ジョイスティックインスタンスの生成
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print('ジョイスティックの名前:', joystick.get_name())
    print('ボタン数 :', joystick.get_numbuttons())
except pygame.error:
    print('ジョイスティックが接続されていません')

# pygameの初期化
pygame.init()

# 画面の生成
screen = pygame.display.set_mode((320, 320))

# ループ
active = True
handleControllerCommand = sender.HandleControllerCommand()
while active:
    # イベントの取得
    for e in pygame.event.get():
        # 終了ボタン
        if e.type == QUIT:
            active = False

        # ジョイスティックのボタンの入力
        if e.type == pygame.locals.JOYAXISMOTION:
            # print を入れると、CANの送信処理が正しく走らなくなるのでデバッグ時以外はprint を消す
            # print('十時キー:', joystick.get_axis(0), joystick.get_axis(1), joystick.get_axis(2), joystick.get_axis(3))
            
            # ハンドルは軸0
            handle = joystick.get_axis(0)
            
            # ブレーキペダルが軸3
            # 全く踏んでいない状態が 1 で、完全に踏むと 0 になる ので、それを
            # 全く踏んでいない状態 : 0 -> 完全に踏むと 1 に補正している。
            break_pedal_raw = 1- joystick.get_axis(3)
            
            # アクセルペダルが軸2
            # 全く踏んでいない状態が 1 で、完全に踏むと -1 になるので、それを
            # 全く踏んでいない状態 : 0 -> 完全に踏むと 1 に補正している。
            accel_pedal = ((-1) * (joystick.get_axis(2)) + 1 ) / 2
            brake_pedal = 0
            
            # ブレーキペダルがごくわずかにしか踏まれていないときは、踏んでいない状態とするようにする
            if break_pedal_raw > 0.02:
                brake_pedal = break_pedal_raw
            handleControllerCommand.setHandleControllerCommandSend(handle, accel_pedal, brake_pedal)
            handleControllerCommand.startCanSend()
            if handleControllerCommand.sendFlag == False:
                handleControllerCommand.sendFlag = True