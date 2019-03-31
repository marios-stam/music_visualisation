import serial, time,struct
arduino = serial.Serial('COM3', 115200, timeout=.1)
time.sleep(1) #give the connection a second to settle

time.sleep(1)
#print('1'.encode("utf-8"))
while True:
    arduino.write(struct.pack('>i', 256))
    print("received")
    line = arduino.readline()
    print(line)