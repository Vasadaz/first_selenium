#!/usr/bin/python3
"""
Скрипт для автоматического тестирования 573.
Логирование команд просисходит в консоле.
"""

import time  # библиотека для работы со временем
import subprocess  # библеотека для работы с командами и процессами ОС

from selenium import webdriver  # webdriver это набор методов для управления браузером


def cmd_time(time_or_date="time") -> str:
    # Функция для возврата месного и GMT времения
    # time_or_date - маркер для возврата времени(time_or_date="time") или даты(time_or_date="date")
    # По умолчанию time_or_date="time"
    # Месное дата и время
    local_time = time.localtime()
    # GMT дата и время
    gmt_time = time.gmtime()

    # Условие для возврата даты или времени.
    if time_or_date == "time":
        # Форматирование времени в привычный вид, т.е. из 1:14:3 в 01:14:03.
        # tm_hour, tm_min, tm_sec методы для возвращения единиц времени.
        # Месное время
        local_time_str = "{:0>2d}:{:0>2d}:{:0>2d}".format(local_time.tm_hour, local_time.tm_min, local_time.tm_sec)
        # GMT время
        gmt_time_str = "{:0>2d}:{:0>2d}:{:0>2d}".format(gmt_time.tm_hour, gmt_time.tm_min, gmt_time.tm_sec)
        # Возврат времени в формате "чч:мм:сс (GMT чч:мм:сс)"
        return "{} (GMT {})".format(local_time_str, gmt_time_str)
    else:
        # Форматирование дыты в привычный вид, т.е. из 1:14:3 в 01:14:03.
        # tm_hour, tm_min, tm_sec методы для возвращения единиц времени.
        # Месное время
        local_time_str = "{:0>2d}.{:0>2d}.{:4d}".format(local_time.tm_mday, local_time.tm_mon, local_time.tm_year)
        # GMT время
        gmt_time_str = "{:0>2d}:{:0>2d}:{:0>2d}".format(gmt_time.tm_mday, gmt_time.tm_mon, gmt_time.tm_year)
        # Возврат времени в формате "чч:мм:сс (GMT чч:мм:сс)"
        return "DATE {} (GMT {})".format(local_time_str, gmt_time_str)




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
        except:
            print("***** CONTROL ERROR *****")  # Логирование.
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
        subprocess.run(["wget", el])
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

    print("""Тестирование по 573. Можно запустить отдельные тесты вводя их номер:
    1 - http    4 - ssh
    2 - ftp     5 - https 
    3 - telnet  Все - пустая строка.""")


    # Создание списка из введёной строки
    marker_test_list = [el for el in input("\nКакие тесты выполнять?\n").strip()]

    # Логирование
    print("\n\n")
    print("START " * 8)
    print(cmd_time(time_or_date="date"), end="")  # Логирование - дата

    # Условие для выполнения всех тестов.
    if len(marker_test_list) == 0:
        # Добавление в marker_test_list всех маркеров тестов.
        marker_test_list = ["1", "2", "3", "4", "5"]

    # Блок тестов с условием для запуска >>> Если маркер "X" есть в списке marker_test_list
    web_test("HTTP", http_list) if "1" in marker_test_list else None
    ftp_test(ftp_list) if "2" in marker_test_list else None
    terminal_test("TELNET", telnet_list) if "3" in marker_test_list else None
    terminal_test("SSH", ssh_list) if "4" in marker_test_list else None
    web_test("HTTPS", https_list) if "5" in marker_test_list else None

    # Логирование
    print()
    print(cmd_time(time_or_date="date"))  # Логирование - дата
    print("END   " * 8 , "\n\n\n\n")
