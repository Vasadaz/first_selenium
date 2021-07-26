#!/usr/bin/python3
"""
Скрипт для автоматического тестирования im тестов 573.
Логирование команд просисходит в консоле.
Работа с XMPP

Источник:
https://github.com/louiz/slixmpp
"""

import logging
import time
from slixmpp import ClientXMPP


class EchoBot(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

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
            time.sleep(10)
            msg.reply("test in").send()

        # Условие для контрольного ответа
        elif msg['body'] == "Отправка сообщения":
            time.sleep(10)
            msg.reply("Получение сообщения").send()

        # Ответ на любое другое сообщение
        else:
            time.sleep(10)
            msg.reply(f"OT: {msg['from']} \nПОЛУЧЕНО: {msg['body']}").send()

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

    # Логин и пароля от кого будет идти ответ
    xmpp = EchoBot('rtc-nt-test1@jabber.ru', 'zaq123edcxsw2')

    # Подключение к серверу XMPP jabber
    xmpp.connect()

    # Процесс мониторинга сообщенией, атрибуты:
    # timeout = время его работы в секундах;
    # forever = True/False атрибут вечной работы;
    xmpp.process(timeout=100)