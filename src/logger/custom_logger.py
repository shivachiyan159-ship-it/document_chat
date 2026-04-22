import os
import logging
from datetime import datetime

class CustomLogger():
    def __init__(self):
        # 1.create folder
        self.LOG_FOLDER=os.path.join(os.getcwd(),"logs")
        os.makedirs(self.LOG_FOLDER,exist_ok=True)
        # 2.create filename path
        LOG_FILE_NAME = f"{datetime.now().strftime("%m_%d_%y")}.log"
        self.LOG_FILE_PATH=os.path.join(self.LOG_FOLDER,LOG_FILE_NAME)
       
    def get_logger(self,name=__file__):
        # for file handler
        file_handler=logging.FileHandler(self.LOG_FILE_PATH)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(message)s"))
        
        # for console
        console_handler=logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s"))
        
        logging.basicConfig( 
            level=logging.INFO,        
            format="%(message)s",
            handlers=[file_handler,console_handler]
        )
        
        return logging.getLogger(__name__)
    
if __name__ == "__main__":
      loggerobj=CustomLogger()
      logger=loggerobj.get_logger()
      logger.info("i am calling from custom logger")
      