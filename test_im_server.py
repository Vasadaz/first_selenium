#!/usr/bin/python3
"""
СЕРВЕРНЫЙ АВТООТВЕТЧИК

Для его работы необходимо ПО:
1. Установить Python не ниже v3.8. При установки обязательно
   указать добавление в PATH.
2. Установка slixmpp для теста 3 >>> pip3 install slixmpp

Скрипт для автоматического тестирования im тестов 573.
Логирование команд происходит в консоли.
Работа с XMPP

Источник:
https://slixmpp.readthedocs.io/en/latest/index.html
"""

from test_im import i_answer

i_answer()