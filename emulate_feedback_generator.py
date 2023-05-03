import can
# from python_can import msg
import msg
import time
import threading

# bus1 = can.interface.Bus('test', bustype='virtual', preserve_timestamps=True)
# bus2 = can.interface.Bus('test', bustype='virtual')
bus = can.Bus('http://localhost:54701/', bustype='remote', bitrate=500000, receive_own_messages=True)

counter = 0

command_Steer_AngleTarget = None
command_Brake_Pedal_Target = None
command_Drive_ThrottlePedalTarget = None

command_Steer_AngleSpeed = None

timer = 0

can_msg_steering_Report = None
can_msg_brake_Report = None
can_msg_throttle_Report = None

def can_sender():
    global bus
    global can_msg_steering_Report
    global can_msg_brake_Report
    global can_msg_throttle_Report

    while True:
        if can_msg_steering_Report != None and can_msg_brake_Report != None and can_msg_throttle_Report != None:
            bus.send(can_msg_steering_Report)
            bus.send(can_msg_brake_Report)
            bus.send(can_msg_throttle_Report)
            time.sleep(0.01)

if __name__ == "__main__":
    thread1 = threading.Thread(target=can_sender)
    thread1.start()

    while True:
        counter = counter + 1
        receiveCanMsg = bus.recv()

        # コマンドの受信関連処理
        if receiveCanMsg.arbitration_id == 0x102:
            message2 = msg.Steering_Command()
            message2.setDataFromCANMessage(receiveCanMsg.data)
            message2.toData()
            command_Steer_AngleTarget = message2.Steer_AngleTarget
            command_Steer_AngleSpeed = message2.Steer_AngleSpeed

        elif receiveCanMsg.arbitration_id == 0x101:
            message2 = msg.Brake_Command()
            message2.setDataFromCANMessage(receiveCanMsg.data)
            message2.toData()
            command_Brake_Pedal_Target = message2.Brake_Pedal_Target
        
        elif receiveCanMsg.arbitration_id == 0x100:
            message2 = msg.Throttle_Command()
            message2.setDataFromCANMessage(receiveCanMsg.data)
            message2.toData()
            command_Drive_ThrottlePedalTarget = message2.Drive_ThrottlePedalTarget
        
        # 受信したコマンドの受信の表示
        if counter % 100 == 0:
            counter = 1
            print("Steer_AngleTarget : " + str(command_Steer_AngleTarget))
            print("Brake_Pedal_Target : " + str(command_Brake_Pedal_Target))
            print("Drive_ThrottlePedalTarget : " + str(command_Drive_ThrottlePedalTarget))

        # report メッセージの生成処理

        # すべての command を受信していたら
        if command_Steer_AngleTarget != None and command_Brake_Pedal_Target != None and command_Drive_ThrottlePedalTarget != None and command_Steer_AngleSpeed != None:
            steering_Report = msg.Steering_Report()
            brake_Report = msg.Brake_Report()
            throttle_Report = msg.Throttle_Report()

            # コマンドの情報から、reportを生成する
            steering_Report.setDataFromInt(Steer_EnState=1, Steer_Flt1=0, Steer_Flt2=0, Steer_AngleActual=command_Steer_AngleTarget, Steer_AngleRear_Actual=500, Steer_AngleSpeedActual=command_Steer_AngleSpeed)
            brake_Report.setDataFromInt(Brake_EnState=1, Brake_Flt1=0, Brake_Flt2=0, Brake_PedalActual=command_Brake_Pedal_Target)
            throttle_Report.setDataFromInt(Drive_EnState=1, Drive_Flt1=0, Drive_Flt2=0, Drive_ThrottlePedalActual=command_Drive_ThrottlePedalTarget)

            # CANに変換
            steering_Report.toData()
            brake_Report.toData()
            throttle_Report.toData()


            can_msg_steering_Report = can.Message(arbitration_id = steering_Report.msg_id, data= steering_Report.data, is_extended_id = False)
            can_msg_brake_Report = can.Message(arbitration_id = brake_Report.msg_id, data= brake_Report.data, is_extended_id = False)
            can_msg_throttle_Report = can.Message(arbitration_id = throttle_Report.msg_id, data= throttle_Report.data, is_extended_id = False)

            