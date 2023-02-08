# Requirement

```
pip3 install python-can
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
