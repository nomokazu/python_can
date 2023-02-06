import can
import msg

bus1 = can.interface.Bus('test', bustype='virtual', preserve_timestamps=True)
bus2 = can.interface.Bus('test', bustype='virtual')

#--------------Steering_Command---------------------
# Steering_Commandメッセージの作成
message = msg.Steering_Command()
# メッセージのパラメータの指定
message.setDataFromInt(0, 100, 400)
# CAN
message.toData()
message.view()

#送信データ
can_msg = can.Message(arbitration_id = message.msg_id, data= message.data, is_extended_id = False)

bus1.send(can_msg)
msg2 = bus2.recv()

print(msg2)
print(msg2.data)


#--------------Brake_Command-----------------------
# Brake_Commandメッセージの作成
message = msg.Brake_Command()
# メッセージのパラメータの指定
message.setDataFromInt(0,3,20)
# CAN
message.toData()
message.view()

#送信データ
can_msg = can.Message(arbitration_id = message.msg_id, data= message.data, is_extended_id = False)

bus1.send(can_msg)
msg2 = bus2.recv()

print(msg2)
print(msg2.data)

#------------------ Throttle_Command ---------------------

# Throttle_Commandメッセージの作成
message = msg.Throttle_Command()
# メッセージのパラメータの指定
message.setDataFromInt(0,5,30,5)
# CAN
message.toData()
message.view()

#送信データ
can_msg = can.Message(arbitration_id = message.msg_id, data= message.data, is_extended_id = False)

bus1.send(can_msg)
msg2 = bus2.recv()

print(msg2)
print(msg2.data)