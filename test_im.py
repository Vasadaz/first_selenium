#!/usr/bin/python3
"""
Скрипт для автоматического тестирования im тестов 573.
Логирование команд просисходит в консоле.
Работа с XMPP

Источник:
https://slixmpp.readthedocs.io/en/latest/index.html
"""

import time
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
    # jid = аккаунт test@jabber.ru
    # password = пароль от jid
    # how_first_send = None/1 условие для самостоятельной иницииации диалога, кто первый начинает?
    def __init__(self, jid, password, jid_to):
        ClientXMPP.__init__(self, jid, password)
        print("""Для работы этого теста необходимо запустить ответную часть test_im_serv.py на другом ПК.
Для его работы необходимо ПО:
1. Установить Python не ниже v3.8. При установки обязательно
   указать добавление в PATH.
2. Установка slixmpp для теста 3 >>> pip3 install slixmpp\n""")
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
        #   <message from="rtc-nt-test1@jabber.ru/6908052297956221828"
        # to="test-rtc-nt@jabber.ru/6162992849949770130" type="chat" xml:lang="en"
        # id="2e23b4aa49a8429e8b5a1a9f95ae5de3">
        # 	<origin-id xmlns="urn:xmpp:sid:0" id="2e23b4aa49a8429e8b5a1a9f95ae5de3" />
        # 	<body>
        # 			Получение сообщения
        # 	</body>
        # 	</message>

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
    xmpp.process(timeout=60)

    # Подключение к серверу XMPP jabber
    # disable_starttls=True отключаем шифрование, т.е TLS и поддержку STARTTLS.
    # Параметр должен стоять и у клиента и у сервера.
    # Источники:
    # https://slixmpp.readthedocs.io/en/latest/api/clientxmpp.html
    # https://stackru.com/questions/4521237/kak-otklyuchit-shifrovanie-v-lokalnoj-seti-xmpp
    xmpp.connect(disable_starttls=True)

    print(f"DISCONNECT")
    print("\n----------------------------------------------------------------------------")
    return print("IM end")

# start_im_test()
