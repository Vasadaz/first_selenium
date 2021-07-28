#!/usr/bin/python3
"""
СЕРВЕРНЫЙ АВТООТВЯЕТЧИК
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
'''


class EchoBot(ClientXMPP):
    # Атрибуты:
    # jid = аккаунт test@jabber.ru
    # password = пароль от jid
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        print(""""Это ответная часть для теста №3 IM (test_im.py).
Скрипт работает до принудительного завершения, логирование происходит в только в консоле.

Для его работы необходимо ПО:
1. Установить Python не ниже v3.8. При установки обязательно
   указать добавление в PATH.
   ![img.png](img/img1.png)
2. Установка slixmpp для теста 3 >>> pip3 install slixmpp
        """)
        print(f"CONNECT as {jid}")
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)


    def session_start(self, event):
        self.send_presence()
        self.get_roster()


    def message(self, msg):
        # print(msg)
        # Вид msg:
        # <message from="test-rtc-nt@jabber.ru/DESKTOP-0T8DF1D" to="rtc-nt-test1@jabber.ru/12115888673434915089" xml:lang="ru" id="ab22a" type="chat">
        # <body>555</body>
        # <active xmlns="http://jabber.org/protocol/chatstates" />
        # <request xmlns="urn:xmpp:receipts" />
        # </message>

        # Условие для тестового ответа
        if msg['body'] == "test out":
            print("\n\nIM start")
            print("----------------------------------------------------------------------------")
            msg_log = str(msg).replace("<body>", "<body>\n\t\t\t").replace("<", "\n\t<")
            print(f'INPUT №1 {cmd_time()}:{msg_log}\n\n')
            time.sleep(10)
            answer_msg = msg.reply("test in")  # Создание обратного сообщения
            answer_msg.send()  # Отправляем на тотже адрес откуда пришло сообщение
            answer_msg_log = str(answer_msg).replace("<body>", "<body>\n\t\t\t").replace("<", "\n\t<")
            print(f'SEND №2 {cmd_time()}:{answer_msg_log}\n\n')

        # Условие для контрольного ответа
        elif msg['body'] == "Отправка сообщения":
            msg_log = str(msg).replace("<body>", "<body>\n\t\t\t").replace("<", "\n\t<")
            print(f'INPUT №3 {cmd_time()}:{msg_log}\n\n')
            time.sleep(10)
            answer_msg = msg.reply("Получение сообщения")  # Создание обратного сообщения
            answer_msg.send()  # Отправляем на тотже адрес откуда пришло сообщение
            answer_msg_log = str(answer_msg).replace("<body>", "<body>\n\t\t\t").replace("<", "\n\t<")
            print(f'SEND №4 {cmd_time()}:{answer_msg_log}')
            print("----------------------------------------------------------------------------")
            return print("IM end")


# Системное логирование
# logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

# Логин и пароля от кого будет идти ответ
xmpp = EchoBot('rtc-nt-test1@jabber.ru', 'zaq123edcxsw2')


# Подключение к серверу XMPP jabber
xmpp.connect()

# Процесс мониторинга сообщенией, атрибуты:
# timeout = время его работы в секундах;
# forever = True/False атрибут вечной работы;
xmpp.process()

# Отключение от сервера
xmpp.disconnect()

print(f"DISCONNECT")
input("\nEXIT?")
