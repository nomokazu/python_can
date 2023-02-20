import can
import msg
import asyncio


class HandleControllerCommand:
    def __init__(self):
        # self.bus = can.interface.Bus('ws://localhost:54701/', bustype='remote', preserve_timestamps=True)
        # self.bus = can.interface.Bus('test', bustype='virtual', preserve_timestamps=True)
        self.bus = can.interface.Bus(bustype='socketcan', channel="slcan0", bitrate=500000, app_name='python-can')



        # CANメッセージを送信するかしないかを判断するFlag
        self.sendFlag = False

        # 非同期でCANを送る
        asyncio.new_event_loop().run_in_executor(None, self.canSend)
        
    
    def setHandleControllerCommandSend(self, steering, accel_pedal, brake_pedal):
        self.steering = steering
        self.accel_pedal = accel_pedal
        self.brake_pedal = brake_pedal
        self.convertHandleControllerParameterToCanBusParameter()
    
    # ハンドルコントロールが出力した値を、CANBUSに載せる値に変化する
    # 現状はただの int 変換のみ
    # ハンドルコントロールの使用に合わせて変更する
    def convertHandleControllerParameterToCanBusParameter(self):
        # マイナスの値は送れないので、+ 1しておく
        self.canbus_steering = int((self.steering) * -500 + 500)
        self.canbus_accel_pedal = int(self.accel_pedal * 100)
        self.canbus_brake_pedal = int(self.brake_pedal * 100)
        self.message_Steering_Command = msg.Steering_Command()
        self.message_Steering_Command.setDataFromInt(1, 16, self.canbus_steering)
        self.message_Brake_Command = msg.Brake_Command()
        self.message_Brake_Command.setDataFromInt(1, 10, self.canbus_brake_pedal)
        self.message_Throttle_Command = msg.Throttle_Command()
        self.message_Throttle_Command.setDataFromInt(1, 10, self.canbus_accel_pedal, 100)
        
        self.message_Steering_Command.toData()
        self.message_Brake_Command.toData()
        self.message_Throttle_Command.toData()

        # self.message_Throttle_Command.view()


        self.can_msg_Steering_Command = can.Message(arbitration_id = self.message_Steering_Command.msg_id, data= self.message_Steering_Command.data, is_extended_id = False)
        self.can_msg_Brake_Command = can.Message(arbitration_id = self.message_Brake_Command.msg_id, data= self.message_Brake_Command.data, is_extended_id = False)
        self.can_msg_Throttle_Command = can.Message(arbitration_id = self.message_Throttle_Command.msg_id, data= self.message_Throttle_Command.data, is_extended_id = False)

    def canSend(self):
        while True:
            print(self.sendFlag)
            if self.sendFlag:
                print("s")
                self.bus.send(self.can_msg_Steering_Command)
                self.bus.send(self.can_msg_Brake_Command)
                self.bus.send(self.can_msg_Throttle_Command)
            # time.sleep(0.001)
    
    def startCanSend(self):
        self.sendFlag = True
    
    def stopCanSend(self):
        self.sendFlag = False
    
