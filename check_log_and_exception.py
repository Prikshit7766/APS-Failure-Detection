#  This file is for personal under standing to see how loging and exception are working in the project
from sensor.exception import SensorException
from sensor.logger import logging
import sys

def test_logger_and_exception():
    try:
        logging.info("staring the test_logger_and_eception")
        result =3/0
        print(result)
        logging.info("stoping the test_logger_and_exception ")
    except Exception as e:
        logging.debug(str(e))  # it will  no show up as we set our loger lev as info
        raise SensorException(e, sys)
    


if __name__=="__main__":
    try:
        test_logger_and_exception()
    except Exception as e:
        print(e)