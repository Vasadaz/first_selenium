#!/usr/bin/python3
"""
Скрипт для автоматического тестирования email тестов 573.
Логирование команд происходит в консоле.
Работа с IMAP

Источник:
https://habr.com/ru/post/51772/
https://habr.com/ru/company/truevds/blog/262819/
https://www.dmosk.ru/instruktions.php?object=python-mail

IMAP http://python-3.ru/page/imap-email-python

"""
import imaplib
import email
import time
import base64
# Функция возврата времени из файла log_time.py
from log_time import cmd_time


NEW_MILES = 0  # Маркер определения новых писем
STOP_IMAP = 0  # Маркер завершения функции pop3_email

def imap_email(host: list):
    global NEW_MILES, STOP_IMAP

    time.sleep(10)

    # Условие для завершения функции
    if STOP_IMAP == 5:
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

    msg_head = email.message_from_string(msg_content[0])  # Преобразуем str -> dict
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


# Отравитель
sender = ["rtc-nt-test1@yandex.ru", "zaq123edcxsw2", "imap.yandex.ru"]

print("\n\nIMAP start")
print("----------------------------------------------------------------------------")
imap_email(sender)
print("----------------------------------------------------------------------------")
print("IMAP end")
