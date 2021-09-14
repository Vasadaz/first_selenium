#!/usr/bin/python3
"""
Скрипт для автоматического тестирования im тестов 573.
Логирование команд происходит в консоли.
Работа с XMPP

Источник:
https://slixmpp.readthedocs.io/en/latest/index.html
"""

from slixmpp import ClientXMPP
from log_time import cmd_time
import csv
import time


class SendMsgBot(ClientXMPP):
    # Класс для отправки сообщения. аргументы:
    # jid аккаунт jabber и его пароль password
    # recipient получатель сообщения
    # message текст сообщения

    def __init__(self, jid: str, password: str, recipient: str, message: str):
        ClientXMPP.__init__(self, jid, password)  # Создание клиента для подключения
        self.recipient, self.msg = recipient, message  # Перенаправление  аргументов в среду self
        self.add_event_handler("session_start", self.session_start)  # Запуск функции sender_msg

    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        self.sender_msg()

    def sender_msg(self):
        self.send_message(mto=self.recipient, mbody=self.msg, mtype='chat')
        print(f"SEND {cmd_time()}")
        print(f"FROM: {self.jid}")
        print(f"  TO: {self.recipient}")
        print(f" MSG: {self.msg}")
        self.disconnect()


class ReadMsgBot(ClientXMPP):
    # Класс для чтения сообщения. аргументы:
    # jid аккаунт jabber и его пароль password

    def __init__(self, jid: str, password: str):
        ClientXMPP.__init__(self, jid, password)
        self.jid = jid
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        msg_list = str(msg).split()  # Преобразование сообщения в список для логирования
        print(f"READ {cmd_time()}")
        print(f"FROM: {msg_list[1][6:-22]}")  # Определение отправителя
        print(f"  TO: {self.jid}")  # Определение получателя
        print(f" MSG: {(msg_list[-2] + ' ' + msg_list[-1])[8:-17]}")  # Определение сообщения
        self.disconnect()


# Защит от отсутствия файла
try:
    # Открываем файл im_data.csv c данными для подключения
    with open("im_data.csv", "r") as im_data:
        im_data_list = csv.reader(im_data)  # Преобразуем строку из файла в список
        im_data_dict = {}  # Словарь для записи данных
        for line in im_data_list:
            im_data_dict[line[0]] = line[1:]  # Аккаунт jabber
        im_data.close()
except FileNotFoundError:
    print("***** IM: CONTROL ERROR - CSV File Not Found *****")  # Логирование.

jid_1 = im_data_dict["jid_1"]
jid_2 = im_data_dict["jid_2"]


def fun_sender(jid: str, password: str, recipient: str, message: str):
    sender = SendMsgBot(jid, password, recipient, message)
    sender.connect(disable_starttls=True)
    sender.process(forever=False)


def fun_reader(jid: str, password: str, time=None):
    if time is None:
        print("\n\nIM")
        print("----------------------------------------------------------------------------")
    reader = ReadMsgBot(jid, password)
    reader.connect(disable_starttls=True)
    reader.process(forever=True if time is None else time)


def i_sender():
    print("\n\nIM")
    print("----------------------------------------------------------------------------")
    fun_sender(jid_1[0], jid_1[1], jid_2[0], "test out")
    fun_reader(jid_1[0], jid_1[1], time=60)
    fun_sender(jid_1[0], jid_1[1], jid_2[0], "Отправка сообщения")
    fun_reader(jid_1[0], jid_1[1], time=60)
    print("\n----------------------------------------------------------------------------")
    print("IM end")

def i_answer():
    while True:
        fun_reader(jid_2[0], jid_2[1])
        fun_sender(jid_2[0], jid_2[1], jid_1[0], "test in")
        fun_reader(jid_2[0], jid_2[1])
        fun_sender(jid_2[0], jid_2[1], jid_1[0], "Получение сообщения")
        print("\n----------------------------------------------------------------------------")
        print("IM end")