#!/usr/bin/python3
"""
Скрипт для автоматического тестирования email тестов 573.
Логирование команд происходит в консоле.
Работа с SMTP

Источник:
https://habr.com/ru/post/51772/
https://habr.com/ru/company/truevds/blog/262819/
https://www.dmosk.ru/instruktions.php?object=python-mail

SMTP https://code.tutsplus.com/ru/tutorials/sending-emails-in-python-with-smtp--cms-29975
     https://habr.com/ru/post/495256/

"""


import smtplib  # Импортируем библиотеку по работе с SMTP
from email import message_from_string
from email import encoders  # Импортируем энкодер
from email.mime.base import MIMEBase  # Общий тип файла
from email.mime.text import MIMEText  # Тип для Текст/HTML
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
import poplib
import imaplib
import base64
import time
# Функция возврата времени из файла log_time.py
from log_time import cmd_time


I_FIRST = True  # True - инициатор, False - автоответчик
#I_FIRST = False  # True - инициатор, False - автоответчик
NEW_MILES = 0  # Маркер определения новых писем
STOP_POP3 = 0  # Маркер завершения функции
STOP_IMAP = 0  # Маркер завершения функции


def send_email(list_from: list, list_to: list, list_msg: list, list_cc=None, list_bcc=None):
    # Все данные в списках должны иметь строковый тип
    # list_from список отправителя, формат: [email , pass, почтовый сервера, порт почтового сервера]
    # list_to список получателя, формат: [email №1, ..., email №n]
    # list_msg список для формирования письма, формат: [тема письма, текст письма, относительный путь к файлу]
    # list_cc (необязательный аргумент) список адресов копии, формат: [email №1, ..., email №n]
    # list_bcc (необязательный аргумент) список адресов скрытой копии, формат: [email №1, ..., email №n]

    if list_cc is None:
        list_cc = []
    if list_bcc is None:
        list_bcc = []

    # Формирование тела письма
    msg = MIMEMultipart(boundary="/")  # Создаем сообщение
    msg["From"] = list_from[0]  # Добавление отправителя
    msg["To"] = ", ".join(list_to)  # Добавление получателей
    msg["Cc"] = ", ".join(list_cc)  # Добавление копии
    msg["Bcc"] = ", ".join(list_bcc)  # Добавление скрытой копии
    msg["Subject"] = list_msg[0]  # Добавление темы сообщения
    msg.attach(MIMEText(list_msg[1], "plain"))  # Добавляем в сообщение текст

    # Условие для определение вложения у письма
    if len(list_msg) > 2:
        filepath = f"./email/{list_msg[2]}"  # Путь к файлу. Файлы для отправки должны лежать в ./email/
        filename = f"{list_msg[2]}"  # Только имя файла

        with open(filepath, "rb") as fp:
            file = MIMEBase("application", "pdf")  # Используем общий MIME-тип
            file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
            fp.close()

        encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
        file.add_header("Content-Disposition", "attachment", filename=filename)  # Добавляем заголовки
        msg.attach(file)  # Присоединяем файл к сообщению

    server = smtplib.SMTP(list_from[2], int(list_from[3]))  # Создаем объект SMTP (сервер, порт)
    # server.set_debuglevel(1)  # Системные логи, дебагер
    server.starttls()  # Начинаем шифрованный обмен по TLS
    server.login(list_from[0], list_from[1])  # Получаем доступ (email, пароль)
    server.send_message(msg)  # Отправляем сообщение

    # Логирование
    print(cmd_time())
    print(f"FROM: {list_from[0]}")
    print(f"  TO: {', '.join(list_to)}")
    print(f"  CC: {', '.join(list_cc)}") if len(list_cc) != 0 else None
    print(f" BCC: {', '.join(list_bcc)}") if len(list_bcc) != 0 else None
    print(f" SUB: {list_msg[0]}")
    print(f"TEXT: {list_msg[1]}")
    print(f"FILE: {list_msg[2]}") if len(list_msg) > 2 else None
    print()

    server.quit()  # Выходим
    time.sleep(10)


def pop3_email(host: list):
    # Передаётся список el: str in [email, pass, server]
    global I_FIRST, NEW_MILES, STOP_POP3

    time.sleep(10)
    # Условие для завершения функции
    if STOP_POP3 == 5 and I_FIRST:
        return

    # Подключаемся к серверу, для Яндекса нужен SSL
    server = poplib.POP3(host[2]) if I_FIRST else poplib.POP3_SSL(host[2])
    # server.set_debuglevel(1)  # Системный лог, дебагер
    server.user(host[0])  # Email
    server.pass_(host[1])  # Пароль
    # Список доступных писем и их размер, при появлении нового список растёт.
    mails = server.list()[1]

    # Условие для начального поиска новых писем, т.е. присваивается количество писем на данный момент.
    if NEW_MILES == 0:
        NEW_MILES = len(mails)

    # Условие для определения новых писем
    if NEW_MILES < len(mails):
        NEW_MILES = len(mails) if I_FIRST else 0
    else:
        # Действие при отсутствии писем до 5 проходов
        STOP_POP3 += 1
        print("No new mails! ", end="*" * (6 - STOP_POP3) + "\n")
        time.sleep(6)
        pop3_email(host)
        return

    lines = server.retr(NEW_MILES)[1]  # Получаем тело сообщения
    # b'\r\n'.join(lines) Подготавливаем сообщение к декодированию.
    # decode('utf-8') Декодируем сообщение по UTF-8 -> str
    # split("--/") создаём список на основе декодированного сообщения, элементы списка делятся по маркеру "--/"
    msg_content = b'\r\n'.join(lines).decode('utf-8').split("--/")
    msg_head = message_from_string(msg_content[0])  # Преобразуем str -> dict
    # Декодируем сообщение base64 -> UTF-8 -> str
    msg_text = base64.b64decode(msg_content[1].split()[-1]).decode('utf-8')
    # Условие для определения вложенного файла и присвоение его имени
    msg_file = msg_content[2].split()[8][10:-1] if len(msg_content) > 3 else None

    msg_subject_decode = str()
    for el in (msg_head.get('Subject')).split():
        # Декодируем тему сообщения base64 -> UTF-8 -> str
        msg_subject_decode += base64.b64decode(el[10:-2]).decode('utf-8')

    print(cmd_time())
    print(f"FROM: {msg_head.get('From')}")  # Вытаскиваем значение по ключу
    print(f"  TO: {msg_head.get('To')}")  # Вытаскиваем значение по ключу
    # Вытаскиваем значение по ключу если оно есть
    print(f"  CC: {msg_head.get('Cc')}") if msg_head.get('Cc') != (None or "") else None
    # Вытаскиваем значение по ключу если оно есть
    print(f" BCC: {msg_head.get('Bcc')}") if msg_head.get('Bcc') != None else None
    print(f" SUB: {msg_subject_decode}")
    print(f"TEXT: {msg_text}")
    print(f"FILE: {msg_file}") if msg_file != None else None  # Имя вложенного файла если оно есть
    print()

    server.quit()  # Закрываем соединение
    pop3_email(host)


def imap_email(host: list):
    global NEW_MILES, STOP_IMAP

    time.sleep(10)

    # Условие для завершения функции
    if STOP_IMAP == 5 and I_FIRST:
        return

    server = imaplib.IMAP4_SSL(host[2])
    server.debug = True
    server.login(host[0], host[1])

    # Выводит список папок в почтовом ящике.
    server.select("inbox")  # Подключаемся к папке "входящие"

    dir_inbox = server.search(None, "ALL")[1]
    id_list = dir_inbox[0].split()  # Получаем сроку номеров писем
    latest_email_id = id_list[-1] if len(id_list) != 0 else 0  # Берем последний ID

    # Условие для начального поиска новых писем, т.е. присваивается количество писем на данный момент.
    if NEW_MILES == 0:
        NEW_MILES = latest_email_id

    # Условие для определения новых писем
    if NEW_MILES < latest_email_id:
        NEW_MILES = latest_email_id
    else:
        # Действие при отсутствии писем до 5 проходов
        STOP_IMAP += 1
        print("No new mails! ", end="*" * (6 - STOP_IMAP) + "\n")
        time.sleep(6)
        imap_email(host)
        return

    # *server.fetch(latest_email_id, "(RFC822)")[1][0]][1] Подготавливаем сообщение к декодированию путём распаковки tuple
    # decode('utf-8') Декодируем сообщение по UTF-8 -> str
    # split("--/") создаём список на основе декодированного сообщения, элементы списка делятся по маркеру "--/"
    # Тело письма в необработанном виде включает в себя заголовки и альтернативные полезные нагрузки
    msg_content = [*server.fetch(latest_email_id, "(RFC822)")[1][0]][1].decode("utf-8").split("--/")  # Получаем тело письма

    msg_head = message_from_string(msg_content[0])  # Преобразуем str -> dict
    # Декодируем сообщение base64 -> UTF-8 -> str
    msg_text = base64.b64decode(msg_content[1].split()[-1]).decode('utf-8')
    # Условие для определения вложенного файла и присвоение его имени
    msg_file = msg_content[2].split()[8][10:-1] if len(msg_content) > 3 else None

    msg_subject_decode = str()
    for el in (msg_head.get('Subject')).split():
        # Декодируем тему сообщения base64 -> UTF-8 -> str
        msg_subject_decode += base64.b64decode(el[10:-2]).decode('utf-8')

    print(cmd_time())
    print(f"FROM: {msg_head.get('From')}")  # Вытаскиваем значение по ключу
    print(f"  TO: {msg_head.get('To')}")  # Вытаскиваем значение по ключу
    # Вытаскиваем значение по ключу если оно есть
    print(f"  CC: {msg_head.get('Cc')}") if msg_head.get('Cc') != (None or "") else None
    # Вытаскиваем значение по ключу если оно есть
    print(f" BCC: {msg_head.get('Bcc')}") if msg_head.get('Bcc') != None else None
    print(f" SUB: {msg_subject_decode}")
    print(f"TEXT: {msg_text}")
    print(f"FILE: {msg_file}") if msg_file != None else None  # Имя вложенного файла если оно есть
    print()

    server.close()  # Закрываем соединение
    imap_email(host)




































# Отравитель №1
sender_1 = ["test@rtc-nt.ru", "Elcom101120", "mail.nic.ru", "587"]
# Письмо №1
to_1 = ["rtc-nt-test1@yandex.ru", "rtc-nt-test2@yandex.ru", "rtc-nt-test3@yandex.ru"]
bcc_1 = ["rtc-nt-test4@yandex.ru"]
msg_1 = ["АВТО Отправка письма с 3 получателями, вложением и скрытой копией",  # Тема письма
         "Текст письма Python",  # Текст письма
         "constitution.pdf"]  # Прикреплённый файл из ./email/
# Письмо №3
to_3 = ["rtc-nt-test1@yandex.ru"]
cc_3 = ["rtc-nt-test2@yandex.ru", "rtc-nt-test3@yandex.ru"]
msg_3 = ["АВТО Отправка письма с 2 копиями и иероглифами",  # Тема письма
         "لِيَتَقَدَّسِ اسْمُكَ"]  # Текст письма

# Отравитель №2
sender_2 = ["rtc-nt-test1@yandex.ru", "zaq123edcxsw2", "smtp.yandex.ru", "587"]
# Письмо №2
to_2 = ["test@rtc-nt.ru", "rtc-nt-test2@yandex.ru", "rtc-nt-test3@yandex.ru"]
msg_2 = ["АВТО Получение письма с 3 получателями и вложением",  # Тема письма
         "Текст письма",  # Текст письма
         "constitution.pdf"]  # Прикреплённый файл из ./email/
# Письмо №4
to_4 = ["test@rtc-nt.ru"]
cc_4 = ["rtc-nt-test2@yandex.ru", "rtc-nt-test3@yandex.ru"]
msg_4 = ["АВТО Получение письма с 2 копиями и иероглифами",  # Тема письма
         "لِيَتَقَدَّسِ اسْمُكَ"]  # Текст письма

print("\n\nSMTP start")
print("----------------------------------------------------------------------------")
# Условие для инициирования переписки
if I_FIRST:
    # Отравитель №1
    send_email(sender_1, to_1, msg_1, list_bcc=bcc_1)  # Отправка Письма №1
    send_email(sender_1, to_3, msg_3)  # Отправка Письма №3
else:
    # Отравитель №12
    send_email(sender_2, to_2, msg_2)  # Отправка Письма №2
    send_email(sender_2, to_4, msg_4, list_cc=cc_4)  # Отправка Письма №4

print("\n----------------------------------------------------------------------------")
print("SMTP end")