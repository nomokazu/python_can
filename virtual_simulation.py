import can
import msg

bus1 = can.interface.Bus('test', bustype='virtual', preserve_timestamps=True)
bus2 = can.interface.Bus('test', bustype='virtual')

msg1 = can.Message(timestamp=1639740470.051948, arbitration_id=0x502, data=[0x00,0x00,0x01,0x01,0x5A,0x01,0xF4,0xF0])

# Messages sent on bus1 will have their timestamps preserved when received
# on bus2
bus1.send(msg1)
msg2 = bus2.recv()

print(msg2)
print(msg2.data)

messageInstance = msg.Msg_Steering_Report()
messageInstance.setDataFromCANMessage(msg2.data)
messageInstance.view()

messageInstance2 = msg.Msg_Steering_Report()
messageInstance2.setDataFromInt(0,0,1,346,500,240)
messageInstance2.view()

assert msg1.arbitration_id == msg2.arbitration_id
assert msg1.data == msg2.data
assert msg1.timestamp == msg2.timestamp

# Messages sent on bus2 will not have their timestamps preserved when
# received on bus1
bus2.send(msg1)
msg3 = bus1.recv()

assert msg1.arbitration_id == msg3.arbitration_id
assert msg1.data == msg3.data
assert msg1.timestamp != msg3.timestamp