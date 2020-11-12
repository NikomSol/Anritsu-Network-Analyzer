import serial.tools.list_ports
import serial
import time
import numpy as np
import re
import matplotlib.pyplot as plt

coms = list(serial.tools.list_ports.comports())
print(coms[0][0])

terminator_input = 'LF'

ser = serial.Serial(
    port=coms[0][0],
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.1
)

print(ser.isOpen())

ser.flushInput()
ser.flushOutput()
# ser.write(b'ACCH? \n')
flag = 1
while flag:
    flag = len(ser.readline())
    # print(ser.readline().decode('utf-8') is '')
print('clear')

N = 1001
data = np.zeros(N)
ser.write(('XMA? 0, '+str(N)+' \n').encode('utf-8'))
# ser.write(b'XMA? 0, 10 \n')

for i in range(N):
    str = ser.readline()
    # print(str)
    if str is not b'':
        data[i] = float(str.decode('utf-8'))
# print(data)

ser.close()
print(ser.isOpen())

plt.plot(data)
plt.show()