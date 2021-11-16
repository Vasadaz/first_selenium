"""
Скрипт для логирования и записи данных лога в файл.
Также определения времени выполнения команды.
"""
import os
import time

# Release v1.5.4
RELEASE = "v1.5.4"


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
        return gmt_date_log + "_" + gmt_time_log + "_GMT.log"
    else:
        return '\nНЕ ВЕРНЫЙ ФОРМАТ ДЫТЫ: time_or_date="time"/"date"/"for_log"\n'


def file_for_log():
    try:
        os.mkdir("logs")
    except FileExistsError:
        pass

    os.chdir("./logs")  # Меняем рабочую директорию
    logs_file = open(cmd_time("for_log"), mode="x")  # Создаём и открываем файл в режиме записи
    logs_file.write("")
    logs_file.close()  # Закрываем файл
    os.chdir("../")  # Меняем рабочую директорию
    time.sleep(2)


def print_in_log(text="\n"):
    try:
        os.mkdir("logs")
    except FileExistsError:
        pass
    # Функция для записи данных в файл ГГММДД_ччммсс_GMT.log
    os.chdir("./logs")  # Меняем рабочую директорию

    try:
        name_file = tuple(os.walk(os.getcwd()))[0][-1]
        name_file.sort()
    except IndexError:
        os.chdir("../")  # Меняем рабочую директорию
        return

    logs_file = open(name_file[-1], mode="a")  # Открываем файл в режиме дозаписи
    logs_file.write(text + '\n')  # Дозаписываем в файл
    logs_file.close()  # Закрываем файл
    print(text)
    os.chdir("../")  # Меняем рабочую директорию
