#!/usr/bin/python3
"""
Скрипт для автоматического тестирования VOIP тестов 573.
Логирование команд просисходит в консоле.
Работа с SIP

Источник:
https://most-voip.readthedocs.io/en/latest/python_docs/tutorial/voip_tutorial_1.html
"""

# add the most.voip library root dir to the current python path...
import sys
sys.path.append("")

# import the Voip Library
from most.voip.api import VoipLib

# instanziate the lib
my_voip = VoipLib()
