import serial.tools.list_ports
import logging
from anritsu import Network_Analyser
from myserial import Serial


# def excepthook(*args):
#   logging.getLogger().error('Uncaught exception:', exc_info=args)
logging.basicConfig(filename="INFO.log", level=logging.INFO, filemode='w')

ser = Serial(setup_file=False,
             com=False, baud=9600, parity='NONE', stopbits=1, bytesize=8,
             terminator='LN', terminator_space=True,
             timeout=5, answer_time=0.05,
             logging_message=True)

anr = Network_Analyser(ser)

# anr.set_power(output_pow=-6)
# anr.set_freq(10,3*10**8,log=True)
# anr.set_meas_points(6)
# anr.set_RBW(2)
#
# anr.set_channel(channel='all')
# anr.set_data_format(ch1_format = 3, ch2_format = 3)
# anr.set_meas(ch1_meas = 3, ch2_meas = 5)
#
anr.set_channel(channel='ch2')
anr.sweep(mode = 'single')
anr.auto_scale()
anr.get_data(channel='ch2', plot=True, save=True)

ser.close()
