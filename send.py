import msg
import can

#バス接続
bus = can.interface.Bus(bustype='virtual', channel=0, bitrate=500000, app_name='python-can')

# Steering_Commandメッセージの作成
message = msg.Steering_Command()
# メッセージののパラメータの指定
message.setDataFromInt(0, 100, 400)
# CAN
message.toData()

#送信データ
can_msg = can.Message(arbitration_id = message.msg_id, data= message, is_extended_id = False)

#送信
task = bus.send_periodic(can_msg, 1)
assert isinstance(task, can.CyclicSendTaskABC)

time.sleep(10)
task.stop()
print("stopped cyclic send")