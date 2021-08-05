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

# import python poplib module
import poplib
from email.parser import Parser
# input email address, password and pop3 server domain or ip address
email = "test@rtc-nt.ru"
password = "Elcom101120"
pop3_server = "mail.nic.ru"
# connect to pop3 server:
server = poplib.POP3(pop3_server)
# open debug switch to print debug information between client and pop3 server.
# server.set_debuglevel(1)
# get pop3 server welcome message.
pop3_server_welcome_msg = server.getwelcome().decode('utf-8')
# print out the pop3 server welcome message.
print(server.getwelcome().decode('utf-8'))
# user account authentication
server.user(email)
server.pass_(password)
# stat() function return email count and occupied disk size
print('Messages: %s. Size: %s' % server.stat())
# list() function return all email list
resp1, mails, octets1 = server.list()
print(mails)
# retrieve the newest email index number
index = len(mails)
# server.retr function can get the contents of the email with index variable value index number.
resp2, lines, octets2 = server.retr(index)
# lines stores each line of the original text of the message
# so that you can get the original text of the entire message use the join function and lines variable.
msg_content = b'\r\n'.join(lines).decode('utf-8')
# now parse out the email object.
msg = Parser().parsestr(msg_content)
# get email from, to, subject attribute value.
email_from = msg.get('From')
email_to = msg.get('To')
email_subject = msg.get('Subject')

print(msg_content)
print(email_subject)

# delete the email from pop3 server directly by email index.
# server.dele(index)
# close pop3 server connection.
server.quit()
