import logging
from log_time import cmd_time # Функция возврата времени из файла log_time.py
import os

try:
    os.mkdir("logs")
    os.chdir("./logs")
except:
    os.chdir("./logs")

logging.basicConfig(filename=cmd_time("for_log")+".log", level=logging.INFO)

os.getcwd()


logging.info("Informational message")
logging.error("An error has happened!")



logging.basicConfig(filename=cmd_time("for_log")+".log", level=logging.INFO)
