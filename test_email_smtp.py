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

import time
# Функция возврата времени из файла log_time.py
from log_time import cmd_time


#I_FIRST = True  # True - инициатор, False - автоответчик
I_FIRST = False  # True - инициатор, False - автоответчик

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
    print("SMTP end")
    time.sleep(10)


# Отравитель №1
sender_1 = ["test@rtc-nt.ru", "Elcom101120", "mail.nic.ru", "587"]
# Письмо №1
to_1 = ["rtc-nt-test1@yandex.ru", "rtc-nt-test2@yandex.ru", "rtc-nt-test3@yandex.ru"]
bcc_1 = ["rtc-nt-test4@yandex.ru"]
msg_1 = ["АВТО Отправка письма с 3 получателями, вложением и скрытой копией",  # Тема письма
         "Текст письма Python",  # Текст письма
         "constitution.pdf"]  # Прикреплённый файл из ./email/
# Письмо №3
to_3 = ["rtc-nt-test4@yandex.ru"]
cc_3 = ["rtc-nt-test2@yandex.ru", "rtc-nt-test3@yandex.ru"]
msg_3 = ["АВТО Отправка письма с 2 копиями и иероглифами",  # Тема письма
         "لِيَتَقَدَّسِ اسْمُكَ"]  # Текст письма

# Отравитель №2
sender_2 = ["rtc-nt-test1@yandex.ru", "zaq123edcxsw2", "smtp.yandex.ru", "587"]
# Письмо №2
to_2 = ["test@rtc-nt.ru", "rtc-nt-test2@yandex.ru", "rtc-nt-test3@yandex.ru"]
msg_2 = ["АВТО Получение письма с 3 получателями и вложением\r\n",  # Тема письма
         "Текст письма",  # Текст письма
         "constitution.pdf"]  # Прикреплённый файл из ./email/
# Письмо №4
to_4 = ["test@rtc-nt.ru"]
cc_4 = ["rtc-nt-test2@yandex.ru", "rtc-nt-test3@yandex.ru"]
msg_4 = ["АВТО Получение письма с 2 копиями и иероглифами\r\n",  # Тема письма
         "لِيَتَقَدَّسِ اسْمُكَ"]  # Текст письма

# Условие для инициирования переписки
if I_FIRST:
    # Отравитель №1
    send_email(sender_1, to_1, msg_1, list_bcc=bcc_1)  # Отправка Письма №1
    send_email(sender_1, to_3, msg_3)  # Отправка Письма №3
else:
    # Отравитель №12
    send_email(sender_2, to_2, msg_2)  # Отправка Письма №2
    send_email(sender_2, to_4, msg_4, list_cc=cc_4)  # Отправка Письма №4