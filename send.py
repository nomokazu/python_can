import msg
import can
import time

#バス接続
bus = can.interface.Bus(bustype='socketcan', channel="slcan0", bitrate=500000, app_name='python-can')

# Steering_Commandメッセージの作成
message = msg.Steering_Command()

# メッセージののパラメータの指定
message.setDataFromInt(1, 240, 100)

# CAN
message.toData()
message.view()

#送信データ
can_msg = can.Message(arbitration_id = message.msg_id, data= message.data, is_extended_id = False)

# 送信
# 必ず 20ミリ秒以下で送信する
task = bus.send_periodic(can_msg, 0.01)
assert isinstance(task, can.CyclicSendTaskABC)

time.sleep(0.2)
task.stop()
print("stopped cyclic send")