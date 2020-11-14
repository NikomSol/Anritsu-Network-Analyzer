import serial
import serial.tools.list_ports
import logging
import time


class Myserial:
    def __init__(self, file=False, com=False, baud=9600, parity='NONE', stopbits=1, bytesize=8,
                 timeout=0.1, answertime=0.1,
                 terminator='LN', terminator_spase=True,
                 logging_massage='single'):

        if file:
            com, baud, parity, stopbits, bitesize = self.get_settings_from_file(file)

        if not com:
            coms = list(serial.tools.list_ports.comports())
            try:
                com = coms[0][0]
            except Exception:
                logging.ERROR('There is not available COM')
                raise

        try:
            ser = serial.Serial(
                port=com,
                baudrate=baud,
                timeout=timeout
            )
        except Exception:
            logging.ERROR('Can not open serial')
            raise

        if parity is "NONE":
            ser.parity = serial.PARITY_NONE
        else:
            logging.ERROR('Unknown parity: ' + str(parity))
            raise ValueError
        if stopbits == 1:
            ser.stopbits = serial.STOPBITS_ONE
        elif stopbits == 2:
            ser.stopbits = serial.STOPBITS_TWO
        else:
            logging.ERROR('Unknown stopbits: ' + str(stopbits))
            raise ValueError

        if bytesize == 8:
            ser.bytesize = serial.EIGHTBITS
        elif bytesize == 7:
            ser.bytesize = serial.SEVENBITS
        else:
            logging.ERROR('Unknown bytesize: ' + str(bytesize))
            raise ValueError

        assert ser.isOpen()
        logging.INFO('Serial is open')
        self.ser = ser

        if terminator == 'LN':
            self.terminator = '\n'
        elif terminator == 'CR':
            self.terminator = '\r'
        elif terminator == 'LNCR':
            self.terminator = '\n\r'
        elif terminator == 'CRLN':
            self.terminator = '\n\r'
        else:
            logging.ERROR('Unknown terminator: ' + str(terminator))
            raise ValueError

        if terminator_spase:
            self.terminator = ' ' + self.terminator

        self.answertime = answertime
        self.logging_massage = logging_massage

    def get_settings_from_file(self, file):
        try:
            open('settings_serial.txt')
        except Exception:
            logging.ERROR('There is not settings serial file')
            raise

    def close(self):
        ser = self.ser
        ser.close()
        assert not ser.isOpen()
        logging.INFO('Serial is close')

    def write(self, massage):
        ser = self.ser
        bmassage = (massage + self.terminator).encode('unf-8')
        ser.write(bmassage)
        if self.logging_massage:
            logging.INFO(b'serial write: ' + bmassage)

    def write_readline(self, massage):
        ser = self.ser
        bmassage = (massage + self.terminator).encode('unf-8')
        ser.write(bmassage)
        if self.logging_massage:
            logging.INFO(b'serial write: ' + bmassage)

        time.sleep(self.answertime)
        answer = ser.readline()
        if self.logging_massage:
            logging.INFO(b'serial read: ' + answer)

        return answer.decode('uts-8').rstrip('\n')

    def write_readlines(self, massage, N=False):
        ser = self.ser
        logging_massage = self.logging_massage
        bmassage = (massage + self.terminator).encode('unf-8')
        ser.write(bmassage)
        if logging_massage:
            logging.INFO(b'serial write: ' + bmassage)

        time.sleep(self.answertime)

        if N:
            answer = N * []
            for i in range(N):
                answer[i] = ser.readline()
                if logging_massage == 'all':
                    logging.INFO(b'serial read: ' + answer[i])
                answer[i].decode('utf-8').rstrip('\n')
        else:
            flag = 1
            answer = ''
            while flag:
                buf = ser.readline()
                if logging_massage == 'all':
                    logging.INFO(b'serial read: ' + buf)
                answer += buf
                flag = len(buf)
            answer.decode('utf-8')
            answer.split('\n')

        return answer

    def clear_input(self):
        ser = self.ser
        logging_massage = self.logging_massage
        flag = 1
        while flag:
            buf = ser.readline()
            if logging_massage == 'all':
                logging.INFO(b'serial read (clear_input): ' + buf)
            flag = len(buf)
