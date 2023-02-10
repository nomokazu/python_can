import time
import msg
import can

throttle_path = '/mnt/d/Research/CAN/CAN_Unity/Assets/Resources/throttle.txt'
steering_path = '/mnt/d/Research/CAN/CAN_Unity/Assets/Resources/steering.txt'

bus = can.Bus('ws://localhost:54701/', bustype='remote', bitrate=500000)

steering = 0 # Steeringは-1~1の間で左が-1, 中心が, 右が1
throttle = 1 # throttleは-1~0がブレーキ, 0～1がアクセル

steering_can = msg.Steering_Command()

while True:
    print("==============================================")
    # CANメッセージを受信
    start_time = time.time()
    while time.time() - start_time < 0.01 : # 0.01sec間モニター
        recv_msg = bus.recv(timeout=1) # canメッセージを受け取る
        if recv_msg != None: # メッセージがあるとき
            if recv_msg.arbitration_id == 258: # id=102のとき
                print(recv_msg.data)
                steering_can.setDataFromCANMessage(recv_msg.data)
                print(steering_can.Steer_AngleTarget)
                steering = steering_can.Steer_AngleTarget/500 # canデータをUnityの車両のスケールに合わせる

    # Steering情報をSteering.txtに書き込み
    with open(steering_path, mode='w') as f:
        f.write(str(steering) + "\n")
    print("Updated.")

    # 書き込んだsteering情報をターミナルに出力
    if(steering>0):
        print("Steering: " + str(steering*100)+"% Right")
    elif(steering==0):
        print("Steering: Center")
    else:
        print("Steering: " + str(steering*100)+"% Left")
    time.sleep(1)