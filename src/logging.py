import sys
import os
import logging
import datetime

LOG_FILE = f"{datetime.datetime.now().date()}.log"

logs_path = os.path.join(os.getcwd(), 'logs')

os.makedirs(logs_path, exist_ok= True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename = LOG_FILE_PATH,
    format = "[%(asctime)s] %(lineno)d - %(name)s - %(levelname)s - %(message)s ",
    level = logging.INFO

)