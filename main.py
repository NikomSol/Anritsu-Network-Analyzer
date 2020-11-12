import serial.tools.list_ports
import serial
import time
import numpy as np
import pandas as pd
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


def read_data(N):
    time.sleep(0.5)
    data = np.zeros(N)
    for i in range(N):
        str = ser.readline()
        if str is not b'':
            data[i] = float(str.decode('utf-8'))
    return data


def clear_input():
    flag = 1
    while flag:
        flag = len(ser.readline())


ser.write(b'SWP 1 \n')

sweep = 1
while sweep:
    time.sleep(0.1)
    ser.write(b'SWP? \n')
    sweep = 0 if (ser.readline() == b'0\n') else 1

N = 101
dataChannel = pd.DataFrame(np.zeros((N, 3)), columns=['fq', 'mag', 'pha'])
# ser.write(('XMA? 0, '+str(N)+' \n').encode('utf-8'))

clear_input()
ser.write(('FQM? 0, ' + str(N) + ' \n').encode('utf-8'))
dataChannel['fq'] = read_data(N)

clear_input()
ser.write(('XMA? 0, ' + str(N) + ' \n').encode('utf-8'))
dataChannel['mag'] = read_data(N)

clear_input()
ser.write(('XMB? 0, ' + str(N) + ' \n').encode('utf-8'))
dataChannel['pha'] = read_data(N)

dataChannel.to_csv("dataChannel.csv")

fig, axs = plt.subplots(nrows=1, ncols=2, sharex=True)
ax = axs[0]
ax.errorbar(dataChannel['fq'], dataChannel['mag'])
ax.set_title('magnitude')

ax = axs[1]
ax.errorbar(dataChannel['fq'], dataChannel['pha'])
ax.set_title('phase')

fig.suptitle('data from channel')

ser.close()
print(ser.isOpen())
plt.show()
