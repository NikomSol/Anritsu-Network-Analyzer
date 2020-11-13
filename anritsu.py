import serial
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re


class Anritsu:
    def __init__(self, serial):
        self.ser = serial
        self.sleep = 0.1
        self.clear_input()

    def set_freq(self, start, stop, log=True):
        ser = self.ser
        if ((type(start) is float) or (type(start) is int)) and ((type(stop) is float) or (type(stop) is int)) and (
                stop > start):
            str_start = 'STF ' + str(start) + 'HZ'
            str_stop = 'SOF ' + str(stop) + 'HZ'
            if log:
                str_log = 'LOG 1'
            else:
                str_log = 'LOG 0'

            ser.write((str_log + '; ' + str_start + '; ' + str_stop + ' \n').encode('utf-8'))
        else:
            print('data type error')

        sleep = self.sleep
        ser.write(b'STF? \n')
        time.sleep(sleep)
        start = ser.readline()

        ser.write(b'SOF? \n')
        time.sleep(sleep)
        stop = ser.readline()

        ser.write(b'LOG? \n')
        time.sleep(sleep)
        log = ser.readline()

        return start, stop, log

    def set_power(self, output_pow):
        ser = self.ser
        if 15 >= output_pow >= -6:
            ser.write(('OPL ' + str(output_pow) + '\n').encode('utf-8'))
        else:
            print('output out diapasone')

        ser.write(b'OPL? \n')
        time.sleep(self.sleep)
        return ser.readline()

    def set_poins(self, points):
        """
        N = [11, 21, 51, 101, 251, 501, 1001][MEP]
        """
        if 0 <= points <= 6:
            ser = self.ser
            ser.write(('MEP ' + str(points) + '\n').encode('utf-8'))
        else:
            print('uncorrect points value')

        ser.write(b'MEP? \n')
        time.sleep(self.sleep)
        return ser.readline()

    def set_RBW(self, RBW=13):
        """
        0: 3Hz
        1: 10Hz
        2: 30Hz
        3: 100Hz
        4: 300Hz
        5: 1kHz
        6: 3kHz
        7: 10kHz
        8: 500Hz
        9: 2kHz
        10: 4kHz
        11: 5kHz
        12: 20kHz
        13:AUTO
        """
        if 0 <= RBW <= 13:
            ser = self.ser
            ser.write(('RBW ' + str(RBW) + '\n').encode('utf-8'))
        else:
            print('uncorrect RBW value')

        ser.write(b'RBW? \n')
        time.sleep(self.sleep)
        return ser.readline()

    def set_format(self, format, channel='all'):
        """
        0: LOGMAG
        1: PHASE
        2: DELAY
        3: MAG & PHASE
        4: MAG & DELAY
        5: POLAR
        6: IMPD
        CHART
        7: ADMT
        CHART
        8: VSWR
        9: LINMAG
        10: LIN & PHASE
        11: LIN & DELAY
        12: REAL
        13: IMAG
        14: REAL & IMAG
        15: LOG
        Z
        16: LOG
        Z & θ
        17: Q
        18: LOG Z & Q
        """
        ser = self.ser
        form1 = None
        form2 = None
        if (channel is 'ch1') or (channel is 'all'):
            ser.write(b'ACCH 1 \n')
            ser.write(('TRC ' + str(format) + ' \n').encode('utf-8'))
            ser.write(b'TRC? \n')
            time.sleep(self.sleep)
            form1 = ser.readline()
        if (channel is 'ch2') or (channel is 'all'):
            ser.write(b'ACCH 2 \n')
            ser.write(('TRC ' + str(format) + ' \n').encode('utf-8'))
            ser.write(b'TRC? \n')
            time.sleep(self.sleep)
            form2 = ser.readline()
        return form1, form2

    def set_meas(self, meas, channel='all'):
        """
        0:TB/TA
        1: TA/R
        2: TB/R
        3:TA
        4:TB
        5:R
        """
        ser = self.ser
        meas1 = None
        meas2 = None
        if (channel is 'ch1') or (channel is 'all'):
            ser.write(b'ACCH 1 \n')
            ser.write(('MEASPT ' + str(meas) + ' \n').encode('utf-8'))
            ser.write(b'MEASPT? \n')
            time.sleep(self.sleep)
            meas1 = ser.readline()
        if (channel is 'ch2') or (channel is 'all'):
            ser.write(b'ACCH 2 \n')
            ser.write(('MEASPT ' + str(meas) + ' \n').encode('utf-8'))
            ser.write(b'MEASPT? \n')
            time.sleep(self.sleep)
            meas2 = ser.readline()

        return meas1, meas2

    def set_channel(self, channel='all'):
        ser = self.ser
        if channel is 'all':
            ser.write(b'SELCH 0 \n')
        elif channel is 'ch1':
            ser.write(b'SELCH 1 \n')
        elif channel is 'ch2':
            ser.write(b'SELCH 2 \n')

        ser.write(b'SELCH? \n')
        time.sleep(self.sleep)
        return ser.readline()

    def sweep(self, mode):
        ser = self.ser
        if mode is 'single':
            ser.write(b'SWP 1 \n')
        elif mode is 'repeat':
            ser.write(b'SWP 0 \n')
        else:
            print('unknown sweep mode')

    def wait_sweep_stop(self):
        ser = self.ser
        sleep = self.sleep
        flag = 1
        while flag:
            time.sleep(sleep)
            ser.write(b'SWP? \n')
            if (ser.readline() == b'0\n'):
                flag = 0

    def clear_input(self):
        ser = self.ser
        flag = 1
        while flag:
            flag = len(ser.readline())

    def _get_data_N(self, N):
        time.sleep(self.sleep)
        ser = self.ser
        data = np.zeros(N)
        for i in range(N):
            str = self.ser.readline()
            if str is not b'':
                data[i] = float(str.decode('utf-8'))
        return data

    def get_data(self, channel='all', plot=True, save=True):
        """
        only single mode
        only mag & phase mode
        """
        ser = self.ser
        sleep = self.sleep

        self.wait_sweep_stop()

        self.clear_input()
        ser.write(b'MEP? \n')
        time.sleep(sleep)
        MEP_str = ser.readline()
        MEP = int(MEP_str.decode('utf-8')[-2])
        N = [11, 21, 51, 101, 251, 501, 1001][MEP]

        def one_channel_read():
            self.clear_input()
            ser.write(('FQM? 0, ' + str(N) + ' \n').encode('utf-8'))
            fq = self._get_data_N(N)

            self.clear_input()
            ser.write(('XMA? 0, ' + str(N) + ' \n').encode('utf-8'))
            mag = self._get_data_N(N)

            self.clear_input()
            ser.write(('XMB? 0, ' + str(N) + ' \n').encode('utf-8'))
            pha = self._get_data_N(N)

            return fq, mag, pha

        if channel is 'all':
            dataChannel = pd.DataFrame(np.zeros((N, 5)), columns=['fq', 'mag1', 'pha1', 'mag2', 'pha2'])
            ser.write(b'SRW CH1 \n')
            dataChannel['fq'], dataChannel['mag1'], dataChannel['pha1'] = one_channel_read()
            ser.write(b'SRW CH2 \n')
            buf, dataChannel['mag2'], dataChannel['pha2'] = one_channel_read()
        elif channel is 'ch1':
            ser.write(b'SRW CH1 \n')
            dataChannel = pd.DataFrame(np.zeros((N, 3)), columns=['fq', 'mag', 'pha'])
            dataChannel['fq'], dataChannel['mag'], dataChannel['pha'] = one_channel_read()
        elif channel is 'ch2':
            ser.write(b'SRW CH2 \n')
            dataChannel = pd.DataFrame(np.zeros((N, 3)), columns=['fq', 'mag', 'pha'])
            dataChannel['fq'], dataChannel['mag'], dataChannel['pha'] = one_channel_read()
        else:
            print('uncorrect channel')

        if save:
            dataChannel.to_csv("dataChannel.csv")
        if plot:
            ser.write(b'LOG? \n')
            time.sleep(sleep)
            log = int(ser.readline().decode('utf-8')[-2])

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
