"""
Скрипт для логирования и записи данных лога в файл.
Также определения времени выполнения команды.
"""
import os
import time
import http.client  # Для определения своего WAN адреса
import socket  # Для определения своего LAN адреса

# Release v1.5.5
RELEASE = "v1.5.5"


def cmd_time(time_or_date="time") -> str:
    # Функция для возврата местного и GMT времени.
    # time_or_date - маркер для возврата времени(time_or_date="time") или даты(time_or_date="date").
    # Для записи наименования лога используется формат time_or_date="for_log"
    # По умолчанию возвращает время time_or_date="time".

    # Местное дата и время
    local_time = time.localtime()
    # GMT дата и время
    gmt_time = time.gmtime()

    # Условие для возврата даты или времени.
    if time_or_date == "time":
        # Форматирование времени в привычный вид, т.е. из 1:14:3 в 01:14:03.
        # tm_hour, tm_min, tm_sec методы для возвращения единиц времени.
        # Местное время
        local_time_str = "{:0>2d}:{:0>2d}:{:0>2d}".format(local_time.tm_hour, local_time.tm_min, local_time.tm_sec)
        # GMT время
        gmt_time_str = "{:0>2d}:{:0>2d}:{:0>2d}".format(gmt_time.tm_hour, gmt_time.tm_min, gmt_time.tm_sec)
        # Возврат времени в формате "чч:мм:сс (GMT чч:мм:сс)"
        return f"{local_time_str} (GMT {gmt_time_str})"
    elif time_or_date == "date":
        # Форматирование даты в привычный вид, т.е. из 6.1.21 в 06.01.21.
        # tm_mday, tm_mon, tm_year методы для возвращения единиц времени.
        # Местная дата
        local_date_str = "{:0>2d}.{:0>2d}.{:4d}".format(local_time.tm_mday, local_time.tm_mon, local_time.tm_year)
        # GMT дата
        gmt_date_str = "{:0>2d}.{:0>2d}.{:0>2d}".format(gmt_time.tm_mday, gmt_time.tm_mon, gmt_time.tm_year)
        # Возврат даты в формате "ДД.ММ.ГГ (GMT ДД.ММ.ГГ)"
        return f"DATE {local_date_str} (GMT {gmt_date_str})"
    elif time_or_date == "for_log":
        # Форматирование даты в привычный вид, т.е. из 6.1.21 в 06.01.21.
        # GMT время
        gmt_time_log = "{:0>2d}{:0>2d}{:0>2d}".format(gmt_time.tm_hour, gmt_time.tm_min, gmt_time.tm_sec)
        # GMT дата
        gmt_date_log = "{}{:0>2d}{:0>2d}".format(gmt_time.tm_year - 2000, gmt_time.tm_mon, gmt_time.tm_mday)
        # Возврат даты в формате "ГГММДД_ччммсс_GMT)"
        return gmt_date_log + "_" + gmt_time_log + "_GMT.csv"
    else:
        return '\nНЕ ВЕРНЫЙ ФОРМАТ ДЫТЫ: time_or_date="time"/"date"/"for_log"\n'


def my_wan_ip():
    # Определение моего WAN адреса
    wan_ip = http.client.HTTPConnection("ifconfig.me")
    wan_ip.request("GET", "/ip")
    return wan_ip.getresponse().read().decode('utf-8')


def my_lan_ip():
    # Определение моего LAN адреса
    return socket.gethostbyname(socket.gethostname())


def file_for_log():
    # Функция создания лог файла ГГММДД_ччммсс_GMT.log

    # Создаём директорию logs
    try:
        os.mkdir("logs")
    except FileExistsError:
        pass

    os.chdir("logs")  # Меняем рабочую директорию
    logs_file = open(cmd_time("for_log"), mode="x", encoding="utf-8")  # Создаём и открываем файл в режиме записи
    logs_file.write("protocol;time;resource;size;from;to;msg;error;\n")
    logs_file.write(f"INFO;{cmd_time()};WAN {my_wan_ip()};LAN {my_lan_ip()};;;;;")
    logs_file.close()  # Закрываем файл
    os.chdir("../")  # Меняем рабочую директорию


def log_csv(text):
    # Функция для записи данных в файл ГГММДД_ччммсс_GMT.log

    try:
        os.chdir("logs")  # Меняем рабочую директорию
        name_file = tuple(os.walk(os.getcwd()))[0][-1]
        name_file.sort()
    except IndexError:
        os.chdir("../")  # Меняем рабочую директорию
        return

    if len(name_file) == 0:
        # Условие для пустой директории logs
        os.chdir("../")  # Меняем рабочую директорию
        return

    elif len(name_file) > 20:
        # Очищаем папку logs оставляя максимум 20 файлов
        os.remove(name_file[0])

    logs_file = open(name_file[-1], mode="a", encoding="utf-8")  # Открываем файл в режиме дозаписи
    logs_file.write("\n" + text)  # Дозаписываем в файл
    logs_file.close()  # Закрываем файл
    os.chdir("../")  # Меняем рабочую директорию
