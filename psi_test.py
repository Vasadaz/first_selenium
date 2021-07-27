#!/usr/bin/python3
"""
Скрипт для автоматического тестирования im тестов 573.
Логирование команд просисходит в консоле.
Работа с XMPP

Источник:
https://github.com/louiz/slixmpp
"""

import time
from slixmpp import ClientXMPP
# import logging  # Для системного логирования

# Windows. Для работы скрипта на Windows, иначе ошибка NotImplementedError
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class EchoBot(ClientXMPP):
    # Атрибуты:
    # jid = аккаунт test@jabber.ru
    # password = пароль от jid
    # how_first_send = None/1 условие для самостоятельной иницииации диалога, кто первый начинает?
    def __init__(self, jid, password, how_first_send=None):
        ClientXMPP.__init__(self, jid, password)
        print(f"CONNECT as {jid}")
        self.how_first_send = how_first_send
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    def session_start(self, event):

        self.send_presence()
        self.get_roster()
        # Начало теста, отправка тестового сообщение, на которое должен придти ответ.
        if self.how_first_send == 1:
            print("I'm first sender!")
            #first_msg = self.make_message(mto="rtc-nt-test1@jabber.ru", mbody="test out", mtype='chat')
            first_msg = self.make_message(mto="test-rtc-nt@jabber.ru", mbody="test out", mtype='chat')
            first_msg.send()
            print(f'SEND №1:\n  {first_msg}\n\n')

    def message(self, msg):
        # print(msg)
        # Вид msg:
        # <message from="test-rtc-nt@jabber.ru/DESKTOP-0T8DF1D" to="rtc-nt-test1@jabber.ru/12115888673434915089" xml:lang="ru" id="ab22a" type="chat">
        # <body>555</body>
        # <active xmlns="http://jabber.org/protocol/chatstates" />
        # <request xmlns="urn:xmpp:receipts" />
        # </message>

        # Условие для определения инициатора диалога.
        if self.how_first_send == 1:
            # Условие для контрольного ответа
            if msg['body'] == "test in":
                print(f'INPUT №2:\n  {msg}\n\n')
                time.sleep(10)
                msg.reply("Отправка сообщения").send()  # Отправляем на тотже адрес откуда пришло сообщение
                print(f'SEND №3:\n  {msg}\n\n')

            # условие окончания переписуки
            elif msg['body'] == "Полученик сообщения":
                print(f'INPUT №4:\n  {msg}\n\n')

        else:
            # Условие для тестового ответа
            if msg['body'] == "test out":
                print(f'INPUT №1:\n  {msg}\n\n')
                time.sleep(10)
                msg.reply("test in").send()  # Отправляем на тотже адрес откуда пришло сообщение
                print(f'SEND №2:\n  {msg}\n\n')

            # Условие для контрольного ответа
            elif msg['body'] == "Отправка сообщения":
                print(f'INPUT №3:\n  {msg}\n\n')
                time.sleep(10)
                msg.reply("Получение сообщения").send()  # Отправляем на тотже адрес откуда пришло сообщение
                print(f'SEND №4:\n  {msg}\n\n')


# Системное логирование
# logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

# Логин и пароля от кого будет идти ответ
xmpp = EchoBot('rtc-nt-test1@jabber.ru', 'zaq123edcxsw2')
# xmpp = EchoBot('test-rtc-nt@jabber.ru', 'zaq123edcxsw2', 1)

# Подключение к серверу XMPP jabber
xmpp.connect()

# Процесс мониторинга сообщенией, атрибуты:
# timeout = время его работы в секундах;
# forever = True/False атрибут вечной работы;
xmpp.process(timeout=40)

# Отключение от сервера
xmpp.disconnect()