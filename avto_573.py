"""
Скрипт для автоматического тестирования 573
"""

import time  # библиотека для работы со временем
import subprocess  # библеотека для работы с командами и процессами ОС
from selenium import webdriver  # webdriver это набор методов для управления браузером

def cmd_time():
    # Месное время
    local_time = time.localtime()
    local_time_str = "{:0>2d}:{:0>2d}:{:0>2d}".format(local_time.tm_hour, local_time.tm_min, local_time.tm_sec)

    # UTC время
    utc_time = time.gmtime()
    utc_time_str = "{:0>2d}:{:0>2d}:{:0>2d}".format(utc_time.tm_hour, utc_time.tm_min, utc_time.tm_sec)

    return "{} (utc {})".format(local_time_str, utc_time_str)

def web_test(protocol: str, sait_list: list):
    print("\n\n{} start".format(protocol))
    print("----------------------------------------------------------------------------")
    print("Open browser")

    # Инициализируем драйвер браузера. После этой команды вы должны увидеть новое открытое окно браузера
    driver = webdriver.Chrome()
    time.sleep(5)

    for el in sait_list:
        print("\n{}\n{} {}".format(cmd_time(), protocol, el))
        # Перенаправление ошибки вдля заблокированых ресурсов
        try:
            # Метод get сообщает браузеру, что нужно открыть сайт по указанной ссылке
            driver.get(el)
        except:
            print("***** CONTROL ERROR *****")
        time.sleep(10)

    # После выполнения всех действий мы должны не забыть закрыть окно браузера
    driver.quit()
    driver.quit()

    print("\nClose browser")
    print("----------------------------------------------------------------------------")
    return print("{} end".format(protocol))


def ftp_test(download_list: list):
    print("\n\nFTP start")
    print("----------------------------------------------------------------------------")

    for el in download_list:
        print("\n{}\nFTP {}".format(cmd_time(), el))
        print("Download {}\n".format(el[28:]))
        subprocess.run(["wget", el])
        time.sleep(60)

    print("\n----------------------------------------------------------------------------")
    return print("FTP end")


def terminal_test(protocol: str, hosts_list: list, ):
    print("\n\n{} start".format(protocol))
    print("----------------------------------------------------------------------------")

    flag = "-telnet" if len(protocol) > 3 else "-ssh"

    for el in hosts_list:
        print("\n{}\n{} {}".format(cmd_time(), protocol, el))
        subprocess.Popen(["putty", flag, el])
        time.sleep(10)
        subprocess.run("taskkill /IM putty.exe /F")

    print("\n----------------------------------------------------------------------------")
    return print("{} end".format(protocol))


http_list = ["http://kremlin.ru",
             "http://kremlin.ru/acts/constitution",
             "http://kremlin.ru/static/pdf/constitution.pdf?6fbd2dc717",
             "http://fsb.ru",
             "http://khann.ru",
             "http://khann.ru/wallpapers/",
             "http://alex-kuznetsov.ru/test",
             "http://www.thesheep.info",
             "http://www.grani.ru"]

ftp_list = ["ftp://alta.ru/packets/distr/ts.zip",
            "ftp://alta.ru/packets/distr/gtdw.zip",
            "ftp://alta.ru/packets/distr/maximum.zip"]

telnet_list = ["towel.blinkenlights.nl",
               "lord.stabs.org",
               "35.185.12.150"]

ssh_list = ["195.144.107.198",
            "sdf.org"]

https_list = ["https://yandex.ru",
              "https://mail.ru",
              "https://rambler.ru",
              "https://2ip.ru",
              "https://cia.gov",
              "https://nsa.gov",
              "https://ssu.gov.ua",
              "https://mossad.gov.il",
              "https://sis.gov.uk",
              "https://bnd.bund.de"]

while True:
    print("\nКакие тесты выполнять? Все - ENTER")
    marker_test_list = [el for el in input().strip()]

    if len(marker_test_list) == 0:
        marker_test_list = ["1", "2", "3", "4", "5"]

    web_test("HTTP", http_list) if "1" in marker_test_list else None
    ftp_test(ftp_list) if "2" in marker_test_list else None
    terminal_test("TELNET", telnet_list) if "3" in marker_test_list else None
    terminal_test("SSH", ssh_list) if "4" in marker_test_list else None
    web_test("HTTPS", https_list) if "5" in marker_test_list else None
