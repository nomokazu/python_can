class Steering_Report:
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
        self.data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

        # raw に変換する
        # 1 ってのは8バイト。2 ってのは16バイトで、表の Bit Length と対応する
        self.raw_Steer_EnCtrl = self.Steer_EnCtrl.to_bytes(1, byteorder='big')
        self.raw_Steer_AngleSpeed = self.Steer_AngleSpeed.to_bytes(1, byteorder='big')
        self.raw_Steer_AngleTarget = self.Steer_AngleTarget.to_bytes(2, byteorder='big')


        # 単純に 16進数に変換するだけ
        self.data[0] = int.from_bytes((self.raw_Steer_EnCtrl), byteorder="big")
        self.data[1] = int.from_bytes((self.raw_Steer_AngleSpeed), byteorder="big")

        # 配列の2要素にまたがるので、一度 bytearraｙから1つずつ取り出す
        self.data[3] = self.raw_Steer_AngleTarget[0]
        self.data[4] = self.raw_Steer_AngleTarget[1]

        # チェックサムはダミー
        self.checksum_102 = self.data[0] ^ self.data[1] ^ self.data[2] ^ self.data[3] ^ self.data[4] ^ self.data[5] ^ self.data[6]
        self.data[7] = self.checksum_102

    def view(self):
        print("--- CAN ID = " + str(hex(self.msg_id)).ljust(3,"-") + "----- msg_name = " + str(self.msg_name).ljust(20,"-") +  "--")
        print(self.data)
        print("Steer_EnCtrl : ".ljust(30) + str(self.Steer_EnCtrl))
        print("Steer_AngleSpeed : ".ljust(30) + str(self.Steer_AngleSpeed))
        print("Steer_AngleTarget : ".ljust(30) + str(self.Steer_AngleTarget))
        print("checksum_102 : ".ljust(30) + str(self.checksum_102))
        print("---------------------")

class Brake_Report:
    def __init__(self):
        self.msg_id = 0x501
        self.msg_name = "Brake_Report"
        
    def setDataFromCANMessage(self, data):
        self.data = data
        self.dataParser()
        self.toInt()

    # データ型の配列から、それぞれのデータを取り出す
    # とりあえずはあえて bytearray 型　を維持するようにする
    def dataParser(self):
        self.raw_Brake_EnState = self.data[0].to_bytes(1, byteorder='big')
        self.raw_Brake_Flt1 = self.data[1].to_bytes(1, byteorder='big')
        self.raw_Brake_Flt2 = self.data[2].to_bytes(1, byteorder='big')
        self.raw_Brake_PedalActual = self.data[3:4+1]
    
    # それぞれのデータについて、bytearray型 から Int 型にして取り出す
    def toInt(self):
        self.Brake_EnState = int.from_bytes(self.raw_Brake_EnState,"big")
        self.Brake_Flt1 = int.from_bytes(self.raw_Brake_Flt1, "big")
        self.Brake_Flt2 = int.from_bytes(self.raw_Brake_Flt2, "big")
        self.Brake_PedalActual = int.from_bytes(self.raw_Brake_PedalActual, "big")
    
    def view(self):
        print("--- CAN ID = " + str(hex(self.msg_id)).ljust(3,"-") + "----- msg_name = " + str(self.msg_name).ljust(20,"-") +  "--")
        print(self.data)
        print("Brake_EnState : ".ljust(30) + str(self.Brake_EnState))
        print("Brake_Flt1 : ".ljust(30) + str(self.Brake_Flt1))
        print("Brake_Flt2 : ".ljust(30) + str(self.Brake_Flt2))
        print("Brake_PedalActual : ".ljust(30) + str(self.Brake_PedalActual))
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
        self.data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

        self.raw_Brake_EnCtrl = self.Brake_EnCtrl.to_bytes(1, byteorder='big')
        self.raw_Brake_Dec = self.Brake_Dec.to_bytes(2, byteorder='big')
        self.raw_Brake_Pedal_Target = self.Brake_Pedal_Target.to_bytes(2, byteorder='big')

        self.data[0] = int.from_bytes((self.raw_Brake_EnCtrl), byteorder="big")

        self.data[1] = self.raw_Brake_Dec[0]
        self.data[2] = self.raw_Brake_Dec[1]

        self.data[3] = self.raw_Brake_Pedal_Target[0]
        self.data[4] = self.raw_Brake_Pedal_Target[1]

        # チェックサムはダミー
        self.checksum_101 = 0
        self.data[7] = self.checksum_101
    
    def view(self):
        print("--- CAN ID = " + str(hex(self.msg_id)).ljust(3,"-") + "----- msg_name = " + str(self.msg_name).ljust(20,"-") +  "--")
        print(self.data)
        print("Brake_EnCtrl : ".ljust(30) + str(self.Brake_EnCtrl))
        print("Brake_Dec : ".ljust(30) + str(self.Brake_Dec))
        print("Brake_Pedal_Target : ".ljust(30) + str(self.Brake_Pedal_Target))
        print("checksum_101 : ".ljust(30) + str(self.checksum_101))
        print("---------------------")

class Throttle_Report:
    def __init__(self):
        self.msg_id = 0x500
        self.msg_name = "Throttle_Report"
        
    def setDataFromCANMessage(self, data):
        self.data = data
        self.dataParser()
        self.toInt()

    # データ型の配列から、それぞれのデータを取り出す
    # とりあえずはあえて bytearray 型　を維持するようにする
    def dataParser(self):
        self.raw_Dirve_EnState = self.data[0].to_bytes(1, byteorder='big')
        self.raw_Dirve_Flt1 = self.data[1].to_bytes(1, byteorder='big')
        self.raw_Dirve_Flt2 = self.data[2].to_bytes(1, byteorder='big')
        self.raw_Dirve_ThrottlePedalActual = self.data[3:4+1]
    
    # それぞれのデータについて、bytearray型 から Int 型にして取り出す
    def toInt(self):
        self.Dirve_EnState = int.from_bytes(self.raw_Dirve_EnState,"big")
        self.Dirve_Flt1 = int.from_bytes(self.raw_Dirve_Flt1, "big")
        self.Dirve_Flt2 = int.from_bytes(self.raw_Dirve_Flt2, "big")
        self.Dirve_ThrottlePedalActual = int.from_bytes(self.raw_Dirve_ThrottlePedalActual, "big")
    
    def view(self):
        print("--- CAN ID = " + str(hex(self.msg_id)).ljust(3,"-") + "----- msg_name = " + str(self.msg_name).ljust(20,"-") +  "--")
        print(self.data)
        print("Dirve_EnState : ".ljust(30) + str(self.Dirve_EnState))
        print("Dirve_Flt1 : ".ljust(30) + str(self.Dirve_Flt1))
        print("Dirve_Flt2 : ".ljust(30) + str(self.Dirve_Flt2))
        print("Dirve_ThrottlePedalActual : ".ljust(30) + str(self.Dirve_ThrottlePedalActual))
        print("---------------------")

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
        self.data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

        self.raw_Dirve_EnCtrl = self.Dirve_EnCtrl.to_bytes(1, byteorder='big')
        self.raw_Dirve_Acc = self.Dirve_Acc.to_bytes(2, byteorder='big')
        self.raw_Dirve_ThrottlePedalTarget = self.Dirve_ThrottlePedalTarget.to_bytes(2, byteorder='big')
        self.raw_Dirve_SpeedTarget = self.Dirve_SpeedTarget.to_bytes(2, byteorder='big')

        self.data[0] = int.from_bytes((self.raw_Dirve_EnCtrl), byteorder="big")

        self.data[1] = self.raw_Dirve_Acc[0]
        self.data[2] = self.raw_Dirve_Acc[1]
        self.data[3] = self.raw_Dirve_ThrottlePedalTarget[0]
        self.data[4] = self.raw_Dirve_ThrottlePedalTarget[1]
        self.data[5] = self.raw_Dirve_SpeedTarget[0]
        self.data[6] = self.raw_Dirve_SpeedTarget[1]

        # チェックサムはダミー
        self.checksum_100 = 0
        self.data[7] = self.checksum_100

    def view(self):
        print("--- CAN ID = " + str(hex(self.msg_id)).ljust(3,"-") + "----- msg_name = " + str(self.msg_name).ljust(20,"-") +  "--")
        print(self.data)
        print("Dirve_EnCtrl : ".ljust(30) + str(self.Dirve_EnCtrl))
        print("Dirve_Acc : ".ljust(30) + str(self.Dirve_Acc))
        print("Dirve_ThrottlePedalTarget : ".ljust(30) + str(self.Dirve_ThrottlePedalTarget))
        print("Dirve_SpeedTarget : ".ljust(30) + str(self.Dirve_SpeedTarget))
        print("checksum_100 : ".ljust(30) + str(self.checksum_100))
        print("---------------------")
