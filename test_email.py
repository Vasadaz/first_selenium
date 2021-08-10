#!/usr/bin/python3
"""
Скрипт для автоматического тестирования email тестов 573.
Логирование команд происходит в консоли.
Работа с SMTP, POP3 и IMAP

Источник:
https://habr.com/ru/post/51772/
https://habr.com/ru/company/truevds/blog/262819/
https://www.dmosk.ru/instruktions.php?object=python-mail

SMTP https://code.tutsplus.com/ru/tutorials/sending-emails-in-python-with-smtp--cms-29975
     https://habr.com/ru/post/495256/

POP3 https://www.code-learner.com/python-use-pop3-to-read-email-example/

IMAP http://python-3.ru/page/imap-email-python
"""

import smtplib  # Импортируем библиотеку по работе с SMTP
from email import message_from_string
from email import encoders  # Импортируем энкодер
from email.mime.base import MIMEBase  # Общий тип файла
from email.mime.text import MIMEText  # Тип для Текст/HTML
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
import poplib  # Библиотека для POP3
import imaplib  # Библиотека для IMAP
import base64  # Библиотека кодировки Base64

# Функция возврата времени из файла log_time.py
from log_time import cmd_time, time

I_FIRST = True  # True - инициатор, False - автоответчик
NEW_MILES = 0  # Маркер определения новых писем
STOP_READ_EMAIL = 0  # Маркер завершения функции
COUNT_SUBJECTS = True  # Маркер для логирования


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
    print("SEND SMTP", cmd_time())
    print(f"FROM: {list_from[0]}")
    print(f"  TO: {', '.join(list_to)}")
    print(f"  CC: {', '.join(list_cc)}") if len(list_cc) != 0 else None
    print(f" BCC: {', '.join(list_bcc)}") if len(list_bcc) != 0 else None
    print(f" SUB: {list_msg[0]}")
    print(f"TEXT: {list_msg[1]}")
    print(f"FILE: {list_msg[2]}") if len(list_msg) > 2 else None
    print()

    server.quit()  # Выходим
    return


def read_email(info_email: list, protocol: str):
    # info_email список el: str in [email, pass, server]
    # protocol либо "POP3", либо "IMAP"
    global I_FIRST, NEW_MILES, STOP_READ_EMAIL, COUNT_SUBJECTS

    time.sleep(2)
    mails = 0  # Надо - без этого почему-то не получить письма


    # Условие для завершения функции
    if STOP_READ_EMAIL == 500 and I_FIRST:
        print("*** THE COLONEL's NO ONE WRITES! ***\n")
        return False


    if protocol == "POP3":
        # Подключаемся к серверу, для Яндекса нужен SSL
        server = poplib.POP3(info_email[2]) if I_FIRST else poplib.POP3_SSL(info_email[2])
        # server.set_debuglevel(1)  # Системный лог, дебагер
        server.user(info_email[0])  # Email
        server.pass_(info_email[1])  # Пароль
        # Список доступных писем и их размер, при появлении нового список растёт.
        mails = len(server.list()[1])

    elif protocol == "IMAP":
        server = imaplib.IMAP4_SSL(info_email[2])
        server.debug = True
        server.login(info_email[0], info_email[1])
        # Выводит список папок в почтовом ящике.
        server.select("inbox")  # Подключаемся к папке "входящие"
        dir_inbox = server.search(None, "ALL")[1]
        id_list = dir_inbox[0].split()  # Получаем сроку номеров писем
        mails = id_list[-1] if len(id_list) != 0 else 0  # Берем последний ID

    else:
        print("***** PROTOCOL: POP3 or IMAP *****")
        return False

    # Условие для начального поиска новых писем, т.е. присваивается количество писем на данный момент.
    if NEW_MILES == 0:
        NEW_MILES = mails

    # Условие для определения новых писем
    if NEW_MILES < mails:
        NEW_MILES = mails if I_FIRST else 0
    else:
        # Действие при отсутствии писем до 5 проходов
        print("No new mails!") if I_FIRST else None
        return read_email(info_email, protocol)

    # Обработка сообщения
    if protocol == "POP3":
        lines = server.retr(NEW_MILES)[1]  # Получаем тело сообщения
        # b'\r\n'.join(lines) Подготавливаем сообщение к декодированию.
        # decode('utf-8') Декодируем сообщение по UTF-8 -> str
        # split("--/") создаём список на основе декодированного сообщения, элементы списка делятся по маркеру "--/"
        msg_content = b'\r\n'.join(lines).decode('utf-8').split("--/")

    else:
        # для IMAP: *server.fetch(latest_email_id, "(RFC822)")[1][0]][1] Подготавливаем сообщение к декодированию
        # путём распаковки tuple decode('utf-8') Декодируем сообщение по UTF-8 -> str split("--/") создаём список на
        # основе декодированного сообщения, элементы списка делятся по маркеру "--/" Тело письма в необработанном
        # виде включает в себя заголовки и альтернативные полезные нагрузки
        msg_content = [*server.fetch(mails, "(RFC822)")[1][0]][1].decode("utf-8").split("--/")  # Получаем тело письма

    msg_head = message_from_string(msg_content[0])  # Преобразуем str -> dict
    # Декодируем сообщение base64 -> UTF-8 -> str
    msg_text = base64.b64decode(msg_content[1].split()[-1]).decode('utf-8')
    # Условие для определения вложенного файла и присвоение его имени
    msg_file = msg_content[2].split()[8][10:-1] if len(msg_content) > 3 else None

    msg_subject_decode = str()
    for el in (msg_head.get('Subject')).split():
        # Декодируем тему сообщения base64 -> UTF-8 -> str
        msg_subject_decode += base64.b64decode(el[10:-2]).decode('utf-8')

    if not I_FIRST and COUNT_SUBJECTS:
        COUNT_SUBJECTS = False
        print("\n\nEMAIL start")
        print("--------------------------------------------------------------------------")

    print("\nREAD", protocol, cmd_time())
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

    server.quit() if protocol == "POP3" else server.close()  # Закрываем соединение
    STOP_READ_EMAIL = 0
    return True


# Отравитель №1
sender_1 = ["test@rtc-nt.ru", "Elcom101120", "mail.nic.ru", "587", ]

# Письмо №1
to_1 = ["rtc-nt-test1@yandex.ru", "rtc-nt-test2@yandex.ru", "rtc-nt-test3@yandex.ru"]
bcc_1 = ["rtc-nt-test4@yandex.ru"]
msg_1 = ["АВТО Отправка письма с 3 получателями, вложением и скрытой копией",  # Тема письма
         "Текст письма Отправка",  # Текст письма
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
         "Текст письма Получение",  # Текст письма
         "constitution.pdf"]  # Прикреплённый файл из ./email/
# Письмо №4
to_4 = ["test@rtc-nt.ru"]
cc_4 = ["rtc-nt-test2@yandex.ru", "rtc-nt-test3@yandex.ru"]
msg_4 = ["АВТО Получение письма с 2 копиями и иероглифами",  # Тема письма
         "لِيَتَقَدَّسِ اسْمُكَ"]  # Текст письма

# Получатель №1 POP3
reader_1_pop3 = ["test@rtc-nt.ru", "Elcom101120", "mail.nic.ru"]
# Получатель №2 IMAP
reader_2_imap = ["rtc-nt-test1@yandex.ru", "zaq123edcxsw2", "imap.yandex.ru"]


def i_sender():  # Отравитель №1

    print("\n\nEMAIL start")
    print("----------------------------------------------------------------------------")
    print("""Для работы этого теста необходимо запустить ответную часть test_email_server.py на другом ПК.
Для его работы необходимо ПО:
1. Установить Python не ниже v3.8. При установки обязательно
   указать добавление в PATH.\n""")
    send_email(sender_1, to_1, msg_1, list_bcc=bcc_1)  # Отправка Письма №1
    read_email(reader_1_pop3, "POP3")  # Получение письма № 2
    send_email(sender_1, to_3, msg_3, list_cc=cc_3)  # Отправка Письма №3
    read_email(reader_1_pop3, "POP3")  # Получение письма № 4
    print("\n--------------------------------------------------------------------------")
    return print("EMAIL end\n")


def i_answer():  # Отравитель №1

    global I_FIRST
    I_FIRST = False

    print("""Это ответная часть для теста №2 EMAIL (test_email.py).
Скрипт работает до принудительного завершения, логирование происходит в только в консоли.""")

    while True:
        read_email(reader_2_imap, "IMAP")  # Получение письма № 1
        send_email(sender_2, to_2, msg_2)  # Отправка Письма №2
        read_email(reader_2_imap, "IMAP")  # Получение письма № 3
        send_email(sender_2, to_4, msg_4, list_cc=cc_3)  # Отправка Письма №4
        print("--------------------------------------------------------------------------")
        print("EMAIL end\n")
