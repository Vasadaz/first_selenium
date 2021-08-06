#!/usr/bin/python3
"""
Скрипт для автоматического тестирования email тестов 573.
Логирование команд происходит в консоле.
Работа с POP3

Источник:
https://habr.com/ru/post/51772/
https://habr.com/ru/company/truevds/blog/262819/

POP3 https://www.code-learner.com/python-use-pop3-to-read-email-example/
"""

import poplib
import time
import base64
import email
# from email.parser import Parser
# Функция возврата времени из файла log_time.py
from log_time import cmd_time

I_FIRST = True  # True - инициатор, False - автоответчик
#I_FIRST = False  # True - инициатор, False - автоответчик
NEW_MILES = 0  # Маркер определения новых писем
STOP_POP3 = 0  # Маркер завершения функции pop3_email

def pop3_email(host: list):
    # Передаётся список el: str in [email, pass, server]
    global I_FIRST, NEW_MILES, STOP_POP3

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
        print("No new mails!\n")
        time.sleep(5)
        pop3_email(host)
        return

    lines = server.retr(NEW_MILES)[1]
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    msg_head = email.message_from_string(msg_content[0])
    msg_text = base64.b64decode(msg_content[1].split()[-1]).decode('utf-8')
    msg_file = msg_content[2].split()[8][10:-1] if len(msg_content) > 3 else None

    msg_subject_decode = str()
    for el in (msg_head.get('Subject')).split():
        msg_subject_decode += base64.b64decode(el[10:-2]).decode('utf-8')

    print(cmd_time())
    print(f"FROM: {msg_head.get('From')}")
    print(f"  TO: {msg_head.get('To')}")
    print(f"  CC: {msg_head.get('Cc')}") if msg_head.get('Cc') != (None or "") else None
    print(f" BCC: {msg_head.get('Bcc')}") if msg_head.get('Bcc') != None else None
    print(f" SUB: {msg_subject_decode}")
    print(f"TEXT: {msg_text}")
    print(f"FILE: {msg_file}") if msg_file != None else None
    print()

    server.quit()
    time.sleep(10)
    pop3_email(host)


# Отравитель №1
sender_1 = ["test@rtc-nt.ru", "Elcom101120", "mail.nic.ru", "587"]
# Отравитель №2
sender_2 = ["rtc-nt-test1@yandex.ru", "zaq123edcxsw2", "pop.yandex.ru"]

print("\n\nPOP3 start")
print("----------------------------------------------------------------------------")
if I_FIRST:
    pop3_email(sender_1)
else:
    pop3_email(sender_2)
print("----------------------------------------------------------------------------")
print("POP3 end")
