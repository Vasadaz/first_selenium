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


def pop3_email(host: list):
    global NEW_MILES



    server = poplib.POP3(host[2])
    # server.set_debuglevel(1)  # Системный лог, дебагер
    server.user(host[0])
    server.pass_(host[1])
    mails = server.list()[1]

    if NEW_MILES == 0:
        NEW_MILES = len(mails)

    if NEW_MILES > len(mails):
        NEW_MILES = len(mails)
    else:
        print("No new mails!\n")
        time.sleep(5)
        pop3_email(host)

    print("CONNECTION")
    lines = server.retr(NEW_MILES)[1]
    msg_content = b'\r\n'.join(lines).decode('utf-8').split("--/")
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
sender_2 = ["rtc-nt-test1@yandex.ru", "zaq123edcxsw2", "pop3.yandex.ru"]

print("\n\nPOP3 start")
print("----------------------------------------------------------------------------")
if I_FIRST:
    pop3_email(sender_1)
else:
    pop3_email(sender_2)
print("----------------------------------------------------------------------------")
print("POP3 end")
