import logging

from myserial import Serial

def test_simple_open():
    ser = Serial()
    ser.close()

def test_settings_open():
    ser = Serial(setup_file=False,
                 com=False, baud=9600, parity='NONE', stopbits=1, bytesize=8,
                 timeout=0.1, answer_time=0.1,
                 terminator='LN', terminator_space=True,
                 logging_message=True)
    ser.close()

def test_filesettings_open():
    ser = Serial(setup_file='myfile.txt',
                 com=False, baud=9600, parity='NONE', stopbits=1, bytesize=8,
                 timeout=0.1, answer_time=0.1,
                 terminator='LN', terminator_space=True,
                 logging_message=True)
    ser.close()

def test_write_str():
    ser = Serial()
    ser.write('abc')
    ser.close()

def test_write_num():
    ser = Serial()
    with pytest.raises(TypeError):
            ser.write(1)

def test_write_readlines():
    ser = Serial(logging_message='all')
    n = 3
    assert ser.write_readlines('aa', lines_number=n) == n * [b'']
    ser.close()



if __name__ == '__main__':
    logging.basicConfig(filename="INFO.log", level=logging.INFO, filemode='w')

    test_simple_open()
    test_settings_open()
    # test_filesettings_open()
    test_write_str()
    # test_write_num()
    test_write_readlines()
