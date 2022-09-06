"""
Скрипт для логирования и записи данных лога в файл.
Также определения времени выполнения команды.
"""
import os
import subprocess
import datetime  # Для возврата дат и времени
import csv
import http.client  # Для определения своего WAN адреса
import socket  # Для определения своего LAN адреса

# Импорт модуля docx, в случае отсутствия будет сделана его установка
# Для работы с файлами .docx
try:
    import docx
    from docx.shared import Pt  # Для работы с .docx
except ModuleNotFoundError:
    print("Installing python-docx==0.8.11")
    # Установка модуля с отключенным stdout
    mod_inst = subprocess.Popen("pip3 install python-docx==0.8.11", shell=True,
                                stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    mod_inst.wait()  # Вызов и ожидание установки
    import docx
    from docx.shared import Pt  # Для работы с .docx

# Release v1.6.9
RELEASE = "v1.6.9"

OBJECT_NAME = "UNKNOWN"


def object_name():
    # Название объекта для логирования
    global OBJECT_NAME

    if my_lan_ip() in ["192.168.1.127", "172.24.64.1"]:
        OBJECT_NAME = "РТК-НТ"
        return OBJECT_NAME

    name_file = tuple(os.walk(os.getcwd()))[0][-1]  # Получаем список файлов внутри

    if "name_object.txt" in name_file:
        with open("name_object.txt", "r+", encoding='UTF-8') as name_object_txt:
            line = name_object_txt.readline()
            if len(line) == 0:
                OBJECT_NAME = input("Имя объекта для логирования:\n")
                name_object_txt.write(OBJECT_NAME)
            else:
                OBJECT_NAME = line
            name_object_txt.close()
    else:
        with open("name_object.txt", "x+", encoding='UTF-8') as name_object_txt:
            OBJECT_NAME = input("Имя объекта для логирования:\n")
            name_object_txt.write(OBJECT_NAME)
            name_object_txt.close()

    return OBJECT_NAME


def cmd_time(time_or_date="time") -> str:
    # Функция для возврата местного и GMT времени.
    # time_or_date - маркер для возврата времени(time_or_date="time") или даты(time_or_date="date").
    # Для записи наименования лога используется формат time_or_date="for_log"
    # По умолчанию возвращает время time_or_date="time".

    # Местное дата и время
    local_date = datetime.datetime.now().date()  # YYYY-MM-DD
    local_time = str(datetime.datetime.now().time())[:-7]  # hh24:mi:ss

    # GMT дата и время
    gmt_date = datetime.datetime.utcnow().date()  # YYYY-MM-DD
    gmt_time = str(datetime.datetime.utcnow().time())[:-7]  # hh24:mi:ss

    # Условие для возврата даты или времени.
    if time_or_date == "time":
        # Возврат времени в формате "hh24:mi:ss (GMT hh24:mi:ss)"
        return f"{local_time} (GMT {gmt_time})"
    elif time_or_date == "date":
        # Возврат даты в формате "YYYY-MM-DD (GMT YYYY-MM-DD)"
        return f"DATE {local_date} (GMT {gmt_date})"
    elif time_or_date == "for_log":
        # Форматирование даты и времени для логирования YYMMDD_hh24miss.
        # Возврат даты в формате "YYMMDD_hh24miss_GMT NAME.csv"
        return f"{str(gmt_date).replace('-', '')[2:] + '_' + gmt_time.replace(':', '')}_GMT  {OBJECT_NAME}.csv"
    elif time_or_date == "test_end":
        # Форматирование даты и времени для проверки в ПУ 573 210106000000Z.
        gmt_date_test_today = f"{str(gmt_date).replace('-', '')[2:]}"
        gmt_date_test_tomorrow = str(gmt_date + datetime.timedelta(days=1)).replace("-", "")[2:]

        # Возврат даты в формате "YYMMDD000000Z"
        return f"{gmt_date_test_today}000000Z\n{gmt_date_test_tomorrow}000000Z"
    else:
        return '\nНЕ ВЕРНЫЙ ФОРМАТ ДЫТЫ: time_or_date="time"/"date"/"for_log"/"test_end"\n'


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

    global OBJECT_NAME

    # Создаём директорию logs
    try:
        os.mkdir("logs")
    except FileExistsError:
        pass

    # Очищаем папку logs оставляя максимум 10 файлов
    os.chdir("logs")  # Меняем рабочую директорию
    files_in_dir_logs = tuple(os.walk(os.getcwd()))[0][-1]  # Получаем список файлов внутри ./logs
    for i in range(len(files_in_dir_logs) - 10):
        os.remove(files_in_dir_logs[i])
    os.chdir("../")  # Меняем рабочую директорию

    # Создаём директорию logs_in_docx
    try:
        os.mkdir("logs_in_docx")
    except FileExistsError:
        pass

    # Очищаем папку logs_in_docx оставляя максимум 10 файлов
    os.chdir("logs_in_docx")  # Меняем рабочую директорию
    files_in_dir_logs = tuple(os.walk(os.getcwd()))[0][-1]  # Получаем список файлов внутри ./logs_in_docx
    for i in range(len(files_in_dir_logs) - 10):
        os.remove(files_in_dir_logs[i])
    os.chdir("../")  # Меняем рабочую директорию

    os.chdir("logs")  # Меняем рабочую директорию
    logs_file = open(cmd_time("for_log"), mode="x", encoding="utf-8")  # Создаём и открываем файл в режиме записи
    logs_file.write("protocol;time;resource;size;from;to;msg;error;\n")
    logs_file.write(f"{OBJECT_NAME};{cmd_time()};WAN {my_wan_ip()};LAN {my_lan_ip()};;;;;")
    logs_file.close()  # Закрываем файл
    os.chdir("../")  # Меняем рабочую директорию


def log_csv(text):
    # Функция для записи данных в файл ГГММДД_ччммсс_GMT.log

    os.chdir("logs")  # Меняем рабочую директорию
    name_file = tuple(os.walk(os.getcwd()))[0][-1]  # Получаем список файлов внутри ./logs
    name_file.sort()
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

    # Обработка последнего лога из csv файла вида:
    # protocol;time;resource;size;from;to;msg;error;
    #    ||     ||     ||     ||   ||  ||  ||   ||
    #   [0]    [1]    [2]    [3]  [4] [5] [6]  [7]
    # line[0] - headers
    # line[1] - info about WAN and LAN addresses

    os.chdir("logs")  # Меняем рабочую директорию
    name_file = tuple(os.walk(os.getcwd()))[0][-1]  # Получаем список файлов внутри ./logs
    name_file.sort()
    with open(name_file[-1], "r", encoding="utf-8") as log_in_csv:
        log_list = [line[0].split(";") for line in csv.reader(log_in_csv)]  # Преобразуем строку из файла в список
        log_in_csv.close()
    os.chdir("../")  # Меняем рабочую директорию

    http_time_list = []
    email_time_list = []
    im_time_list = []
    voip_time_list = []
    ftp_time_list = []
    telnet_time_list = []
    ssh_time_list = []
    https_time_list = []

    for test in log_list:
        if test[0] == "HTTP":
            http_time_list.append(test[1][:5])
        elif "EMAIL" in test[0]:
            email_time_list.append(test[1][:5])
        elif "IM" in test[0]:
            im_time_list.append(test[1][:5])
        elif "VOIP" in test[0]:
            voip_time_list.append(test[1][:5])
        elif "FTP" in test[0]:
            if test[3] == "0":  # start
                ftp_time_list.append(test[1][:5])
            else:  # end
                # Получаем строку "start - hh:mi (size MB/GB)"
                ftp_time_list[-1] += f" - {test[1][:5]} ({test[3].replace(' (', '    ')[:8].strip(' ')})"
        elif "TELNET" in test[0]:
            telnet_time_list.append(test[1][:5])
        elif "SSH" in test[0]:
            ssh_time_list.append(test[1][:5])
        elif "HTTPS" in test[0]:
            https_time_list.append(test[1][:5])

    # VOIP тест не готов, поэтому заменим его первым временем HTTP,
    # т.к. он делается вручную перед запуском авто-теста
    try:
        if len(voip_time_list) == 0:
            voip_time_list.append(http_time_list[0])
            voip_time_list.append(http_time_list[0])
    except IndexError:
        pass

    wordDoc = docx.Document("./template_report_test.docx")  # Открываем чистую таблицу
    style = wordDoc.styles['Normal']  # задаем стиль текста по умолчанию
    style.font.name = 'Times New Roman'  # название шрифта
    style.font.size = Pt(12)  # размер шрифта

    # Таблица №1 wordDoc.tables[0]
    wordDoc.tables[0].rows[0].cells[0].text = f"Оператор: {OBJECT_NAME}"
    wordDoc.tables[0].rows[2].cells[0].text = f"IP-адрес тестового рабочего места: {log_list[1][2][4:]}"
    wordDoc.tables[0].rows[3].cells[0].text = f"Дата выполнения тестов: {cmd_time('date')[5:15]}"

    # Таблица №2 wordDoc.tables[1]
    try:
        # HTTP
        wordDoc.tables[1].rows[1].cells[3].text = http_time_list[0]  # HTTP Время http://kremlin.ru
        wordDoc.tables[1].rows[2].cells[3].text = http_time_list[1]  # HTTP Время http://kremlin.ru/acts/constitution
        wordDoc.tables[1].rows[3].cells[3].text = http_time_list[2]  # HTTP Время constitution.pdf
        wordDoc.tables[1].rows[4].cells[3].text = http_time_list[3]  # HTTP Время http://fsb.ru
        wordDoc.tables[1].rows[5].cells[3].text = http_time_list[4]  # HTTP Время http://khann.ru
        wordDoc.tables[1].rows[6].cells[3].text = http_time_list[5]  # HTTP Время http://khann.ru/wallpapers/
        wordDoc.tables[1].rows[7].cells[3].text = http_time_list[5]  # HTTP Время *.jpg
        wordDoc.tables[1].rows[8].cells[3].text = http_time_list[6]  # HTTP Время http://alex-kuznetsov.ru/test
        wordDoc.tables[1].rows[9].cells[3].text = http_time_list[7]  # HTTP Время http://www.thesheep.info
        wordDoc.tables[1].rows[10].cells[3].text = http_time_list[8]  # HTTP Время http://www.grani.ru
    except IndexError:
        pass

    try:
        # EMAIL
        wordDoc.tables[1].rows[11].cells[3].text = email_time_list[
            0]  # EMAIL Время Отправка письма с 3 получателями, вложением и копией
        wordDoc.tables[1].rows[13].cells[3].text = email_time_list[
            1]  # EMAIL Время Получение письма с 3 получателями и вложением
        wordDoc.tables[1].rows[15].cells[3].text = email_time_list[
            2]  # EMAIL Время Отправка письма с 2 копиями и иероглифы
        wordDoc.tables[1].rows[17].cells[3].text = email_time_list[
            3]  # EMAIL Время Получение письма с 2 копиями и иероглифы
    except IndexError:
        pass

    try:
        # IM
        wordDoc.tables[1].rows[19].cells[3].text = im_time_list[2]  # IM Время Отправка сообщений
        wordDoc.tables[1].rows[20].cells[3].text = im_time_list[3]  # IM Время Получение сообщений
    except IndexError:
        pass

    try:
        # VOIP
        wordDoc.tables[1].rows[21].cells[3].text = voip_time_list[0]  # VOIP Время Исходящее голосовое соединение
        wordDoc.tables[1].rows[23].cells[3].text = voip_time_list[1]  # VOIP Время Входящее голосовое соединение
    except IndexError:
        pass

    try:
        # FTP
        wordDoc.tables[1].rows[25].cells[3].text = ftp_time_list[0][
                                                   :5]  # FTP Время Доступ к ресурсу: ftp://alta.ru/packets/distr/
        wordDoc.tables[1].rows[26].cells[3].text = "\n\n" + ftp_time_list[0]  # FTP Время start - end ts.zip
        wordDoc.tables[1].rows[27].cells[3].text = ftp_time_list[1]  # FTP Время start - end  gtdw.zip
        wordDoc.tables[1].rows[28].cells[3].text = ftp_time_list[2]  # FTP Время start - end  maximum.zip
    except IndexError:
        pass

    try:
        # TELNET
        wordDoc.tables[1].rows[30].cells[3].text = telnet_time_list[0]  # TELNET Время towel.blinkenlights.nl
        wordDoc.tables[1].rows[31].cells[3].text = telnet_time_list[1]  # TELNET Время lord.stabs.org
        wordDoc.tables[1].rows[32].cells[3].text = telnet_time_list[2]  # TELNET Время 35.185.12.150
    except IndexError:
        pass

    try:
        # SSH
        wordDoc.tables[1].rows[33].cells[3].text = ssh_time_list[0]  # SSH Время 195.144.107.198
        wordDoc.tables[1].rows[34].cells[3].text = ssh_time_list[1]  # SSH Время sdf.org
    except IndexError:
        pass

    try:
        # HTTPS
        wordDoc.tables[1].rows[35].cells[3].text = https_time_list[0]  # HTTPS Время https://yandex.ru
        wordDoc.tables[1].rows[36].cells[3].text = https_time_list[1]  # HTTPS Время https://mail.ru
        wordDoc.tables[1].rows[37].cells[3].text = https_time_list[2]  # HTTPS Время https://rambler.ru
        wordDoc.tables[1].rows[38].cells[3].text = https_time_list[3]  # HTTPS Время https://2ip.ru
        wordDoc.tables[1].rows[39].cells[3].text = https_time_list[4]  # HTTPS Время https://cia.gov
        wordDoc.tables[1].rows[40].cells[3].text = https_time_list[5]  # HTTPS Время https://nsa.gov
        wordDoc.tables[1].rows[41].cells[3].text = https_time_list[6]  # HTTPS Время https://ssu.gov.ua
        wordDoc.tables[1].rows[42].cells[3].text = https_time_list[7]  # HTTPS Время https://mossad.gov.il
        wordDoc.tables[1].rows[43].cells[3].text = https_time_list[8]  # HTTPS Время https://sis.gov.uk
        wordDoc.tables[1].rows[44].cells[3].text = https_time_list[9]  # HTTPS Время https://bnd.bund.de
    except IndexError:
        pass

    # Сохраняем заполненный файл "Проверен YYMMDD_hh24miss_GMT Тесты ПСИ 573 ПД.docx" в директории logs_in_docx
    wordDoc.save(f"./logs_in_docx/Проверен {name_file[-1][:-4]} Тесты ПСИ 573 ПД.docx")
