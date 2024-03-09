# Requirement

```
pip3 install python-can
pip3 install python-can-remote
pip3 install pygame
```

# msg.py

それぞれのCANメッセージのクラスが用意されている。
すべてのクラスは、以下のメソッドを持つ
- setDataFromCANMessage
CANメッセージから、メッセージのパラメータにパースする

- setDataFromInt
変数を受け取り、メッセージごとのパラメータにセットする

- dataParser
メッセージごとのパラメータにパースする（まだ可読状態ではない）

- toInt
可読状態ではないパラメータをInt型に変換して可読状態にする

- view
メッセージの各パラメータを表示する

- toData
メッセージごとのパラメータから、CANメッセージのデータに変換する

## 変数 -> CAN　のときの処理の流れ

1. setDataFromInt
2. toData

## CAN -> パラメータ

1. setDataFromCANMessage
2. （内部的に）dataParser
3. （内部的に）toInt
4. toData

# handle_controller.py の使い方（リモート版)

0. sender.py の接続先を以下に修正する

なお、「ws://localhost:54701/」は python-can-remote のサーバIPに合わせる

```
self.bus = can.interface.Bus('ws://localhost:54701/', bustype='remote', preserve_timestamps=True)
```

1. python-can-remote を起動する

```
python -m can_remote --interface=virtual --channel=0 --bitrate=500000
```

2. ハンコンの値を取得して、CANに流す

```
python3 handle_controller.py
```

3. CANの値を確認する

```
python3 python-can-remote_viewer.py
```

# PIXKITでCANインタフェースをopenする方法

Lawicel CAN を USB接続した状態で、以下のコマンドを実行するとCANインタフェースを python-can で制御可能になる

```
sudo slcand -o -s6 -t hw  /dev/ttyUSB0 
sudo ip link set up can0
```

なお、Lawicel CAN をつなぎ直した場合は、 /dev/ttyUSBX の X が 0 からインクリメントされるかもしれないので注意。

以下のコマンドを実行して、CANが流れているかを確認できる
```
candump slcan0
```

# handle_controller.py の使い方（PIXKIT版)

0. sender.py の接続先を以下に修正する
```
self.bus = can.interface.Bus(bustype='socketcan', channel="slcan0", bitrate=500000, app_name='python-can')
```

1. 「PIXKITでCANインタフェースをopenする方法」に従って、CANを読み書きできるようにする

2. ハンコンの値を取得して、CANに流す

```
python3 handle_controller.py
```

3. PIXKITのコントローラーを「seld driving」に変更して、CANの制御を受け付けるようにする

# エミュレーションの方法

このエミュレーションでは、ハンドルコントロールによる操作をGUIソフトウェアで行える。
また、送られたコマンドを元にPIXKITからのフィードバックメッセージも送信される。（ID : 500, 501, 502）

1. sender.py のバスをリモートにする

例
```
self.bus = can.interface.Bus('ws://localhost:54701/', bustype='remote', preserve_timestamps=True)
```

2. python-can-remoteを立ち上げる
```
python -m can_remote --interface=virtual --channel=0 --bitrate=500000
```

3. ハンドルのエミュレーションプログラムを立ち上げる
```
python3 emulate_handle.py
```

4. PIXKITのエミュレーションプログラムを立ち上げる
```
python3 emulate_feedback_generator.py
```