import serial
import serial.tools.list_ports
import logging
import time


class MySerial:
    def __init__(self, setup_file=False,
                 com=False, baud=9600, parity='NONE', stopbits=1, bytesize=8,
                 timeout=0.1, answer_time=0.1,
                 terminator='LN', terminator_space=True,
                 logging_message=True):
        """
        :param setup_file:  filename:str if use serial setup from file or False if setup from code
        :param com: "COM X"  or False - auto finding free com
        :param baud: {19200,9600,4800,2400,1200}
        :param parity: {"NONE",}
        :param stopbits: {1,2}
        :param bytesize: {7,8}
        :param timeout: time wait answer
        :param answer_time: sleep time between write and read
        :param terminator: {'LN', 'CR', 'CRLN','LNCR'}
        :param terminator_space: {True, False} space before terminator
        :param logging_message: {False, True, 'all'} 'all' if you want to logging multiline answers
        """
        if setup_file:
            com, baud, parity, stopbits, bitesize = self.get_settings_from_file(setup_file)

        # Search all coms and use first
        if not com:
            coms = list(serial.tools.list_ports.comports())
            try:
                com = coms[0][0]
            except Exception:
                logging.ERROR('There is not available COM')
                raise

        if baud not in {19200, 9600, 4800, 2400, 1200}:
            logging.ERROR('Unknown baud: ' + str(baud))

        # GEO - really? Before setting all the settings as stopbits etc. ?
        try:
            ser = serial.Serial(
                port=com,
                baudrate=baud,
                timeout=timeout
            )
        except Exception:
            logging.ERROR('Can not open serial')
            raise

        if parity is 'NONE':
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

        if terminator_space:
            self.terminator = ' ' + self.terminator

        self.answer_time = answer_time
        self.logging_message = logging_message

    # TODO parameters typing
    def get_settings_from_file(self, setup_file):
        """
        TODO
        :param setup_file:
        :return:
        """
        try:
            open(setup_file)
        except Exception:
            logging.ERROR('There is not settings serial file')
            raise

    def close(self) -> None:
        ser = self.ser
        ser.close()
        assert not ser.isOpen()
        logging.INFO('Serial is close')

    def write(self, message: str) -> None:
        ser = self.ser
        bmessage = (message + self.terminator).encode('unf-8')
        ser.write(bmessage)
        if self.logging_message:
            logging.INFO(b'serial write: ' + bmessage)

    # TODO return parameter typing == str?
    def write_readline(self, message: str):
        ser = self.ser
        bmessage = (message + self.terminator).encode('unf-8')
        ser.write(bmessage)
        if self.logging_message:
            logging.INFO(b'serial write: ' + bmessage)

        time.sleep(self.answer_time)
        answer = ser.readline()
        if self.logging_message:
            logging.INFO(b'serial read: ' + answer)

        return answer.decode('uts-8').rstrip('\n')

    # TODO return parameter typing == str?
    # TODO argument names should be lowercase
    def write_readlines(self, message: str, N: int = 0):
        """
        :param message: TODO
        :param N: int - number of lines if 0 - read while not empty lines
        :return: list of str without '\n'
        """
        ser = self.ser
        logging_message = self.logging_message
        bmessage = (message + self.terminator).encode('unf-8')
        ser.write(bmessage)
        if logging_message:
            logging.INFO(b'serial write: ' + bmessage)

        time.sleep(self.answer_time)

        if N:
            answer = N * []
            for i in range(N):
                answer[i] = ser.readline()
                if logging_message == 'all':
                    logging.INFO(b'serial read: ' + answer[i])
                answer[i].decode('utf-8').rstrip('\n')
        else:
            flag = 1
            answer = ''
            while flag:
                buf = ser.readline()
                if logging_message == 'all':
                    logging.INFO(b'serial read: ' + buf)
                answer += buf
                flag = len(buf)
            answer.decode('utf-8')
            answer.split('\n')

        return answer

    def clear_input(self) -> None:
        ser = self.ser
        logging_message = self.logging_message
        flag = 1
        while flag:
            buf = ser.readline()
            if logging_message == 'all':
                logging.INFO(b'serial read (clear_input): ' + buf)
            flag = len(buf)