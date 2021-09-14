#!/usr/bin/python3
"""
Скрипт для автоматического тестирования im тестов 573.
Логирование команд происходит в консоли.
Работа с XMPP

Источник:
https://slixmpp.readthedocs.io/en/latest/index.html
"""
"""
# import time
from slixmpp import ClientXMPP
# Функция возврата времени из файла log_time.py
from log_time import cmd_time

# import logging  # Для системного логирования


try:
    # Только для Windows. Для работы скрипта на Windows, иначе ошибка NotImplementedError
    # Источник: https://github.com/saghul/aiodns/issues/78
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
except AttributeError:
    print("***** IM: CONTROL ERROR - NOT WINDOWS *****")


class EchoBot(ClientXMPP):
    # Атрибуты:
    # jid - аккаунт
    # password - пароль от jid
    # jid_to - кому отправляем сообщение
    # text_msg - текст сообщения
    def __init__(self, jid_from, password, jid_to=None, text_msg=None):
        ClientXMPP.__init__(self, jid_from, password)  # Создаём объект для соединения с сервером
        self.jid_from, self.jid_to, self.text_msg = jid_from, jid_to, text_msg
        #self.add_event_handler("session_start", self.session_start)
        #self.add_event_handler("message", self.message)


    def log_msg(self, msg):
        # Функция логирования
        msg_list = str(msg).split()  # Преобразование сообщения в список для логирования
        log_jid_from = self.jid_from if self.jid_to is not None else msg_list[1][6:-22]  # Определение отправителя
        log_jid_to = self.jid_from if self.jid_to is None else self.jid_to  # Определение получателя
        log_msg = self.text_msg if self.jid_to is not None else (msg_list[-2] + " " + msg_list[-1])[8:-17]  # Определение сообщения
        # Логирование
        print(f"FROM: {log_jid_from}")
        print(f"  TO: {log_jid_to}")
        print(f" MSG: {log_msg}")


    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        self.sender_msg()


    def sender_msg(self):
        # Начало теста, отправка тестового сообщение, на которое должен придти ответ.
        send_msg = self.make_message(mto=self.jid_to, mbody="test out", mtype='chat')
        send_msg.send()
        print(f"SEND {cmd_time()}")
        self.log_msg(send_msg)


    def message(self, msg):
        self.jid_to = None
        # Условие для контрольного ответа
        print(f"READ {cmd_time()}")
        self.log_msg(msg)


def i_sender():
    # Системное логирование
    # logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(read_message)s')

    print("\n\nIM sender_msg")
    print("----------------------------------------------------------------------------")

    # Логин и пароля от кого будет идти ответ и кому
    sender = EchoBot('test-rtc-nt@jabber.ru', 'zaq123edcxsw2', 'rtc-nt-test1@jabber.ru', 'test out')
    sender.connect(disable_starttls=True)
    sender.process(timeout=60)

    # Процесс мониторинга сообщений, атрибуты:
    # timeout = время его работы в секундах;
    # forever = True/False атрибут вечной работы;

    print("\n----------------------------------------------------------------------------")
    print("IM end")


i_sender()
"""

import slixmpp
from log_time import cmd_time


class SendMsgBot(slixmpp.ClientXMPP):

    def __init__(self, jid, password, recipient, message):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.recipient = recipient
        self.msg = message
        self.add_event_handler("session_start", self.sender_msg)

    def sender_msg(self, event):
        self.send_presence()
        self.get_roster()
        self.send_message(mto=self.recipient, mbody=self.msg, mtype='chat')
        print(f"SEND {cmd_time()}")
        print(f"FROM: {self.jid}")
        print(f"  TO: {self.recipient}")
        print(f" MSG: {self.msg}")
        self.disconnect()


class ReadMsgBot(slixmpp.ClientXMPP):

    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.jid = jid
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.reader_msg)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def reader_msg(self, msg):
        msg_list = str(msg).split()  # Преобразование сообщения в список для логирования
        print(f"READ {cmd_time()}")
        print(f"FROM: {msg_list[1][6:-22]}")  # Определение отправителя
        print(f"  TO: {self.jid}")  # Определение получателя
        print(f" MSG: {(msg_list[-2] + ' ' + msg_list[-1])[8:-17]}")  # Определение сообщения
        self.disconnect()


sender = SendMsgBot('test-rtc-nt@jabber.ru', 'zaq123edcxsw2', 'rtc-nt-test1@jabber.ru', 'test out')
sender.connect(disable_starttls=True)
sender.process(forever=False)
print()
reader = ReadMsgBot('test-rtc-nt@jabber.ru', 'zaq123edcxsw2')
reader.connect(disable_starttls=True)
reader.process(forever=False)
print()
sender = SendMsgBot('test-rtc-nt@jabber.ru', 'zaq123edcxsw2', 'rtc-nt-test1@jabber.ru', 'Отправка сообщения')
sender.connect(disable_starttls=True)
sender.process(forever=False)
print()
reader = ReadMsgBot('test-rtc-nt@jabber.ru', 'zaq123edcxsw2')
reader.connect(disable_starttls=True)
reader.process(forever=False)
print()
