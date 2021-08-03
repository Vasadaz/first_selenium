#!/usr/bin/python3
"""
Скрипт для автоматического тестирования email тестов 573.
Логирование команд просисходит в консоле.
Работа с IMAP, SMTP, POP3

Источник:
https://habr.com/ru/post/51772/
SMTP https://code.tutsplus.com/ru/tutorials/sending-emails-in-python-with-smtp--cms-29975
     https://habr.com/ru/post/495256/
IMAP http://python-3.ru/page/imap-email-python
POP3 https://www.code-learner.com/python-use-pop3-to-read-email-example/
"""

# import necessary packages


import smtplib  # Импортируем библиотеку по работе с SMTP
import time
from email import encoders  # Импортируем энкодер
from email.mime.base import MIMEBase  # Общий тип файла
from email.mime.text import MIMEText  # Тип для Текст/HTML
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект


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

    msg = MIMEMultipart()  # Создаем сообщение
    msg["From"] = list_from[0]  # Отправитель

    # Добавление получателей
    for el in list_to:
        msg["To"] = el  # Получатель

    msg["Subject"] = list_msg[0]  # Тема сообщения

    # Добавление копии
    for el in list_cc:
        msg["Cc"] = el  # Копия

    # Добавление скрытой копии
    for el in list_bcc:
        msg["Bcc"] = el  # Скрытая копия

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


    server = smtplib.SMTP(list_from[2], int(list_from[3]))  # Создаем объект SMTP (сервер, порт)
    # server.starttls()  # Начинаем шифрованный обмен по TLS
    server.set_debuglevel(1)  # Системные логи, дебагер
    server.login(list_from[0], list_from[1])  # Получаем доступ (email, пароль)
    server.send_message(msg)  # Отправляем сообщение
    print("Отправили от {} на {}\n".format(list_from[0], list_to))
    server.quit()  # Выходим

    print("--------------------------------------------------\n\n\n")
    time.sleep(10)


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
to_3 = ["rtc-nt-test1@yandex.ru"]
cc_3 = ["rtc-nt-test2@yandex.ru", "rtc-nt-test3@yandex.ru"]
msg_3 = ["Отправка письма с 2 копиями и иероглифы",  # Тема письма
         "لِيَتَقَدَّسِ اسْمُكَ"]  # Текст письма

send_email(sender, to_1, msg_1, list_bcc=bcc_1)  # Отправка Письма №1
send_email(sender, to_3, msg_3, list_cc=cc_3)  # Отправка Письма №3
