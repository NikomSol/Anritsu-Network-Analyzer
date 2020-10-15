import serial
import time

import serial.tools.list_ports
coms = list(serial.tools.list_ports.comports())
print(coms[0][0])

ser = serial.Serial(
    # port=coms[0][0],
    port="COM3",
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
print(ser.isOpen())

ser.write(b'DF2?')

time.sleep(0.3)

data = ser.readline()
print('data is:',data)

ser.close()
print(ser.isOpen())
