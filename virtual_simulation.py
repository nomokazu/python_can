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

message2 = msg.Steering_Command()
message2.setDataFromCANMessage(msg2.data)
message2.toData()
message2.view()

print(message.data)
print(message2.data)
print(message.data==message2.data)


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

message2 = msg.Brake_Command()
message2.setDataFromCANMessage(msg2.data)
message2.toData()
message2.view()

print(message.data)
print(message2.data)
print(message.data==message2.data)


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

message2 = msg.Throttle_Command()
message2.setDataFromCANMessage(msg2.data)
message2.toData()
message2.view()


print(message.data)
print(message2.data)
print(message.data==message2.data)


#--------------Steering_Report---------------------
message = msg.Steering_Report()
message.setDataFromInt(1,0,1,200,100,100)
message.toData()
message.view()

#送信データ
can_msg = can.Message(arbitration_id = message.msg_id, data= message.data, is_extended_id = False)

bus1.send(can_msg)
msg2 = bus2.recv()

print(msg2)
print(msg2.data)

message2 = msg.Steering_Report()
message2.setDataFromCANMessage(msg2.data)
message2.toData()
message2.view()

print(message.data)
print(message2.data)
print(message.data==message2.data)

#--------------Brake_Report---------------------
message = msg.Brake_Report()
message.setDataFromInt(1, 0, 0, 20)
message.toData()
message.view()

#送信データ
can_msg = can.Message(arbitration_id = message.msg_id, data= message.data, is_extended_id = False)

bus1.send(can_msg)
msg2 = bus2.recv()

print(msg2)
print(msg2.data)

message2 = msg.Brake_Report()
message2.setDataFromCANMessage(msg2.data)
message2.toData()
message2.view()

print(message.data)
print(message2.data)
print(message.data==message2.data)


#--------------Throttle_Report---------------------
message = msg.Throttle_Report()
message.setDataFromInt(1, 0, 1, 100)
message.toData()
message.view()

#送信データ
can_msg = can.Message(arbitration_id = message.msg_id, data= message.data, is_extended_id = False)

bus1.send(can_msg)
msg2 = bus2.recv()

print(msg2)
print(msg2.data)

message2 = msg.Throttle_Report()
message2.setDataFromCANMessage(msg2.data)
message2.toData()
message2.view()

print(message.data)
print(message2.data)
print(message.data==message2.data)
