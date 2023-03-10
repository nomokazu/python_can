import can

# Create a connection to server. Any config is passed to server.
bus = can.Bus('ws://localhost:54701/',
              bustype='remote',
              bitrate=500000,
              receive_own_messages=True)

# Send messages
# msg = can.Message(arbitration_id=0x12345, data=[1,2,3,4,5,6,7,8])
# bus.send(msg)

# Receive messages
while True:
	msg2 = bus.recv(1)
	print(msg2)

# Disconnect
bus.shutdown()
