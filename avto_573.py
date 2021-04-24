"""
Скрипт для автоматического тестирования 573.
Логирование команд просисходит в консоле.
Для работы кода нужно стороннее ПО:
1) Python 3.9 с прописыванием в среду переменных PATH;
2) Putty;
3) Папка chromedriver скопирована в C:\ и прописанна в среду переменных PATH.
"""

import time  # библиотека для работы со временем
import subprocess  # библеотека для работы с командами и процессами ОС
from selenium import webdriver  # webdriver это набор методов для управления браузером

def cmd_time():
    # Функция для возврата месного и GMT времения

    # Месное время
    local_time = time.localtime()
    # Форматирование времени в привычный вид, т.е. из 1:14:3 в 01:14:03.
    # tm_hour, tm_min, tm_sec методы для возвращения единиц времени.
    local_time_str = "{:0>2d}:{:0>2d}:{:0>2d}".format(local_time.tm_hour, local_time.tm_min, local_time.tm_sec)

    # GMT время
    gmt_time = time.gmtime()
    gmt_time_str = "{:0>2d}:{:0>2d}:{:0>2d}".format(gmt_time.tm_hour, gmt_time.tm_min, gmt_time.tm_sec)

    return "{} (UTC {})".format(local_time_str, gmt_time_str)

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
        # Перенаправление ошибки для заблокированых ресурсов.
        try:
            # Метод get сообщает браузеру, что нужно открыть сайт по указанной ссылке.
            driver.get(el)
        except:
            print("***** CONTROL ERROR *****")  # Логирование.
        time.sleep(10) # Пауза 10 секунд.

    # Метод для закрытия окна браузера.
    driver.quit()
    driver.quit() # Дублирование метода для надёжности, не всегда выполняется с первого раза.

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
        time.sleep(60) # Пауза 60 секунд.

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
        print("\n{}\n{} {}".format(cmd_time(), protocol, el)) # Логирование.

        # Метод для выполнения команды в консоле, который НЕ ожидает завершения команды и переходит к следующей строке.
        # Команда для соединения по указаному протоколу через putty >>> putty -ssh 195.144.107.198
        subprocess.Popen(["putty", flag, el])
        time.sleep(10) # Пауза 10 секунд.

        # Метод для выполнения команды в консоле, который ожидает завершения команды.
        # Команда для завершения процесса putty >>> putty -ssh 195.144.107.198
        subprocess.run("taskkill /IM putty.exe /F")

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

# Вечный цикл для запуска тестов и просмотра логирования. Вечный для просмотра логирования.
# Выход из цикла осуществляется путём закрытия консоли.
while True:
    print("\nКакие тесты выполнять? Все - ENTER")
    marker_test_list = [el for el in input().strip()]

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
