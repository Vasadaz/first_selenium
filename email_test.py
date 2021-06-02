#!/usr/bin/python3
"""
Скрипт для автоматического тестирования email тестов 573.
Логирование команд просисходит в консоле.

Источник:
https://codius.ru/articles/Python_%D0%9A%D0%B0%D0%BA_%D0%BE%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D1%82%D1%8C_%D0%BF%D0%B8%D1%81%D1%8C%D0%BC%D0%BE_%D0%BD%D0%B0_%D1%8D%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D0%BD%D0%BD%D1%83%D1%8E_%D0%BF%D0%BE%D1%87%D1%82%D1%83
https://www.dmosk.ru/instruktions.php?object=python-mail
"""

import smtplib  # Импортируем библиотеку по работе с SMTP
from email import encoders  # Импортируем энкодер
from email.mime.base import MIMEBase  # Общий тип файла
from email.mime.text import MIMEText  # Тип для Текст/HTML
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект


def send_email(list_from: list, list_to: list, list_msg: list, list_cc=None, list_bcc=None):
    # Все данные в списках должныи иметь строковый тип
    # list_from список отправителя, формат: [email , pass, почтовый сервера, порт почтового сервера]
    # list_to список получателя, формат: [email №1, ..., email №n]
    # list_msg список для формирования письма, формат: [тема письма, текст письма, путь к относительный путь]
    # list_cc (необязательный аргумент) список адресов копии, формат: [email №1, ..., email №n]
    # list_bcc (необязательный аргумент) список адресов скрытой копии, формат: [email №1, ..., email №n]
    #
    #

    msg = MIMEMultipart()  # Создаем сообщение
    msg["From"] = list_from[0]  # Отправитель
    msg["To"] = list_to # Получатель
    msg["Subject"] = list_msg[0]  # Тема сообщения

    body = list_msg[1]
    msg.attach(MIMEText(body, "plain"))  # Добавляем в сообщение текст

    filepath = "./email/constitution.pdf"  # Имя файла в абсолютном или относительном формате
    filename = "constitution.pdf" # Только имя файла

    with open(filepath, "rb") as fp:
      file = MIMEBase("application", "pdf")  # Используем общий MIME-тип
      file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
      fp.close()

    encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
    file.add_header("Content-Disposition", "attachment", filename=filename)  # Добавляем заголовки
    msg.attach(file) # Присоединяем файл к сообщению

    server = smtplib.SMTP(list_from[2], list_from[3])  # Создаем объект SMTP
    server.starttls()  # Начинаем шифрованный обмен по TLS
    server.login(list_from[0], list_from[1])  # Получаем доступ
    server.send_message(msg)  # Отправляем сообщение
    print("Отправили от {} на {}".format(list_from[0], list_to))
    server.quit()  # Выходим


send_email("test@rtc-nt.ru", "", "rtc-nt-test1@yandex.ru", "mail.nic.ru")
send_email("rtc-nt-test1@yandex.ru", "", "test@rtc-nt.ru", "smtp.yandex.ru")


