"""
Скрипт для автоматического тестирования загрузки FTP.
"""

import os
import time


def cmd_time():
    # Месное время
    local_time = time.localtime()
    local_time_str = "{:0>2d}:{:0>2d}:{:0>2d}".format(local_time.tm_hour, local_time.tm_min, local_time.tm_sec)

    # UTC время
    utc_time = time.gmtime()
    utc_time_str = "{:0>2d}:{:0>2d}:{:0>2d}".format(utc_time.tm_hour, utc_time.tm_min, utc_time.tm_sec)

    return "{} (utc {})".format(local_time_str, utc_time_str)


def ftp_test(download_list: list):
    print("\n\nFTP start")
    print("----------------------------------------------------------------------------")

    for el in download_list:
        print("\n{}\nFTP {}".format(cmd_time(), el))
        print("Download {}\n".format(el[28:]))
        os.system("wget {}".format(el))
        time.sleep(60)

    print("\n----------------------------------------------------------------------------")
    return print("FTP end")




ftp_list = ["ftp://alta.ru/packets/distr/ts.zip",
            "ftp://alta.ru/packets/distr/gtdw.zip",
            "ftp://alta.ru/packets/distr/maximum.zip"]
ftp_test(ftp_list)

