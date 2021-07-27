"""
Файлдля определения времени
"""
import time

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
        # Форматирование дыты в привычный вид, т.е. из 6.1.21 в 06.01.21.
        # tm_mday, tm_mon, tm_year методы для возвращения единиц времени.
        # Месная дата
        local_time_str = "{:0>2d}.{:0>2d}.{:4d}".format(local_time.tm_mday, local_time.tm_mon, local_time.tm_year)
        # GMT дата
        gmt_time_str = "{:0>2d}.{:0>2d}.{:0>2d}".format(gmt_time.tm_mday, gmt_time.tm_mon, gmt_time.tm_year)
        # Возврат даты в формате "ДД.ММ.ГГ (GMT ДД.ММ.ГГ)"
        return "DATE {} (GMT {})".format(local_time_str, gmt_time_str)