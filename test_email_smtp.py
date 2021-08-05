#!/usr/bin/python3
"""
Скрипт для автоматического тестирования email тестов 573.
Логирование команд происходит в консоле.
Работа с SMTP

Источник:
https://habr.com/ru/post/51772/
https://habr.com/ru/company/truevds/blog/262819/

SMTP https://code.tutsplus.com/ru/tutorials/sending-emails-in-python-with-smtp--cms-29975
     https://habr.com/ru/post/495256/
"""

import smtplib  # Импортируем библиотеку по работе с SMTP
from email import encoders  # Импортируем энкодер
from email.mime.base import MIMEBase  # Общий тип файла
from email.mime.text import MIMEText  # Тип для Текст/HTML
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
# Функция возврата времени из файла log_time.py
from log_time import cmd_time


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
        filepath = f"./email/{list_msg[2]}"  # Относительный путь к файлу во вложении
        filename = f"{list_msg[2]}"  # Только имя файла

        with open(filepath, "rb") as fp:
            file = MIMEBase("application", "pdf")  # Используем общий MIME-тип
            file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
            fp.close()

        encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
        file.add_header("Content-Disposition", "attachment", filename=filename)  # Добавляем заголовки
        msg.attach(file)  # Присоединяем файл к сообщению

    message = """From: =?UTF-8?B?0KLQtdGB0YLQtdGA?= <test@rtc-nt.ru>
Subject: =?UTF-8?B?0J7RgtC/0YDQsNCy0LrQsCDQv9C40YHRjNC80LAg0YEgMiDQutC+0L8=?=
 =?UTF-8?B?0LjRj9C80Lgg0Lgg0LjQtdGA0L7Qs9C70LjRhNGL?=
To: =?UTF-8?B?0KLQtdGB0YIgMSDQoNCi0Jot0J3QoiAx?= <rtc-nt-test1@ya.ru>
Cc: 2 <rtc-nt-test2@ya.ru>, 3 <rtc-nt-test3@ya.ru>
Message-ID: <edb5d967-3346-7dc8-bbc7-474b5bf406f8@rtc-nt.ru>
Date: Tue, 4 Aug 2021 15:46:31 +0300
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101
 Thunderbird/78.12.0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8; format=flowed
Content-Transfer-Encoding: 8bit
Content-Language: ru\r\n""" + list_msg[1]

    server = smtplib.SMTP(list_from[2], int(list_from[3]))  # Создаем объект SMTP (сервер, порт)
    # server.starttls()  # Начинаем шифрованный обмен по TLS
    # server.set_debuglevel(1)  # Системные логи, дебагер

    # Способ аутентификации №1
    server.user, server.password = list_from[0], list_from[1]  # Присваиваем email, пароль
    server.ehlo()  # Отправляем серверу SMTP EHLO запрос
    server.auth('plain', server.auth_plain)  # Аутентификация на сервере по механизму PLAIN

    # Способ аутентификации №2
    # server.login(list_from[0], list_from[1])  # Получаем доступ (email, пароль)

    server.sendmail(list_from[0], list_to[0], message.encode('utf8'))  # Отправка письма

    # Логирование
    print("\n\nSMTP start")
    print("----------------------------------------------------------------------------")
    print(cmd_time())
    print(f"FROM: {list_from[0]}")
    print(f"  TO: {', '.join(list_to)}")
    print(f"  CC: {', '.join(list_cc)}") if len(list_cc) != 0 else None
    print(f" BCC: {', '.join(list_bcc)}") if len(list_bcc) != 0 else None
    print(f" SUB: {list_msg[0]}")
    print(f"TEXT: {list_msg[1]}")
    print(f"FILE: {list_msg[2]}") if len(list_msg) > 2 else None
    server.quit()  # Выходим
    print("\n----------------------------------------------------------------------------")
    return print("SMTP end")


# Вставь пароль для отправки |
#                            V
sender = ["test@rtc-nt.ru", "Elcom101120", "mail.nic.ru", "587"]

# Письмо №1
to_1 = ["rtc-nt-test1@yandex.ru", "rtc-nt-test2@yandex.ru", "rtc-nt-test3@yandex.ru"]
bcc_1 = ["rtc-nt-test4@yandex.ru"]
msg_1 = ["Отправка письма с 3 получателями, вложением, скрытой копией",  # Тема письма
         "Текст письма Python",  # Текст письма
         "constitution.pdf"]  # Прикреплённый файл из ./email/

# Письмо №3
to_3 = ["rtc-nt-test4@yandex.ru"]
cc_3 = ["rtc-nt-test2@yandex.ru", "rtc-nt-test3@yandex.ru"]
msg_3 = ["ОТ питона",  # Тема письма
         "АВТО текст механизм PLAINَ"]  # Текст письма

send_email(sender, to_1, msg_1, list_bcc=bcc_1)  # Отправка Письма №1
send_email(sender, to_3, msg_3)  # Отправка Письма №3
