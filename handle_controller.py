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
            print('十時キー:', joystick.get_axis(0), joystick.get_axis(1))
            handle = joystick.get_axis(0)
            pedal = joystick.get_axis(1)
            accel_pedal = 0
            brake_pedal = 0
            if pedal < 0:
                accel_pedal = abs(pedal)
            elif pedal > 0.02:
                brake_pedal = pedal
            handleControllerCommand.setHandleControllerCommandSend(handle, accel_pedal, brake_pedal)
            handleControllerCommand.startCanSend()
            print("start")