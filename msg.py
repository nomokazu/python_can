class Msg_Steering_Report:
    def __init__(self):
        self.msg_id = 0x502
        self.msg_name = "Steering_Report"
        
    
    def setDataFromCANMessage(self, data):
        self.data = data
        self.dataParser()
        self.toInt()

    # データ型の配列から、それぞれのデータを取り出す
    # とりあえずはあえて bytearray 型　を維持するようにする
    def dataParser(self):
        self.raw_Steer_EnState = self.data[0].to_bytes(1, byteorder='big')
        self.raw_Steer_Flt1 = self.data[1].to_bytes(1, byteorder='big')
        self.raw_Steer_Flt2 = self.data[2].to_bytes(1, byteorder='big')
        self.raw_Steer_AngleActual = self.data[3:4+1]
        self.raw_Steer_AngleRear_Actual = self.data[5:6+1]
        self.raw_Steer_AngleSpeedActual = self.data[7].to_bytes(1, byteorder='big')
    
    # それぞれのデータについて、bytearray型 から Int 型にして取り出す
    def toInt(self):
        self.Steer_EnState = int.from_bytes(self.raw_Steer_EnState,"big")
        self.Steer_Flt1 = int.from_bytes(self.raw_Steer_Flt1, "big")
        self.Steer_Flt2 = int.from_bytes(self.raw_Steer_Flt2, "big")
        self.Steer_AngleActual = int.from_bytes(self.raw_Steer_AngleActual, "big")
        self.Steer_AngleRear_Actual = int.from_bytes(self.raw_Steer_AngleRear_Actual, "big")
        self.Steer_AngleSpeedActual = int.from_bytes(self.raw_Steer_AngleSpeedActual, "big")
    
    def view(self):
        print("--- CAN ID = " + str(hex(self.msg_id)).ljust(3,"-") + "----- msg_name = " + str(self.msg_name).ljust(20,"-") +  "--")
        print(self.data)
        print("Steer_EnState : ".ljust(30) + str(self.Steer_EnState))
        print("Steer_Flt1 : ".ljust(30) + str(self.Steer_Flt1))
        print("Steer_Flt2 : ".ljust(30) + str(self.Steer_Flt2))
        print("Steer_AngleActual : ".ljust(30) + str(self.Steer_AngleActual))
        print("Steer_AngleRear_Actual : ".ljust(30) + str(self.Steer_AngleRear_Actual))
        print("Steer_AngleSpeedActual : ".ljust(30) + str(self.Steer_AngleSpeedActual))
        print("---------------------")
    
    # 逆に配列 list 型に変換する
    def toData(self):
        data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

        # raw に変換する
        self.raw_Steer_EnState = self.Steer_EnState.to_bytes(1, byteorder='big')
        self.raw_Steer_Flt1 = self.Steer_Flt1.to_bytes(1, byteorder='big')
        self.raw_Steer_Flt2 = self.Steer_Flt2.to_bytes(1, byteorder='big')
        self.raw_Steer_AngleActual = self.Steer_AngleActual.to_bytes(2, byteorder='big')
        self.raw_Steer_AngleRear_Actual = self.Steer_AngleRear_Actual.to_bytes(2, byteorder='big')
        self.raw_Steer_AngleSpeedActual = self.Steer_AngleSpeedActual.to_bytes(1, byteorder='big')

        # 単純に 16進数に変換するだけ
        data[0] = hex(int.from_bytes((self.raw_Steer_EnState), byteorder="big"))
        data[1] = hex(int.from_bytes((self.raw_Steer_Flt1), byteorder="big"))
        data[2] = hex(int.from_bytes((self.raw_Steer_Flt2), byteorder="big"))
        data[7] = hex(int.from_bytes((self.raw_Steer_AngleSpeedActual), byteorder="big"))

        # 配列の2要素にまたがるので、一度 bytearraｙから1つずつ取り出す
        data[3] = hex(self.raw_Steer_AngleActual[0])
        data[4] = hex(self.raw_Steer_AngleActual[1])

        data[5] = hex(self.raw_Steer_AngleRear_Actual[0])
        data[6] = hex(self.raw_Steer_AngleRear_Actual[1])

        self.data = data

    # int型でデータを指定する
    def setDataFromInt(self, Steer_EnState, Steer_Flt1, Steer_Flt2, Steer_AngleActual, Steer_AngleRear_Actual, Steer_AngleSpeedActual):
        self.Steer_EnState = Steer_EnState
        self.Steer_Flt1 = Steer_Flt1
        self.Steer_Flt2 = Steer_Flt2
        self.Steer_AngleActual = Steer_AngleActual
        self.Steer_AngleRear_Actual = Steer_AngleRear_Actual
        self.Steer_AngleSpeedActual = Steer_AngleSpeedActual
        self.toData()

class Steering_Command:
    def __init__(self):
        self.msg_id = 0x102
        self.msg_name = "Steering_Command"
    
    # チェックサムは、後回し
    def setDataFromInt(self, Steer_EnCtrl, Steer_AngleSpeed, Steer_AngleTarget):
        self.Steer_EnCtrl = Steer_EnCtrl
        self.Steer_AngleSpeed = Steer_AngleSpeed
        self.Steer_AngleTarget = Steer_AngleTarget
    

    # 逆に配列 list 型に変換する
    def toData(self):
        data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

        # raw に変換する
        # 1 ってのは8バイト。2 ってのは16バイトで、表の Bit Length と対応する
        self.raw_Steer_EnCtrl = self.Steer_EnCtrl.to_bytes(1, byteorder='big')
        self.raw_Steer_AngleSpeed = self.Steer_AngleSpeed.to_bytes(1, byteorder='big')
        self.raw_Steer_AngleTarget = self.Steer_AngleTarget.to_bytes(2, byteorder='big')
        self.raw_CheckSum_102 = self.CheckSum_102.to_bytes(1, byteorder='big')

        # 単純に 16進数に変換するだけ
        data[0] = hex(int.from_bytes((self.raw_Steer_EnCtrl), byteorder="big"))
        data[1] = hex(int.from_bytes((self.raw_Steer_AngleSpeed), byteorder="big"))
        data[7] = hex(int.from_bytes((self.raw_CheckSum_102), byteorder="big"))

        # 配列の2要素にまたがるので、一度 bytearraｙから1つずつ取り出す
        data[3] = hex(self.raw_Steer_AngleTarget[0])
        data[4] = hex(self.raw_Steer_AngleTarget[1])

        # チェックサムの計算
        # https://github.com/ApolloAuto/apollo/blob/93f69712269da572206e021cc7419b21c6feb595/modules/canbus_vehicle/devkit/protocol/steering_command_102.cc
        checksum_102 = data[0] ^ data[1] ^ data[2] ^ data[3] ^ data[4] ^ data[5] ^ data[6]
        data[7] = checksum_102

    def view(self):
        print("--- CAN ID = " + str(hex(self.msg_id)).ljust(3,"-") + "----- msg_name = " + str(self.msg_name).ljust(20,"-") +  "--")
        print(self.data)
        print("Steer_EnCtrl : ".ljust(30) + str(self.Steer_EnCtrl))
        print("Steer_AngleSpeed : ".ljust(30) + str(self.Steer_AngleSpeed))
        print("Steer_AngleTarget : ".ljust(30) + str(self.Steer_AngleTarget))
        print("---------------------")

class Brake_Command:
    def __init__(self):
        self.msg_id = 0x101
        self.msg_name = "Brake_Command"
    
    def setDataFromInt(self, Brake_EnCtrl, Brake_Dec, Brake_Pedal_Target):
        self.Brake_EnCtrl = Brake_EnCtrl
        self.Brake_Dec = Brake_Dec
        self.Brake_Pedal_Target = Brake_Pedal_Target
    
    def toData(self):
        data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

        self.raw_Brake_EnCtrl = self.Brake_EnCtrl.to_bytes(1, byteorder='big')
        self.raw_Brake_Dec = self.Brake_Dec.to_bytes(2, byteorder='big')
        self.raw_Brake_Pedal_Target = self.Brake_Pedal_Target.to_bytes(2, byteorder='big')

        data[0] = hex(int.from_bytes((self.raw_Brake_EnCtrl), byteorder="big"))

        data[1] = hex(self.raw_Brake_Dec[0])
        data[2] = hex(self.raw_Brake_Dec[1])

        data[3] = hex(self.raw_Brake_Pedal_Target[0])
        data[4] = hex(self.raw_Brake_Pedal_Target[1])

        checksum_101 = data[0] ^ data[1] ^ data[2] ^ data[3] ^ data[4] ^ data[5] ^ data[6]
        data[7] = checksum_101

class Throttle_Command:
    def __init__(self):
        self.msg_id = 0x100
        self.msg_name = "Throttle_Command"
    
    def setDataFromInt(self, Dirve_EnCtrl, Dirve_Acc, Dirve_ThrottlePedalTarget, Dirve_SpeedTarget):
        self.Dirve_EnCtrl = Dirve_EnCtrl
        self.Dirve_Acc = Dirve_Acc
        self.Dirve_ThrottlePedalTarget = Dirve_ThrottlePedalTarget
        self.Dirve_SpeedTarget = Dirve_SpeedTarget
    
    def toData(self):
        data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

        self.raw_Dirve_EnCtrl = self.Dirve_EnCtrl.to_bytes(1, byteorder='big')
        self.raw_Dirve_Acc = self.Dirve_Acc.to_bytes(2, byteorder='big')
        self.raw_Dirve_ThrottlePedalTarget = self.Dirve_ThrottlePedalTarget.to_bytes(2, byteorder='big')
        self.raw_Dirve_SpeedTarget = self.Dirve_SpeedTarget.to_bytes(2, byteorder='big')

        data[0] = hex(int.from_bytes((self.raw_Dirve_EnCtrl), byteorder="big"))

        data[1] = hex(self.raw_Dirve_Acc[0])
        data[2] = hex(self.raw_Dirve_Acc[1])
        data[3] = hex(self.raw_Dirve_ThrottlePedalTarget[0])
        data[4] = hex(self.raw_Dirve_ThrottlePedalTarget[1])
        data[5] = hex(self.raw_Dirve_SpeedTarget[0])
        data[6] = hex(self.raw_Dirve_SpeedTarget[1])

        checksum_100 = data[0] ^ data[1] ^ data[2] ^ data[3] ^ data[4] ^ data[5] ^ data[6]
        data[7] = checksum_100

