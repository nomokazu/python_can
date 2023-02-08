import msg
import can
import time

#バス接続
bus = can.interface.Bus(bustype='socketcan', channel="slcan0", bitrate=500000, app_name='python-can')


for crc in range(256+1):
    # Steering_Commandメッセージの作成
    message = msg.Steering_Command(crc)
    # メッセージののパラメータの指定
    message.setDataFromInt(1, 240, 100)
    # CAN
    message.toData()
    message.view()
    #送信データ
    can_msg = can.Message(arbitration_id = message.msg_id, data= message.data, is_extended_id = False)

    #送信
    task = bus.send_periodic(can_msg, 0.05)
    assert isinstance(task, can.CyclicSendTaskABC)

    time.sleep(0.2)
    task.stop()
    print("stopped cyclic send")