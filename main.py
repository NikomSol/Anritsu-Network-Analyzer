import serial.tools.list_ports
import serial
import matplotlib.pyplot as plt
from anritsu import Anritsu

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

ser.write(b'SWP 1 \n')
print(ser.readline())
# anr = Anritsu(ser)
# anr.sweep('single')

ser.close()
print(ser.isOpen())
