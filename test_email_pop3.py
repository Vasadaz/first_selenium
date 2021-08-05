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
from email.parser import Parser
# Функция возврата времени из файла log_time.py
from log_time import cmd_time

# input email address, password and pop3 server domain or ip address

NEW_MILES = 0

def pop3_email(email="test@rtc-nt.ru",
               password="Elcom101120",
               pop3_server="mail.nic.ru"):
    global NEW_MILES


    server = poplib.POP3(pop3_server)
    # server.set_debuglevel(1)  # Системный лог, дебагер
    # pop3_server_welcome_msg = server.getwelcome().decode('utf-8')
    # user account authentication
    server.user(email)
    server.pass_(password)
    # stat() function return email count and occupied disk size
    # print('Messages: %s. Size: %s' % server.stat())
    # list() function return all email list
    mails= server.list()[1]
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
    msg_content = b'\r\n'.join(lines).decode('utf-8')

    msg = Parser().parsestr(msg_content)
    print(cmd_time())
    print(f"FROM: {msg.get('From')}")
    print(f"  TO: {msg.get('To')}")
    print(f"  CC: {msg.get('Cc')}") if msg.get('Cc') != (None or "") else None
    print(f" BCC: {msg.get('Bcc')}") if msg.get('Bcc') != None else None
    print(f" SUB: {(msg.get('Subject')).encode('utf-8')}")
    print(f"TEXT: ")
    print(f"FILE: {msg.get('Content-Disposition')}")
    print()
    print(msg)
    server.quit()
    time.sleep(10)

    pop3_email()

print("\n\nPOP3 start")
print("----------------------------------------------------------------------------")
pop3_email()
print("\n----------------------------------------------------------------------------")
print("POP3 end")

