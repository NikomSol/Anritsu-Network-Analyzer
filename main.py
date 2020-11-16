import serial.tools.list_ports
import logging
from anritsu import Network_Analyser
from myserial import Serial


# def excepthook(*args):
#   logging.getLogger().error('Uncaught exception:', exc_info=args)
logging.basicConfig(filename="INFO.log", level=logging.INFO, filemode='w')

coms = list(serial.tools.list_ports.comports())
print(coms[0][0])

ser = Serial(setup_file=False,
             com=False, baud=9600, parity='NONE', stopbits=1, bytesize=8,
             terminator='LN', terminator_space=True,
             timeout=0.1, answer_time=0.1,
             logging_message=True)

anr = Network_Analyser(ser)

anr.set_power(output_pow=-6)
anr.set_freq(10,1*10**8,log=True)
anr.set_meas_points(3)
anr.set_RBW(13)

anr.set_channel(channel='all')
anr.set_data_format(ch1_format = 3, ch2_format = 3)
anr.set_meas(ch1_meas = 3, ch2_meas = 5)

anr.sweep(mode = 'single')
anr.get_data(channel='all', plot=True, save=True)

ser.close()
