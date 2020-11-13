import serial
import time
import numpy as np
import pandas as pd
import re

class Anritsu:
    def __init__(self, serial):
        self.ser = serial

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
        flag = 1
        while flag:
            time.sleep(0.1)
            ser.write(b'SWP? \n')
            if (ser.readline() == b'0\n'):
                flag = 0

    def read_data(self, N):
        time.sleep(0.5)
        ser = self.ser
        data = np.zeros(N)
        for i in range(N):
            str = self.ser.readline()
            if str is not b'':
                data[i] = float(str.decode('utf-8'))
        return data

    def clear_input(self):
        ser = self.ser
        flag = 1
        while flag:
            flag = len(ser.readline())

    # def read_chanel_data(self):
    #
    #
    # N = 101
    # dataChannel = pd.DataFrame(np.zeros((N, 3)), columns=['fq', 'mag', 'pha'])
    # # ser.write(('XMA? 0, '+str(N)+' \n').encode('utf-8'))
    #
    # clear_input()
    # ser.write(('FQM? 0, ' + str(N) + ' \n').encode('utf-8'))
    # dataChannel['fq'] = read_data(N)
    #
    # clear_input()
    # ser.write(('XMA? 0, ' + str(N) + ' \n').encode('utf-8'))
    # dataChannel['mag'] = read_data(N)
    #
    # clear_input()
    # ser.write(('XMB? 0, ' + str(N) + ' \n').encode('utf-8'))
    # dataChannel['pha'] = read_data(N)
    #
    # dataChannel.to_csv("dataChannel.csv")
    #
    # fig, axs = plt.subplots(nrows=1, ncols=2, sharex=True)
    # ax = axs[0]
    # ax.errorbar(dataChannel['fq'], dataChannel['mag'])
    # ax.set_title('magnitude')
    #
    # ax = axs[1]
    # ax.errorbar(dataChannel['fq'], dataChannel['pha'])
    # ax.set_title('phase')
    #
    # fig.suptitle('data from channel')