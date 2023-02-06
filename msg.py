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