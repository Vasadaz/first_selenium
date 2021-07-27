
# Тест 573
### Описание
##### Главный файл avto_573.py
Логирование присходит внутри консоли без записи в файл, 
поэтому для избежания потери лога скрипт останавливается 
путём закрытия кнсоли. Изпользуются дополнительные ПО взависимости от ОС.
Можно запустить отдельные тесты вводя их номера:
- 1 - http
- 2 - email(None)
- 3 - im
- 4 - voip(None)
- 5 - ftp
- 6 - telnet
- 7 - ssh
- 8 - https
- Все - пустая строка.
> 135 >>> Запуск тестов для http, telnet, https

___
## Дополнитльное ПО

### Windows:
1. Установить Python не ниже v3.8. При установки обязательно
   указать добавление в PATH.
   ![img.png](img/img1.png)
2. Установить Putty
3. Установить Chrome >= v90
### Linux:
1. Установить wget командой >>> sudo apt install wget
2. Установить Chrome >= v90
___
## Установка chromedriver
Chromedriver официальный драйвер для управления Chrome.
Скрипт использует библиотеку selenium для управления браузером.
### Windows:
1. Скопировать директорию /soft_for_script/win/chromedriver в корень C:\
2. Добавить в PATH путь C:\chromedriver с помощью одного из способов:
2.1. Команда >>> setx /m MYWEBPC "C:\chromedriver" 
2.2. Графический интерфейс:
   ![img.png](img/img2.png)
   ![img.png](img/img3.png)
   ![img.png](img/img4.png)
   ![img.png](img/img5.png)
3. Проверка установки командой >>> chromedriver
4. Установка selenium для тестов 1 и 8 >>> pip3 install selenium
5. Установка slixmpp для теста 3 >>> pip3 install selenium

### Linux:
1. Переходим в директорию /test_573/soft_for_script/linux
2. Запустить скрипт avto_setting.sh или выполняем команды:
   - sudo mv chromedriver /usr/local/bin/chromedriver
   - sudo chown root:root /usr/local/bin/chromedriver
   - sudo chmod +x /usr/local/bin/chromedriver
3. Проверка установки командой >>> chromedriver
4. Установка selenium командой >>> pip3 install selenium
