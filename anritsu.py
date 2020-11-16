from myserial import Serial
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging


class Network_Analyser:

    def __init__(self, _serial: Serial):
        self.ser = _serial
        self.MEP = {0: 11, 1: 21, 2: 51, 3: 101, 4: 251, 5: 501, 6: 1001}
        self.RBW = {0: '3Hz', 1: '10Hz', 2: '30Hz', 3: '100Hz', 4: '300Hz', 5: '1kHz', 6: '3kHz', 7: '10kHz',
                    8: '500Hz', 9: '2kHz', 10: '4kHz', 11: '5kHz', 12: '20kHz', 13: 'AUTO'}
        self.TRC = {0: 'LOGMAG', 1: 'PHASE', 2: 'DELAY', 3: 'MAG & PHASE', 4: 'MAG & DELAY', 5: 'POLAR',
                    6: 'IMPD CHART', 7: 'ADMT CHART', 8: 'VSWR', 9: 'LINMAG', 10: 'LIN & PHASE', 11: 'LIN & DELAY',
                    12: 'REAL', 13: 'IMAG', 14: 'REAL & IMAG', 15: 'LOG Z', 16: 'LOG Z & θ', 17: 'Q', 18: 'LOG Z & Q'}
        self.MEASPT = {0: 'TB/TA', 1: 'TA/R', 2: 'TB/R', 3: 'TA', 4: 'TB', 5: 'R'}

    def set_freq(self, start: int, stop: int, log: bool = True) -> None:
        ser = self.ser

        if start > stop:
            start, stop = stop, start
        if start < 10:
            logging.info('Set start frequency is out of range')
            start = 10
        if stop > 3 * 10 ** 8:
            logging.info('Set start frequency is out of range')
            stop = 3 * 10 ** 8

        str_start = 'STF ' + str(start) + 'HZ'
        str_stop = 'SOF ' + str(stop) + 'HZ'

        if log:
            str_log = 'LOG 1'
        else:
            str_log = 'LOG 0'

        ser.write((str_log + '; ' + str_start + '; ' + str_stop))

        ser.write_readline('STF?')
        ser.write_readline('SOF?')
        ser.write_readline('LOG?')

    def set_power(self, output_pow: float) -> None:
        ser = self.ser
        if 15 >= output_pow >= -6:
            ser.write('OPL ' + str(output_pow))
        else:
            logging.info('Set power out of range -6..15')
        ser.write_readline('OPL?')

    def set_meas_points(self, meas_points: int) -> None:
        ser = self.ser
        if 0 <= meas_points <= 6:
            ser.write('MEP ' + str(meas_points))
        else:
            logging.info('Set points number out of range 0..6')
        ser.write_readline('MEP?')

    def get_meas_points(self) -> int:
        MEP_str = self.ser.write_readline('MEP?')
        meas_points = self.MEP[int(MEP_str[-1])]
        return meas_points

    def set_RBW(self, RBW: int = 13) -> None:
        if 0 <= RBW <= 13:
            ser = self.ser
            ser.write('RBW ' + str(RBW))
        else:
            logging.info('Set RBW out of range 0..13')
        ser.write_readline('RBW?')

    def set_data_format(self, ch1_format: int = None, ch2_format: int = None) -> None:
        ser = self.ser
        if (ch1_format is not None):
            ser.write('ACCH 1')
            ser.write('TRC ' + str(ch1_format))
            ser.write_readline('TRC?')

        if (ch2_format is not None):
            ser.write('ACCH 2')
            ser.write('TRC ' + str(ch2_format))
            ser.write_readline('TRC?')

    def set_meas(self, ch1_meas: int = None, ch2_meas: int = None) -> None:
        ser = self.ser
        if ch1_meas is not None:
            ser.write('ACCH 1')
            ser.write('MEASPT ' + str(ch1_meas))
            ser.write_readline('MEASPT?')
        if ch2_meas is not None:
            ser.write('ACCH 1')
            ser.write('MEASPT ' + str(ch2_meas))
            ser.write_readline('MEASPT?')

    def set_channel(self, channel: str = 'all') -> None:
        ser = self.ser
        if channel is 'all':
            ser.write('SELCH 0')
        elif channel is 'ch1':
            ser.write('SELCH 1')
        elif channel is 'ch2':
            ser.write('SELCH 2')
        else:
            logging.info('Set channel is incorrect')
        ser.write_readline('SELCH?')

    def sweep(self, mode: str = 'single') -> None:
        ser = self.ser
        if mode is 'single':
            ser.write('SWP 1')
        elif mode is 'repeat':
            ser.write('SWP 0')
        elif mode is 'stop':
            ser.write('SWP 2')
        else:
            logging.info('Sweep parameter is incorrect')

    def auto_scale(self) -> None:
        ser = self.ser
        ser.write('SAU')

    def wait_sweep_stop(self) -> None:
        ser = self.ser
        flag = 1
        while flag:
            time.sleep(0.5)
            if ser.write_readline('SWP?') == '0':
                flag = 0

    def get_data(self, channel: 'str' = 'all', plot: bool = True, save: bool = True) -> None:
        """
        only single mode
        """
        ser = self.ser
        self.wait_sweep_stop()

        N = self.get_meas_points()

        def one_channel_read(fq_collumn=True):
            if fq_collumn:
                fq = ser.write_readlines('FQM? 0, ' + str(N))
                mag = ser.write_readlines('XMA? 0, ' + str(N))
                pha = ser.write_readlines('XMB? 0, ' + str(N))
                return fq, mag, pha
            else:
                mag = ser.write_readlines('XMA? 0, ' + str(N))
                pha = ser.write_readlines('XMB? 0, ' + str(N))
                return mag, pha

        if channel is 'all':
            dataChannel = pd.DataFrame(np.zeros((N, 5)), columns=['fq', 'mag1', 'pha1', 'mag2', 'pha2'])
            ser.write('SRW CH1')
            dataChannel['fq'], dataChannel['mag1'], dataChannel['pha1'] = one_channel_read()
            ser.write('SRW CH2')
            dataChannel['mag2'], dataChannel['pha2'] = one_channel_read(fq_collumn=False)
        elif channel is 'ch1':
            ser.write('SRW CH1')
            dataChannel = pd.DataFrame(np.zeros((N, 3)), columns=['fq', 'mag', 'pha'])
            dataChannel['fq'], dataChannel['mag'], dataChannel['pha'] = one_channel_read()
        elif channel is 'ch2':
            ser.write('SRW CH2')
            dataChannel = pd.DataFrame(np.zeros((N, 3)), columns=['fq', 'mag', 'pha'])
            dataChannel['fq'], dataChannel['mag'], dataChannel['pha'] = one_channel_read()
        else:
            logging.info('Uncorrect channel parameter in get data')

        if save:
            dataChannel.to_csv("dataChannel.csv")
        if plot:

            log = int(ser.write_readline('LOG?')[-1])

            if (channel is 'ch1') or (channel is 'ch2'):
                fig, axs = plt.subplots(nrows=1, ncols=2, sharex=True)
                ax = axs[0]
                ax.errorbar(dataChannel['fq'], dataChannel['mag'])
                ax.set_title('magnitude')
                if log:
                    ax.set_xscale('log')

                ax = axs[1]
                ax.errorbar(dataChannel['fq'], dataChannel['pha'])
                ax.set_title('phase')
                if log:
                    ax.set_xscale('log')

            elif channel is 'all':
                fig, axs = plt.subplots(nrows=1, ncols=2, sharex=True)
                ax = axs[0]
                ax.errorbar(dataChannel['fq'], dataChannel['mag1'])
                ax.errorbar(dataChannel['fq'], dataChannel['mag2'])
                ax.set_title('magnitude')
                if log:
                    ax.set_xscale('log')

                ax = axs[1]
                ax.errorbar(dataChannel['fq'], dataChannel['pha1'])
                ax.errorbar(dataChannel['fq'], dataChannel['pha2'])
                ax.set_title('phase')
                if log:
                    ax.set_xscale('log')

            fig.suptitle('data from ' + channel)
            plt.show()
