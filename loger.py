
import logging
from log_time import cmd_time # Функция возврата времени из файла log_time.py

# add filemode="w" to overwrite
print(cmd_time)
logging.basicConfig(filename=cmd_time()+".log", level=logging.INFO)

logging.debug("This is a debug message")
logging.info("Informational message")
logging.error("An error has happened!")
