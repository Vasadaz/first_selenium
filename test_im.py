#!/usr/bin/python3
"""
Скрипт для автоматического тестирования im тестов 573.
Логирование команд просисходит в консоле.
Работа с XMPP

Источник:

"""

import time
from slixmpp import ClientXMPP
# Функция возврата времени из файла log_time.py
from log_time import cmd_time

# import logging  # Для системного логирования


'''
# Только для Windows. Для работы скрипта на Windows, иначе ошибка NotImplementedError
# Источник: https://github.com/saghul/aiodns/issues/78
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#'''


class EchoBot(ClientXMPP):
    # Атрибуты:
    # jid = аккаунт test@jabber.ru
    # password = пароль от jid
    # how_first_send = None/1 условие для самостоятельной иницииации диалога, кто первый начинает?
    def __init__(self, jid, password, jid_to):
        ClientXMPP.__init__(self, jid, password)
        print(f"CONNECT as {jid}")
        self.jid_to = jid_to
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

        # Начало теста, отправка тестового сообщение, на которое должен придти ответ.
        print("I'm first sender!")
        first_msg = self.make_message(mto=self.jid_to, mbody="test out", mtype='chat')
        first_msg.send()
        first_msg_log = str(first_msg).replace("<body>", "<body>\n\t\t\t").replace("<", "\n\t<")
        print(f'SEND №1 {cmd_time()}:{first_msg_log}\n\n')

    def message(self, msg):
        # print(msg)
        # Вид msg:
        # <message from="test-rtc-nt@jabber.ru/DESKTOP-0T8DF1D" to="rtc-nt-test1@jabber.ru/12115888673434915089" xml:lang="ru" id="ab22a" type="chat">
        # <body>555</body>
        # <active xmlns="http://jabber.org/protocol/chatstates" />
        # <request xmlns="urn:xmpp:receipts" />
        # </message>

        # Условие для контрольного ответа
        if msg['body'] == "test in":
            msg_log = str(msg).replace("<body>", "<body>\n\t\t\t").replace("<", "\n\t<")
            print(f'INPUT №2 {cmd_time()}:{msg_log}\n\n')
            time.sleep(10)
            answer_msg = msg.reply("Отправка сообщения")  # Создание обратного сообщения
            answer_msg.send()  # Отправляем на тотже адрес откуда пришло сообщение
            answer_msg_log = str(answer_msg).replace("<body>", "<body>\n\t\t\t").replace("<", "\n\t<")
            print(f'SEND №3 {cmd_time()}:{answer_msg_log}\n\n')

        # условие окончания переписуки
        elif msg['body'] == "Получение сообщения":
            msg_log = str(msg).replace("<body>", "<body>\n\t\t\t").replace("<", "\n\t<")
            print(f'INPUT №4 {cmd_time()}:{msg_log}\n\n')




def start_im_test():
    # Системное логирование
    # logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

    print("\n\nIM start")
    print("----------------------------------------------------------------------------")

    # Логин и пароля от кого будет идти ответ
    xmpp = EchoBot('test-rtc-nt@jabber.ru', 'zaq123edcxsw2', 'rtc-nt-test1@jabber.ru')

    # Подключение к серверу XMPP jabber
    xmpp.connect()

    # Процесс мониторинга сообщенией, атрибуты:
    # timeout = время его работы в секундах;
    # forever = True/False атрибут вечной работы;
    xmpp.process()

    # Отключение от сервера
    xmpp.disconnect()

    print(f"DISCONNECT")
    print("\n----------------------------------------------------------------------------")
    return print("IM end")

#start_im_test()
