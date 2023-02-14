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
        self.data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

        # raw に変換する
        self.raw_Steer_EnState = self.Steer_EnState.to_bytes(1, byteorder='big')
        self.raw_Steer_Flt1 = self.Steer_Flt1.to_bytes(1, byteorder='big')
        self.raw_Steer_Flt2 = self.Steer_Flt2.to_bytes(1, byteorder='big')
        self.raw_Steer_AngleActual = self.Steer_AngleActual.to_bytes(2, byteorder='big')
        self.raw_Steer_AngleRear_Actual = self.Steer_AngleRear_Actual.to_bytes(2, byteorder='big')
        self.raw_Steer_AngleSpeedActual = self.Steer_AngleSpeedActual.to_bytes(1, byteorder='big')

        # 単純に 16進数に変換するだけ
        self.data[0] = int.from_bytes((self.raw_Steer_EnState), byteorder="big")
        self.data[1] = int.from_bytes((self.raw_Steer_Flt1), byteorder="big")
        self.data[2] = int.from_bytes((self.raw_Steer_Flt2), byteorder="big")
        self.data[7] = int.from_bytes((self.raw_Steer_AngleSpeedActual), byteorder="big")

        # 配列の2要素にまたがるので、一度 bytearraｙから1つずつ取り出す
        self.data[3] = self.raw_Steer_AngleActual[0]
        self.data[4] = self.raw_Steer_AngleActual[1]

        self.data[5] = self.raw_Steer_AngleRear_Actual[0]
        self.data[6] = self.raw_Steer_AngleRear_Actual[1]

    # int型でデータを指定する
    def setDataFromInt(self, Steer_EnState, Steer_Flt1, Steer_Flt2, Steer_AngleActual, Steer_AngleRear_Actual, Steer_AngleSpeedActual):
        self.Steer_EnState = Steer_EnState
        self.Steer_Flt1 = Steer_Flt1
        self.Steer_Flt2 = Steer_Flt2
        self.Steer_AngleActual = Steer_AngleActual
        self.Steer_AngleRear_Actual = Steer_AngleRear_Actual
        self.Steer_AngleSpeedActual = Steer_AngleSpeedActual

class Steering_Command:
    def __init__(self):
        self.msg_id = 0x102
        self.msg_name = "Steering_Command"
    
    # チェックサムは、後回し
    def setDataFromInt(self, Steer_EnCtrl, Steer_AngleSpeed, Steer_AngleTarget):
        self.Steer_EnCtrl = Steer_EnCtrl
        self.Steer_AngleSpeed = Steer_AngleSpeed
        self.Steer_AngleTarget = Steer_AngleTarget
    
    def setDataFromCANMessage(self, data):
        self.data = data
        self.dataParser()
        self.toInt()
    
    def dataParser(self):
        self.raw_Steer_EnCtrl = self.data[0].to_bytes(1, byteorder='big')
        self.raw_Steer_AngleSpeed = self.data[1].to_bytes(1, byteorder='big')
        self.raw_Steer_AngleTarget = self.data[3:4+1]
        self.raw_checksum_102 = self.data[7].to_bytes(1, byteorder='big')
    
    def toInt(self):
        self.Steer_EnCtrl = int.from_bytes(self.raw_Steer_EnCtrl,"big")
        self.Steer_AngleSpeed = int.from_bytes(self.raw_Steer_AngleSpeed,"big")
        self.Steer_AngleTarget = int.from_bytes(self.raw_Steer_AngleTarget,"big")
        self.checksum_102 = int.from_bytes(self.raw_checksum_102,"big")

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
    
    def toData(self):
        self.data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

        # raw に変換する
        self.raw_Brake_EnState = self.Brake_EnState.to_bytes(1, byteorder='big')
        self.raw_Brake_Flt1 = self.Brake_Flt1.to_bytes(1, byteorder='big')
        self.raw_Brake_Flt2 = self.Brake_Flt2.to_bytes(1, byteorder='big')
        self.raw_Brake_PedalActual = self.Brake_PedalActual.to_bytes(2, byteorder='big')

        self.data[0] = int.from_bytes((self.raw_Brake_EnState), byteorder="big")
        self.data[1] = int.from_bytes((self.raw_Brake_Flt1), byteorder="big")
        self.data[2] = int.from_bytes((self.raw_Brake_Flt2), byteorder="big")
        
        self.data[3] = self.raw_Brake_PedalActual[0]
        self.data[4] = self.raw_Brake_PedalActual[1]

    def setDataFromInt(self, Brake_EnState, Brake_Flt1, Brake_Flt2, Brake_PedalActual):
        self.Brake_EnState = Brake_EnState
        self.Brake_Flt1 = Brake_Flt1
        self.Brake_Flt2 = Brake_Flt2
        self.Brake_PedalActual = Brake_PedalActual
    

class Brake_Command:
    def __init__(self):
        self.msg_id = 0x101
        self.msg_name = "Brake_Command"
    
    def setDataFromInt(self, Brake_EnCtrl, Brake_Dec, Brake_Pedal_Target):
        self.Brake_EnCtrl = Brake_EnCtrl
        self.Brake_Dec = Brake_Dec
        self.Brake_Pedal_Target = Brake_Pedal_Target
    
    def setDataFromCANMessage(self, data):
        self.data = data
        self.dataParser()
        self.toInt()
    
    def dataParser(self):
        self.raw_Brake_EnCtrl = self.data[0].to_bytes(1, byteorder='big')
        self.raw_Brake_Dec = self.data[1:2+1]
        self.raw_Brake_Pedal_Target = self.data[3:4+1]
        self.raw_checksum_101 = self.data[7].to_bytes(1, byteorder='big')
    
    def toInt(self):
        self.Brake_EnCtrl = int.from_bytes(self.raw_Brake_EnCtrl,"big")
        self.Brake_Dec = int.from_bytes(self.raw_Brake_Dec,"big")
        self.Brake_Pedal_Target = int.from_bytes(self.raw_Brake_Pedal_Target,"big")
        self.checksum_101 = int.from_bytes(self.raw_checksum_101,"big")

    
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
        self.raw_Drive_EnState = self.data[0].to_bytes(1, byteorder='big')
        self.raw_Drive_Flt1 = self.data[1].to_bytes(1, byteorder='big')
        self.raw_Drive_Flt2 = self.data[2].to_bytes(1, byteorder='big')
        self.raw_Drive_ThrottlePedalActual = self.data[3:4+1]
    
    # それぞれのデータについて、bytearray型 から Int 型にして取り出す
    def toInt(self):
        self.Drive_EnState = int.from_bytes(self.raw_Drive_EnState,"big")
        self.Drive_Flt1 = int.from_bytes(self.raw_Drive_Flt1, "big")
        self.Drive_Flt2 = int.from_bytes(self.raw_Drive_Flt2, "big")
        self.Drive_ThrottlePedalActual = int.from_bytes(self.raw_Drive_ThrottlePedalActual, "big")
    
    def view(self):
        print("--- CAN ID = " + str(hex(self.msg_id)).ljust(3,"-") + "----- msg_name = " + str(self.msg_name).ljust(20,"-") +  "--")
        print(self.data)
        print("Drive_EnState : ".ljust(30) + str(self.Drive_EnState))
        print("Drive_Flt1 : ".ljust(30) + str(self.Drive_Flt1))
        print("Drive_Flt2 : ".ljust(30) + str(self.Drive_Flt2))
        print("Drive_ThrottlePedalActual : ".ljust(30) + str(self.Drive_ThrottlePedalActual))
        print("---------------------")
    
    def toData(self):
        self.data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

        self.raw_Drive_EnState = self.Drive_EnState.to_bytes(1, byteorder='big')
        self.raw_Drive_Flt1 = self.Drive_Flt1.to_bytes(1, byteorder='big')
        self.raw_Drive_Flt2 = self.Drive_Flt2.to_bytes(1, byteorder='big')
        self.raw_Drive_ThrottlePedalActual = self.Drive_ThrottlePedalActual.to_bytes(2, byteorder='big')

        self.data[0] = int.from_bytes((self.raw_Drive_EnState), byteorder="big")
        self.data[1] = int.from_bytes((self.raw_Drive_Flt1), byteorder="big")
        self.data[2] = int.from_bytes((self.raw_Drive_Flt2), byteorder="big")

        self.data[3] = self.raw_Drive_ThrottlePedalActual[0]
        self.data[4] = self.raw_Drive_ThrottlePedalActual[1]

    def setDataFromInt(self, Drive_EnState, Drive_Flt1, Drive_Flt2, Drive_ThrottlePedalActual):
        self.Drive_EnState = Drive_EnState
        self.Drive_Flt1 = Drive_Flt1
        self.Drive_Flt2 = Drive_Flt2
        self.Drive_ThrottlePedalActual = Drive_ThrottlePedalActual
    

class Throttle_Command:
    def __init__(self):
        self.msg_id = 0x100
        self.msg_name = "Throttle_Command"
    
    def setDataFromInt(self, Drive_EnCtrl, Drive_Acc, Drive_ThrottlePedalTarget, Drive_SpeedTarget):
        self.Drive_EnCtrl = Drive_EnCtrl
        self.Drive_Acc = Drive_Acc
        self.Drive_ThrottlePedalTarget = Drive_ThrottlePedalTarget
        self.Drive_SpeedTarget = Drive_SpeedTarget
    
    def setDataFromCANMessage(self, data):
        self.data = data
        self.dataParser()
        self.toInt()
    
    def dataParser(self):
        self.raw_Drive_EnCtrl = self.data[0].to_bytes(1, byteorder='big')
        self.raw_Drive_Acc = self.data[1:2+1]
        self.raw_Drive_ThrottlePedalTarget = self.data[3:4+1]
        self.raw_Drive_SpeedTarget = self.data[5:6+1]
        self.raw_checksum_100 = self.data[7].to_bytes(1, byteorder='big')
    
    def toInt(self):
        self.Drive_EnCtrl = int.from_bytes(self.raw_Drive_EnCtrl,"big")
        self.Drive_Acc = int.from_bytes(self.raw_Drive_Acc,"big")
        self.Drive_ThrottlePedalTarget = int.from_bytes(self.raw_Drive_ThrottlePedalTarget,"big")
        self.Drive_SpeedTarget = int.from_bytes(self.raw_Drive_SpeedTarget,"big")
        self.checksum_100 = int.from_bytes(self.raw_checksum_100,"big")

    
    def toData(self):
        self.data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

        self.raw_Drive_EnCtrl = self.Drive_EnCtrl.to_bytes(1, byteorder='big')
        self.raw_Drive_Acc = self.Drive_Acc.to_bytes(2, byteorder='big')
        self.raw_Drive_ThrottlePedalTarget = self.Drive_ThrottlePedalTarget.to_bytes(2, byteorder='big')
        self.raw_Drive_SpeedTarget = self.Drive_SpeedTarget.to_bytes(2, byteorder='big')

        self.data[0] = int.from_bytes((self.raw_Drive_EnCtrl), byteorder="big")

        self.data[1] = self.raw_Drive_Acc[0]
        self.data[2] = self.raw_Drive_Acc[1]
        self.data[3] = self.raw_Drive_ThrottlePedalTarget[0]
        self.data[4] = self.raw_Drive_ThrottlePedalTarget[1]
        self.data[5] = self.raw_Drive_SpeedTarget[0]
        self.data[6] = self.raw_Drive_SpeedTarget[1]

        # チェックサムはダミー
        self.checksum_100 = 0
        self.data[7] = self.checksum_100

    def view(self):
        print("--- CAN ID = " + str(hex(self.msg_id)).ljust(3,"-") + "----- msg_name = " + str(self.msg_name).ljust(20,"-") +  "--")
        print(self.data)
        print("Drive_EnCtrl : ".ljust(30) + str(self.Drive_EnCtrl))
        print("Drive_Acc : ".ljust(30) + str(self.Drive_Acc))
        print("Drive_ThrottlePedalTarget : ".ljust(30) + str(self.Drive_ThrottlePedalTarget))
        print("Drive_SpeedTarget : ".ljust(30) + str(self.Drive_SpeedTarget))
        print("checksum_100 : ".ljust(30) + str(self.checksum_100))
        print("---------------------")
