"""
Скрипт для логирования и записи данных лога в файл.
Также определения времени выполнения команды.
"""
import os
import time
import http.client  # Для определения своего WAN адреса
import socket  # Для определения своего LAN адреса
import docx  # Для работы с .docx
from docx.shared import Pt  # Для работы с .docx

# Release v1.5.6
RELEASE = "v1.5.6"


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

    # Создаём директорию logs_in_docx
    try:
        os.mkdir("logs_in_docx")
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


def csv_to_docx():
    """
    Источники
    https://ru.stackoverflow.com/questions/921605
    https://docs-python.ru/packages/modul-python-docx-python/
    https://question-it.com/questions/1216223/vyravnivanie-teksta-v-biblioteke-python-docx
    """

    # Открываем чистую таблицу
    wordDoc = docx.Document("./clear.docx")
    # задаем стиль текста по умолчанию
    style = wordDoc.styles['Normal']
    # название шрифта
    style.font.name = 'Times New Roman'
    # размер шрифта
    style.font.size = Pt(14)

    # Вносим данные в Таблица №1 (wordDoc.tables[0])
    wordDoc.tables[0].rows[1].cells[2].text = f"Дата: {cmd_time('date')[5:15]}"  # Дата:
    wordDoc.tables[0].rows[3].cells[0].text = f"https://2ip.ru = {my_wan_ip()}"  # https://2ip.ru =
    wordDoc.tables[0].rows[4].cells[0].text = f"Серый IP = {my_lan_ip()}"  # Серый IP =

    # Сохраняем заполненный файл "Проверен YYMMDD_hh24miss_GMT Тесты ПСИ 573 ПД.docx" в директории logs_in_docx
    wordDoc.save(f"./logs_in_docx/Проверен {cmd_time('for_log')[:-4]} Тесты ПСИ 573 ПД.docx")

    """
    # Таблица №1 (wordDoc.tables[0])
    print(wordDoc.tables[0].rows[1].cells[2].text)  # Дата:
    print(wordDoc.tables[0].rows[3].cells[0].text)  # https://2ip.ru =
    print(wordDoc.tables[0].rows[4].cells[0].text)  # Серый IP =
    
    # Таблица №2 (wordDoc.tables[1])
    print(wordDoc.tables[1].rows[2].cells[3].text)  # HTTP Время http://kremlin.ru
    print(wordDoc.tables[1].rows[3].cells[3].text)  # HTTP Время http://kremlin.ru/acts/constitution
    print(wordDoc.tables[1].rows[4].cells[3].text)  # HTTP Время constitution.pdf
    print(wordDoc.tables[1].rows[5].cells[3].text)  # HTTP Время http://fsb.ru
    print(wordDoc.tables[1].rows[6].cells[3].text)  # HTTP Время http://khann.ru
    print(wordDoc.tables[1].rows[7].cells[3].text)  # HTTP Время http://khann.ru/wallpapers/
    print(wordDoc.tables[1].rows[8].cells[3].text)  # HTTP Время *.jpg
    print(wordDoc.tables[1].rows[9].cells[3].text)  # HTTP Время http://alex-kuznetsov.ru/test
    print(wordDoc.tables[1].rows[10].cells[3].text)  # HTTP Время http://www.thesheep.info
    print(wordDoc.tables[1].rows[11].cells[3].text)  # HTTP Время http://www.grani.ru
    print(wordDoc.tables[1].rows[12].cells[3].text)  # EMAIL Время Отправка письма с 3 получателями, вложением и копией
    print(wordDoc.tables[1].rows[14].cells[3].text)  # EMAIL Время Получение письма с 3 получателями и вложением
    print(wordDoc.tables[1].rows[16].cells[3].text)  # EMAIL Время Отправка письма с 2 копиями и иероглифы
    print(wordDoc.tables[1].rows[18].cells[3].text)  # EMAIL Время Получение письма с 2 копиями и иероглифы
    print(wordDoc.tables[1].rows[20].cells[3].text)  # IM Время Отправка сообщений
    print(wordDoc.tables[1].rows[21].cells[3].text)  # IM Время Получение сообщений
    print(wordDoc.tables[1].rows[22].cells[3].text)  # VOIP Время Исходящее голосовое соединение
    print(wordDoc.tables[1].rows[24].cells[3].text)  # VOIP Время Входящее голосовое соединение
    print(wordDoc.tables[1].rows[26].cells[3].text)  # FTP Время Доступ к ресурсу: ftp://alta.ru/packets/distr/
    print(wordDoc.tables[1].rows[27].cells[3].text)  # FTP Время start ts.zip
    print(wordDoc.tables[1].rows[28].cells[3].text)  # FTP Время start gtdw.zip
    print(wordDoc.tables[1].rows[28].cells[5].text)  # FTP Время end gtdw.zip
    print(wordDoc.tables[1].rows[29].cells[3].text)  # FTP Время start maximum.zip
    print(wordDoc.tables[1].rows[29].cells[5].text)  # FTP Время end maximum.zip
    print(wordDoc.tables[1].rows[31].cells[3].text)  # TELNET Время towel.blinkenlights.nl
    print(wordDoc.tables[1].rows[32].cells[3].text)  # TELNET Время lord.stabs.org
    print(wordDoc.tables[1].rows[33].cells[3].text)  # TELNET Время 35.185.12.150
    print(wordDoc.tables[1].rows[34].cells[3].text)  # SSH Время 195.144.107.198
    print(wordDoc.tables[1].rows[35].cells[3].text)  # SSH Время sdf.org
    print(wordDoc.tables[1].rows[36].cells[3].text)  # HTTPS Время https://yandex.ru
    print(wordDoc.tables[1].rows[37].cells[3].text)  # HTTPS Время https://mail.ru
    print(wordDoc.tables[1].rows[38].cells[3].text)  # HTTPS Время https://rambler.ru
    print(wordDoc.tables[1].rows[39].cells[3].text)  # HTTPS Время https://2ip.ru
    print(wordDoc.tables[1].rows[40].cells[3].text)  # HTTPS Время https://cia.gov
    print(wordDoc.tables[1].rows[41].cells[3].text)  # HTTPS Время https://nsa.gov
    print(wordDoc.tables[1].rows[42].cells[3].text)  # HTTPS Время https://ssu.gov.ua
    print(wordDoc.tables[1].rows[43].cells[3].text)  # HTTPS Время https://mossad.gov.il
    print(wordDoc.tables[1].rows[44].cells[3].text)  # HTTPS Время https://sis.gov.uk
    print(wordDoc.tables[1].rows[45].cells[3].text)  # HTTPS Время https://bnd.bund.de
    """

file_for_log()
csv_to_docx()