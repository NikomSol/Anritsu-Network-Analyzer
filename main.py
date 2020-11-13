import serial.tools.list_ports
import serial
import time
from anritsu import Anritsu

coms = list(serial.tools.list_ports.comports())
print(coms[0][0])

ser = serial.Serial(
    port=coms[0][0],
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.1
)
print(ser.isOpen())

anr = Anritsu(ser)

anr.set_power(output_pow=-6)
anr.set_freq(10,1*10**8,log=True)
anr.set_poins(3)
anr.set_RBW(13)

anr.set_channel(channel='all')
anr.set_format(3, channel = 'all')
anr.set_meas(3,channel = 'ch1')
anr.set_meas(5,channel = 'ch2')

anr.sweep('single')
anr.get_data(channel='all',plot=True,save=True)

ser.close()
print(ser.isOpen())

