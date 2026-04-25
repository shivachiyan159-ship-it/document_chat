from src.logger import GLOBAL_LOGGER as log
from src.exception.custom_exception import CustomException
import logging
import sys
from pathlib import Path


def add(a,b):
    log.info("started add method")
    try:
     a = 9/0
    except Exception as e:
        log.error(e)
     #log.error(str(CustomException(e, sys)))
     # three scenarios we are handling
     #customobj=CustomException("Division failed")   
     #customobj=CustomException("Division failed", sys)
     #customobj=CustomException("Division failed", e)
     #print(customobj) # it will call __str__ method
        raise CustomException("Division failed", sys)


if __name__=="__main__":
    try:
        add(2,3)
    except CustomException as e:
       log.error(str(e))
   
    

