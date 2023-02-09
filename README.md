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

# handle_controller.py の使い方

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