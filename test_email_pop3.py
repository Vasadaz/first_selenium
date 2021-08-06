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

# input email address, password and pop3 server domain or ip address

NEW_MILES = 0


def pop3_email(email_addr="test@rtc-nt.ru",
               password="Elcom101120",
               pop3_server="mail.nic.ru"):
    global NEW_MILES

    server = poplib.POP3(pop3_server)
    # server.set_debuglevel(1)  # Системный лог, дебагер
    # pop3_server_welcome_msg = server.getwelcome().decode('utf-8')
    # user account authentication
    server.user(email_addr)
    server.pass_(password)
    # stat() function return email count and occupied disk size
    # print('Messages: %s. Size: %s' % server.stat())
    # list() function return all email list
    mails = server.list()[1]
    """
    if NEW_MILES == 0:
        NEW_MILES = len(mails)
    """
    if NEW_MILES != len(mails):
        NEW_MILES = len(mails)
    else:
        print("No new mails!\n")
        time.sleep(5)
        pop3_email()

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

    # print(msg)
    server.quit()
    time.sleep(10)

    pop3_email()


print("\n\nPOP3 start")
print("----------------------------------------------------------------------------")
pop3_email()
print("\n----------------------------------------------------------------------------")
print("POP3 end")
