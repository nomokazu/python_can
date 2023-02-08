import can
import time

# バスタイプはよくわからない
bus = can.interface.Bus(bustype='socketcan', channel="slcan0", bitrate=500000, app_name='python-can')

#受信
start_time = time.time()

# message の参考情報 : https://python-can.readthedocs.io/en/stable/message.html

while True:
	message = bus.recv(timeout=1)
	if message != None:
		print("CAN ID : " + hex(message.arbitration_id))
		# 果たしてこれがどんなデータになるかわからん
		print("Data : " + str(message.data))