import serial
import time

import serial.tools.list_ports
coms = list(serial.tools.list_ports.comports())
print(coms[0][0])

ser = serial.Serial(
    # port=coms[0][0],
    port="COM4",
    baudrate=19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.Terminator = 'LF'
print(ser.isOpen())



ser.write(b'*IDN?\n')
data = ''
# data = ser.read()
data = ser.readline()
print('data is:',data)

ser.close()
print(ser.isOpen())
