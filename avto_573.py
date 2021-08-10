#!/usr/bin/python3
"""
Скрипт для автоматического тестирования 573.
Логирование команд просисходит в консоле.
"""

import time  # библиотека для работы со временем
import subprocess  # библеотека для работы с командами и процессами ОС

from selenium import webdriver, common
# webdriver набор методов для управления браузером, common для контроля ошибок если сайт недоступен

# Функция возврата времени из файла log_time.py
from log_time import cmd_time

# Функции для тестирования EMAIL из файла test_email.py
import test_email

# Функция для тестирования IM из файла test_im.py
from test_im import start_im_test


VERSION = "v1.4.0"

def web_test(protocol: str, websait_list: list):
    # Функция для теста web соединений. Аргументы:
    # protocol - нужен для логирования;
    # websait_list - список сайтов для теста.

    # Логирование.
    print("\n\n{} start".format(protocol))
    print("----------------------------------------------------------------------------")
    print("Open browser")

    # Инициализируем драйвер браузера. После этой команды будет открыто новое окно браузера.
    driver = webdriver.Chrome()
    time.sleep(5)  # Пауза 5 секунд.

    # Итерации по элементам списка websait_list.
    for el in websait_list:

        print("\n{}\n{} {}".format(cmd_time(), protocol, el))  # Логирование.
        # Исключение для перенаправление ошибки заблокированых ресурсов.
        try:
            # Метод get сообщает браузеру, что нужно открыть сайт по указанной ссылке.
            driver.get(el)
        except common.exceptions.WebDriverException:
            print("***** WEB: CONTROL ERROR - NOT ANSWER *****")  # Логирование.
        time.sleep(10)  # Пауза 10 секунд.

    # Метод для закрытия окна браузера.
    driver.quit()
    driver.quit()  # Дублирование метода для надёжности, не всегда выполняется с первого раза.

    # Логирование.
    print("\nClose browser")
    print("----------------------------------------------------------------------------")
    return print("{} end".format(protocol))


def ftp_test(download_list: list):
    # Функция для теста ftp загрузки. Аргументы:
    # download_list - список ресурсрв для скачивания по ftp.

    # Логирование.
    print("\n\nFTP start")
    print("----------------------------------------------------------------------------")

    # Итерация по элементам списка download_list.
    for el in download_list:
        # Логирование.
        print("\n{}\nFTP {}".format(cmd_time(), el))
        print("Download {}\n".format(el[28:]))  # el[28:] - название файла, удаляется ftp://alta.ru/packets/distr/

        # Метод для выполнения команды в консоле, который ожидает завершения команды.
        # Команда для скачивания файлов >>> wget ftp://alta.ru/packets/distr/ts.zip
        subprocess.run(["wget", "-P", "FTP_573", el])
        time.sleep(60)  # Пауза 60 секунд.

    # Логирование.
    print("\n----------------------------------------------------------------------------")
    return print("FTP end")


def terminal_test(protocol: str, servers_list: list, ):
    # Функция для теста telnet и ssh соединений. Сам тест происходит с помощью putty. Аргументы:
    # protocol - для нужен определения протокола(telnet, ssh) и логирования;
    # servers_list - список серверных адресов для теста.

    # Логирование.
    print("\n\n{} start".format(protocol))
    print("----------------------------------------------------------------------------")

    # Определение протокола путём длинны аргумента protocol
    flag = "-telnet" if len(protocol) > 3 else "-ssh"

    # Итерация по элементам списка servers_list
    for el in servers_list:
        print("\n{}\n{} {}".format(cmd_time(), protocol, el))  # Логирование.

        # Метод для выполнения команды в консоле, который НЕ ожидает завершения команды и переходит к следующей строке.
        # Команда для соединения по указаному протоколу через putty >>> putty -ssh 195.144.107.198
        subprocess.Popen(["putty", flag, el])
        time.sleep(10)  # Пауза 10 секунд.

        # Исключение для завершения процесса putty в зависимости от ОС
        try:
            # Windows
            # Метод для выполнения команды в консоле, который ожидает завершения команды.
            subprocess.run(["taskkill", "/IM", "putty.exe", "/F"])
        except FileNotFoundError:
            # Linux
            # Метод для выполнения команды в консоле, который ожидает завершения команды.
            subprocess.run(["pkill", "putty"])
            print("***** TERM: CONTROL ERROR - NOT WINDOWS *****")

    # Логирование.
    print("\n----------------------------------------------------------------------------")
    return print("{} end".format(protocol))


# Список сайтов для теста http
http_list = ["http://kremlin.ru",
             "http://kremlin.ru/acts/constitution",
             "http://kremlin.ru/static/pdf/constitution.pdf?6fbd2dc717",
             "http://fsb.ru",
             "http://khann.ru",
             "http://khann.ru/wallpapers/",
             "http://alex-kuznetsov.ru/test",
             "http://www.thesheep.info",
             "http://www.grani.ru"]

# Список ресурсов для скачавания по ftp
ftp_list = ["ftp://alta.ru/packets/distr/ts.zip",
            "ftp://alta.ru/packets/distr/gtdw.zip",
            "ftp://alta.ru/packets/distr/maximum.zip"]

# Список серверных адресов для подключения по telnet
telnet_list = ["towel.blinkenlights.nl",
               "lord.stabs.org",
               "35.185.12.150"]

# Список серверных адресов для подключения по ssh
ssh_list = ["195.144.107.198",
            "sdf.org"]

# Список сайтов для теста https
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





# Постоянный цикл для запуска тестов и просмотра логирования. Постоянный для просмотра логирования,
# так как лог идёт в консоле без записи в файл. Выход из цикла осуществляется путём закрытия консоли.
while True:

    print(f"""Тестирование по 573 {VERSION}
    
1 - http        5 - ftp
2 - email       6 - telnet  
3 - im          7 - ssh 
4 - voip(None)  8 - https 
""")

    # Создание списка из введёной строки
    marker_test_list = [el for el in input("Какие тесты выполнять? (12345678)\n").strip()]

    # Логирование
    print("\n\n")
    print("START_" * 8)
    print(cmd_time(time_or_date="date"), end="")  # Логирование - дата

    # Условие для выполнения всех тестов.
    if len(marker_test_list) == 0:
        # Добавление в marker_test_list всех маркеров тестов.
        marker_test_list = ["1", "2", "3", "4", "5", "6", "7", "8"]

    while True:
        # Блок тестов с условием для запуска >>> Если маркер "X" есть в списке marker_test_list
        if "1" in marker_test_list:
            web_test("HTTP", http_list)
            marker_test_list.remove("1")

        if "2" in marker_test_list:

            test_email.i_sender()
            marker_test_list.remove("2")

        if "3" in marker_test_list:
            start_im_test()
            marker_test_list.remove("3")

        if "4" in marker_test_list:
            print("\nТест VOIP не готов!")  # Место для тестов voip
            marker_test_list.remove("4")

        if "5" in marker_test_list:
            ftp_test(ftp_list)
            marker_test_list.remove("5")

        if "6" in marker_test_list:
            terminal_test("TELNET", telnet_list)
            marker_test_list.remove("6")

        if "7" in marker_test_list:
            terminal_test("SSH", ssh_list)
            marker_test_list.remove("7")

        if "8" in marker_test_list:
            web_test("HTTPS", https_list)
            marker_test_list.remove("8")

        if len(marker_test_list) == 0:
            break

    # Логирование
    print()
    print(cmd_time(time_or_date="date"))  # Логирование - дата
    print("END___" * 8, "\n\n\n\n")
