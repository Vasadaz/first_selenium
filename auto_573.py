#!/usr/bin/python3
"""
Скрипт для автоматического тестирования 573.
Логирование команд происходит в консоли.
"""
import os
import shutil  # Для удаления папки FTP
import subprocess  # библиотека для работы с командами и процессами ОС
import sys
import time
import test_email
import test_im

# Импорт логирования
from logger import cmd_time, file_for_log, log_csv, my_lan_ip, my_wan_ip, object_name, csv_to_docx, RELEASE

# Импорт модуля selenium, в случае отсутствия будет сделана его установка
# selenium набор методов для управления браузером, common для контроля ошибок если сайт недоступен
# chromedriver_autoinstaller автоустановщик и инициализатор chromedriver
try:
    from selenium import webdriver, common
    import chromedriver_autoinstaller

except ModuleNotFoundError:
    print("Installing selenium==4.4.3")
    # Установка модуля с отключенным stdout
    mod_inst = subprocess.Popen("pip3 install selenium==4.4.3", shell=True,
                                stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    mod_inst.wait()  # Вызов и ожидание установки

    print("Installing chromedriver-autoinstaller==0.4.0")
    # Установка модуля с отключенным stdout
    drive_inst = subprocess.Popen("pip3 install chromedriver-autoinstaller==0.4.0", shell=True,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    drive_inst.wait()  # Вызов и ожидание установки

    from selenium import webdriver, common
    import chromedriver_autoinstaller

# Импорт модуля wget, в случае отсутствия будет сделана его установка
# Для тестов FTP
try:
    import wget
except ModuleNotFoundError:
    print("Installing wget==3.2")
    # Установка модуля с отключенным stdout
    mod_inst = subprocess.Popen("pip3 install wget==3.2", shell=True,
                                stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    mod_inst.wait()  # Вызов и ожидание установки

    import wget


def web_test(protocol: str, sites: list):
    # Функция для теста web соединений. Аргументы:
    # protocol - нужен для логирования;
    # website_list - список сайтов для теста.

    print(f"\n\n{protocol}")
    print("----------------------------------------------------------------------------")

    # Запуск webdriver для chrome
    chromedriver_autoinstaller.install()

    try:
        # Инициализируем драйвер браузера. После этой команды будет открыто новое окно браузера.
        driver = webdriver.Chrome()
    except common.exceptions.SessionNotCreatedException:
        # При автоматическом обновлении браузера тест падает
        print("***** CONTROL ERROR: updating Chrome browser *****")
        # Инициализируем драйвер браузера. После этой команды будет открыто новое окно браузера.
        driver = webdriver.Chrome()
    time.sleep(5)

    print(f"Open browser CHROME v{chromedriver_autoinstaller.get_chrome_version()}")

    # Итерации по элементам списка website_list.
    for site in sites:

        print(f"\n{cmd_time()}\n{protocol} {site}")  # Логирование.
        # Исключение для перенаправления ошибки заблокированных ресурсов.
        try:
            driver.get(site)

            # Запись лога в csv файл
            # protocol;time;resource;size;from;to;msg;error;
            log_csv(f"{protocol};{cmd_time()};{site};;;;;;")
        except common.exceptions.WebDriverException:
            msg_error = "***** WEB: CONTROL ERROR - NOT ANSWER *****"
            print(msg_error)  # Логирование.
            # Запись лога в csv файл
            # protocol;time;resource;size;from;to;msg;error;
            log_csv(f"{protocol};{cmd_time()};{site};;;;;{msg_error};")
        time.sleep(10)  # Пауза 10 секунд.

    # Метод для закрытия окна браузера.
    driver.quit()

    print("\nClose browser")
    print("----------------------------------------------------------------------------")
    print(f"{protocol} end")


def ftp_test(download_list: list):
    # Функция для теста ftp загрузки. Аргументы:
    # download_list - список ресурсов для скачивания по ftp.

    # Логирование.
    print("\n\nFTP")
    print("----------------------------------------------------------------------------")

    try:
        shutil.rmtree("./FTP_573")  # Удаление папки для экономии места
    except FileNotFoundError:
        pass

    os.mkdir("FTP_573")  # Создание пустой папки

    # Индикатор процесса для ftp тестов
    def bar_progress(current: int, total: int, width: int=None):
        percent_download = round(current / total * 100, 1)
        progress_message = f"Downloading: {percent_download}% [{current} / {total}] bytes"
        sys.stdout.write("\r" + progress_message)
        sys.stdout.flush()

    # Итерация по элементам списка download_list.
    for link in download_list:
        # Логирование.
        print(f"\n{cmd_time()}\nFTP {link}")

        # Запись лога в csv файл
        # protocol;time;resource;size;from;to;msg;error;
        log_csv(f"FTP;{cmd_time()};{link};0;;;;;")

        print(f"Download {link[28:]}")  # el[28:] - название файла, удаляется ftp://alta.ru/packets/distr/

        os.chdir("FTP_573")  # Меняем рабочую директорию

        # Метод для выполнения команды в консоли, который ожидает завершения команды.
        # Команда для скачивания файлов >>> wget ftp://alta.ru/packets/distr/ts.zip
        # В версиях python >= 3.9 идёт ошибка
        # 'utf-8' codec can't decode byte 0xc0 in position 4: invalid start byte
        wget.download(link, bar=bar_progress)

        os.chdir("../")  # Меняем рабочую директорию

        # Логирование
        print()
        file_size = os.path.getsize(f"./FTP_573/{link[28:]}")
        if len(str(file_size)) < 10:
            file_size_mb_or_gb = str(round(file_size / (1024 ** 2), 1)) + " MB"
        else:
            file_size_mb_or_gb = str(round(file_size / (1024 ** 3), 1)) + " GB"
        print(f"End {cmd_time()} {link[28:]} {file_size_mb_or_gb} ({file_size} B)")

        # Запись лога в csv файл
        # protocol;time;resource;size;from;to;msg;error;
        log_csv(f"FTP;{cmd_time()};{link};{file_size_mb_or_gb} ({file_size} B);;;;;")

        time.sleep(60)  # Пауза 60 секунд.

    # Логирование.
    print("----------------------------------------------------------------------------")
    print("FTP end")


def terminal_test(protocol: str, servers_list: list, ):
    # Функция для теста telnet и ssh соединений. Сам тест происходит с помощью putty. Аргументы:
    # protocol - для нужен определения протокола(telnet, ssh) и логирования;
    # servers_list - список серверных адресов для теста.

    # Логирование.
    print(f"\n\n{protocol}")
    print("----------------------------------------------------------------------------")

    # Определение протокола путём длинны аргумента protocol
    flag = "-telnet" if len(protocol) > 3 else "-ssh"

    # Итерация по элементам списка servers_list
    for el in servers_list:
        print(f"{cmd_time()}\n{protocol} {el}")  # Логирование.

        # Метод для выполнения команды в консоли, который НЕ ожидает завершения команды и переходит к следующей строке.
        # Команда для соединения по указанному протоколу через putty >>> putty -ssh 195.144.107.198
        subprocess.Popen(["putty", flag, el])
        time.sleep(10)  # Пауза 10 секунд.

        # Исключение для завершения процесса putty в зависимости от ОС
        try:
            # Windows
            # Метод для выполнения команды в консоли, который ожидает завершения команды.
            subprocess.run(["taskkill", "/IM", "putty.exe", "/F"])

            # Запись лога в csv файл
            # protocol;time;resource;size;from;to;msg;error;
            log_csv(f"{protocol};{cmd_time()};{el};;;;;;")

        except FileNotFoundError:
            # Linux
            # Метод для выполнения команды в консоли, который ожидает завершения команды.
            subprocess.run(["pkill", "putty"])

            # Логирование.
            msg_error = "***** TERM: CONTROL ERROR - NOT WINDOWS *****"
            print(msg_error)
            # Запись лога в csv файл
            # protocol;time;resource;size;from;to;msg;error;
            log_csv(f"{protocol};{cmd_time()};{el};;;;;{msg_error};")
        print() if el != servers_list[-1] else None

    # Логирование.
    print("----------------------------------------------------------------------------")
    print(f"{protocol} end")


# Список сайтов для теста http
http_list = [
    "http://kremlin.ru",
    "http://kremlin.ru/structure/president",
    "http://kremlin.ru/static/pdf/constitution.pdf",
    "http://fsb.ru",
    "http://rtc-nt.ru/",
    "http://gramota.ru/",
    "http://duma.gov.ru/",
    "http://ivo.garant.ru/",
    "http://thesheep.info",
    "http://grani.ru",
]

# Список ресурсов для скачивания по ftp
ftp_list = [
    "ftp://alta.ru/packets/distr/ts.zip",
    "ftp://alta.ru/packets/distr/gtdw.zip",
    "ftp://alta.ru/packets/distr/maximum.zip",
]

# Список серверных адресов для подключения по telnet
telnet_list = [
    "54.39.129.129",
    "192.241.222.161",
    "35.185.12.150",
]

# Список серверных адресов для подключения по ssh
ssh_list = [
    "195.144.107.198",
    "205.166.94.16"
]

# Список сайтов для теста https
https_list = [
    "https://yandex.ru",
    "https://mail.ru",
    "https://rambler.ru",
    "https://2ip.ru",
    "https://cia.gov",
    "https://nsa.gov",
    "https://www.mps.gov.cn",
    "https://mossad.gov.il",
    "https://sis.gov.uk",
    "https://bnd.bund.de",
]

# Условие определения режима автоответчика
if len(sys.argv) == 2:
    if sys.argv[1] == "e":
        # Режим автоответчика для тестов EMAIL
        while True:
            test_email.i_answer()
            continue

    elif sys.argv[1] == "i":
        # Режим автоответчика для тестов IM
        while True:
            test_im.i_answer()
            continue

# Проверка, что есть название
# object_name()

# Постоянный цикл для запуска тестов и просмотра логирования. Постоянный для просмотра логирования,
# так как лог идёт в консоли без записи в файл. Выход из цикла осуществляется путём закрытия консоли.
while True:

    print(f"""
Тестирование 573 {RELEASE}
{object_name()}
WAN: {my_wan_ip()}
LAN: {my_lan_ip()}

1 - http         5 - ftp
2 - email*       6 - telnet  
3 - im*          7 - ssh 
4 - voip(None)*  8 - https 

Режимы автоответчика:
e - email        i - im
""")

    # Создание списка из введённой строки
    marker_test_list = [el for el in input("Какие тесты выполнять? (12345678)\n").strip()]

    # Режим автоответчика для тестов EMAIL
    if "e" in marker_test_list:
        while True:
            test_email.i_answer()
            continue

    # Режим автоответчика для тестов IM
    if "i" in marker_test_list:
        while True:
            test_im.i_answer()
            continue

    # Создаём файл для записи лога
    file_for_log()

    # Логирование
    print("\n\n")
    print("START_" * 8)
    print(cmd_time(time_or_date="date"))  # Логирование - дата

    # Условие для выполнения всех тестов.
    if len(marker_test_list) == 0:
        # Добавление в marker_test_list всех маркеров тестов.
        marker_test_list = ["1", "2", "3", "4", "5", "6", "7", "8"]

    while True:
        # Блок тестов с условием для запуска >>> Если маркер "X" есть в списке marker_test_list
        if "1" in marker_test_list:
            marker_test_list.remove("1")  # Удаляем маркер теста из marker_test_list
            # Защита от остановки тестов в случае ошибки
            # try:
            web_test("HTTP", http_list)
            # except:
            #    print_in_log("***** ERROR IN TEST *****")

        if "2" in marker_test_list:
            marker_test_list.remove("2")  # Удаляем маркер теста из marker_test_list
            try:  # Защита от остановки тестов в случае ошибки
                test_email.i_sender()
            except Exception as err:
                print("***** ERROR IN TEST *****")
                print(err)

        if "3" in marker_test_list:
            marker_test_list.remove("3")  # Удаляем маркер теста из marker_test_list
            try:  # Защита от остановки тестов в случае ошибки
                test_im.i_sender()
            except Exception as err:
                print("***** ERROR IN TEST *****")
                print(err)

        if "4" in marker_test_list:
            marker_test_list.remove("4")  # Удаляем маркер теста из marker_test_list
            try:  # Защита от остановки тестов в случае ошибки
                print("\nТест VOIP не готов!")  # Место для тестов voip
            except Exception as err:
                print("***** ERROR IN TEST *****")
                print(err)

        if "5" in marker_test_list:
            marker_test_list.remove("5")  # Удаляем маркер теста из marker_test_list
            try:  # Защита от остановки тестов в случае ошибки
                ftp_test(ftp_list)
            except Exception as err:
                print("***** ERROR IN TEST *****")
                print(err)

        if "6" in marker_test_list:
            marker_test_list.remove("6")  # Удаляем маркер теста из marker_test_list
            try:  # Защита от остановки тестов в случае ошибки
                terminal_test("TELNET", telnet_list)
            except Exception as err:
                print("***** ERROR IN TEST *****")
                print(err)

        if "7" in marker_test_list:
            marker_test_list.remove("7")  # Удаляем маркер теста из marker_test_list
            try:  # Защита от остановки тестов в случае ошибки
                terminal_test("SSH", ssh_list)
            except Exception as err:
                print("***** ERROR IN TEST *****")
                print(err)

        if "8" in marker_test_list:
            marker_test_list.remove("8")  # Удаляем маркер теста из marker_test_list
            try:  # Защита от остановки тестов в случае ошибки
                web_test("HTTPS", https_list)
            except Exception as err:
                print("***** ERROR IN TEST *****")
                print(err)

        if len(marker_test_list) == 0:
            break

    # Логирование
    print()
    print(cmd_time(time_or_date="date"))  # Логирование - дата
    print("END___" * 8)
    print("\n\n\n")

    # Создаём по тесту файл .docx
    csv_to_docx()

    test_email.send_end_test(object_name())
