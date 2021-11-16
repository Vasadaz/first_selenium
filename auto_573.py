#!/usr/bin/python3
"""
Скрипт для автоматического тестирования 573.
Логирование команд происходит в консоли.
"""
import time
import subprocess  # библиотека для работы с командами и процессами ОС
import os
import shutil  # Для удаления папки FTP
# webdriver набор методов для управления браузером, common для контроля ошибок если сайт недоступен
from selenium import webdriver, common
import test_email  # Функции для тестирования EMAIL из файла test_email.py
import test_im  # Функция для тестирования IM из файла test_im.py
# Импорт логирования
from loger import cmd_time, RELEASE, print_in_log, file_for_log


def web_test(protocol: str, websait_list: list):
    # Функция для теста web соединений. Аргументы:
    # protocol - нужен для логирования;
    # websait_list - список сайтов для теста.

    # Логирование.
    print_in_log(f"\n\n{protocol}")
    print_in_log("----------------------------------------------------------------------------")
    print_in_log("Open browser")

    # Инициализируем драйвер браузера. После этой команды будет открыто новое окно браузера.
    driver = webdriver.Chrome()
    time.sleep(5)  # Пауза 5 секунд.

    # Итерации по элементам списка websait_list.
    for el in websait_list:

        print_in_log(f"\n{cmd_time()}\n{protocol} {el}")  # Логирование.
        # Исключение для перенаправление ошибки заблокированных ресурсов.
        try:
            # Метод get сообщает браузеру, что нужно открыть сайт по указанной ссылке.
            driver.get(el)
        except common.exceptions.WebDriverException:
            print_in_log("***** WEB: CONTROL ERROR - NOT ANSWER *****")  # Логирование.
        time.sleep(10)  # Пауза 10 секунд.

    # Метод для закрытия окна браузера.
    driver.quit()
    driver.quit()  # Дублирование метода для надёжности, не всегда выполняется с первого раза.

    # Логирование.
    print_in_log("\nClose browser")
    print_in_log("----------------------------------------------------------------------------")
    return print_in_log(f"{protocol} end")


def ftp_test(download_list: list):
    # Функция для теста ftp загрузки. Аргументы:
    # download_list - список ресурсов для скачивания по ftp.

    # Логирование.
    print_in_log("\n\nFTP")
    print_in_log("----------------------------------------------------------------------------")

    try:
        shutil.rmtree("./FTP_573")  # Удаление папки для экономии места
    except FileNotFoundError:
        pass

    # Итерация по элементам списка download_list.
    for el in download_list:
        # Логирование.
        print_in_log(f"\n{cmd_time()}\nFTP {el}")
        print_in_log(f"Download {el[28:]}")  # el[28:] - название файла, удаляется ftp://alta.ru/packets/distr/

        # Метод для выполнения команды в консоли, который ожидает завершения команды.
        # Команда для скачивания файлов >>> wget ftp://alta.ru/packets/distr/ts.zip
        subprocess.run(["wget", "-P", "FTP_573", el])
        print_in_log(f"End {cmd_time()} {el[28:]} {os.path.getsize(f'./FTP_573/{el[28:]}')} Byte")
        time.sleep(60)  # Пауза 60 секунд.

    # Логирование.
    print_in_log("\n----------------------------------------------------------------------------")
    print_in_log("FTP end")


def terminal_test(protocol: str, servers_list: list, ):
    # Функция для теста telnet и ssh соединений. Сам тест происходит с помощью putty. Аргументы:
    # protocol - для нужен определения протокола(telnet, ssh) и логирования;
    # servers_list - список серверных адресов для теста.

    # Логирование.
    print_in_log(f"\n\n{protocol}")
    print_in_log("----------------------------------------------------------------------------")

    # Определение протокола путём длинны аргумента protocol
    flag = "-telnet" if len(protocol) > 3 else "-ssh"

    # Итерация по элементам списка servers_list
    for el in servers_list:
        print_in_log(f"\n{cmd_time()}\n{protocol} {el}")  # Логирование.

        # Метод для выполнения команды в консоли, который НЕ ожидает завершения команды и переходит к следующей строке.
        # Команда для соединения по указанному протоколу через putty >>> putty -ssh 195.144.107.198
        subprocess.Popen(["putty", flag, el])
        time.sleep(10)  # Пауза 10 секунд.

        # Исключение для завершения процесса putty в зависимости от ОС
        try:
            # Windows
            # Метод для выполнения команды в консоли, который ожидает завершения команды.
            subprocess.run(["taskkill", "/IM", "putty.exe", "/F"])
        except FileNotFoundError:
            # Linux
            # Метод для выполнения команды в консоли, который ожидает завершения команды.
            subprocess.run(["pkill", "putty"])
            print_in_log("***** TERM: CONTROL ERROR - NOT WINDOWS *****")

    # Логирование.
    print_in_log("\n----------------------------------------------------------------------------")
    print_in_log(f"{protocol} end")


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

# Список ресурсов для скачивания по ftp
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
# так как лог идёт в консоли без записи в файл. Выход из цикла осуществляется путём закрытия консоли.
while True:

    print(f"""
Тестирование 573 {RELEASE}
    
1 - http         5 - ftp
2 - email*       6 - telnet  
3 - im*          7 - ssh 
4 - voip(None)*  8 - https 
""")

    # Создание списка из введённой строки
    marker_test_list = [el for el in input("Какие тесты выполнять? (12345678)\n").strip()]

    # Создаём файл для записи лога
    file_for_log()

    # Логирование
    print("\n\n")
    print_in_log("START_" * 8)
    print_in_log(cmd_time(time_or_date="date"))  # Логирование - дата

    # Условие для выполнения всех тестов.
    if len(marker_test_list) == 0:
        # Добавление в marker_test_list всех маркеров тестов.
        marker_test_list = ["1", "2", "3", "4", "5", "6", "7", "8"]

    while True:
        # Блок тестов с условием для запуска >>> Если маркер "X" есть в списке marker_test_list
        if "1" in marker_test_list:
            marker_test_list.remove("1")  # Удаляем маркер теста из marker_test_list
            #try:  # Защита от остановки тестов в случае ошибки
            web_test("HTTP", http_list)
            #except:
            #    print_in_log("***** ERROR IN TEST *****")

        if "2" in marker_test_list:
            marker_test_list.remove("2")  # Удаляем маркер теста из marker_test_list
            try:  # Защита от остановки тестов в случае ошибки
                test_email.i_sender()
            except:
                print_in_log("***** ERROR IN TEST *****")

        if "3" in marker_test_list:
            marker_test_list.remove("3")  # Удаляем маркер теста из marker_test_list
            try:  # Защита от остановки тестов в случае ошибки
                test_im.i_sender()
            except:
                print_in_log("***** ERROR IN TEST *****")

        if "4" in marker_test_list:
            marker_test_list.remove("4")  # Удаляем маркер теста из marker_test_list
            try:  # Защита от остановки тестов в случае ошибки
                print_in_log("\nТест VOIP не готов!")  # Место для тестов voip
            except:
                print_in_log("***** ERROR IN TEST *****")

        if "5" in marker_test_list:
            marker_test_list.remove("5")  # Удаляем маркер теста из marker_test_list
            try:  # Защита от остановки тестов в случае ошибки
                ftp_test(ftp_list)
            except:
                print_in_log("***** ERROR IN TEST *****")

        if "6" in marker_test_list:
            marker_test_list.remove("6")  # Удаляем маркер теста из marker_test_list
            try:  # Защита от остановки тестов в случае ошибки
                terminal_test("TELNET", telnet_list)
            except:
                print_in_log("***** ERROR IN TEST *****")

        if "7" in marker_test_list:
            marker_test_list.remove("7")  # Удаляем маркер теста из marker_test_list
            try:  # Защита от остановки тестов в случае ошибки
                terminal_test("SSH", ssh_list)
            except:
                print_in_log("***** ERROR IN TEST *****")

        if "8" in marker_test_list:
            marker_test_list.remove("8")  # Удаляем маркер теста из marker_test_list
            try:  # Защита от остановки тестов в случае ошибки
                web_test("HTTPS", https_list)
            except:
                print_in_log("***** ERROR IN TEST *****")

        if len(marker_test_list) == 0:
            break

    # Логирование
    print_in_log()
    print_in_log(cmd_time(time_or_date="date"))  # Логирование - дата
    print_in_log("END___" * 8)
    print("\n\n\n")
