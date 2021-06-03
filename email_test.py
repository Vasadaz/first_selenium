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
        msg["Сc"] = el  # Копия

    # Добавление скрытой копии
    for el in list_bcc:
        msg["Bcc"] = el  # Скрытая копия

    msg.attach(MIMEText(list_msg[1], "plain"))  # Добавляем в сообщение текст

    # Условие для определение вложения у письма
    if len(msg) > 2:
        filepath = "./email/constitution.pdf"  # Относительный путь к файлу во вложении
        filename = "constitution.pdf"  # Только имя файла

        with open(filepath, "rb") as fp:
            file = MIMEBase("application", "pdf")  # Используем общий MIME-тип
            file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
            fp.close()

        encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
        file.add_header("Content-Disposition", "attachment", filename=filename)  # Добавляем заголовки
        msg.attach(file)  # Присоединяем файл к сообщению

    server = smtplib.SMTP(list_from[2], int(list_from[3]))  # Создаем объект SMTP
    server.starttls()  # Начинаем шифрованный обмен по TLS
    server.login(list_from[0], list_from[1])  # Получаем доступ
    server.send_message(msg)  # Отправляем сообщение
    print("Отправили от {} на {}".format(list_from[0], list_to))
    server.quit()  # Выходим


from_1 = ["test@rtc-nt.ru", "", "mail.nic.ru", "587"]
to_1 = ["rtc-nt-test1@yandex.ru"]
cc_1 = ["rtc-nt-test2@yandex.ru", "rtc-nt-test3@yandex.ru"]
bcc_1 = ["rtc-nt-test4@yandex.ru"]
msg_1 = ["Отправка письма с 3 получателями, вложением, скрытой копией",
         "Текст письма"
         "./email/constitution.pdf"]

send_email(from_1, to_1, msg_1, list_cc=cc_1, list_bcc=bcc_1)

# send_email("rtc-nt-test1@yandex.ru", "", "test@rtc-nt.ru", "smtp.yandex.ru")
