
# Тест 573
### Описание
##### Главный файл avto_573.py
Логирование присходит внутри консоли без записи в файл, 
поэтому для избежания потери лога скрипт останавливается 
путём закрытия кнсоли. Изпользуются дополнительные ПО взависимости от ОС.
Можно запустить отдельные тесты вводя их номера:
- 1 - http
- 2 - ftp
- 3 - telnet
- 4 - ssh
- 5 - https
- Все - пустая строка.
> 135 >>> Запуск тестов для http, telnet, https

___
## Дополнитльное ПО

### Windows:
1. Установить Python не ниже v3.8. При установки обязательно
   указать добавление в PATH.
   ![img.png](img/img1.png)
2. Установить Putty
3. Chrome >= v90
### Linux:
1. Chrome >= v90
___
## Установка chromedriver
Chromedriver официальный драйвер для управления Chrome.
Скрипт использует библиотеку selenium для управления браузером.
### Windows:
1. Скопировать директорию /soft_for_script/win/chromedriver в корень C:\
2. Добавить в PATH путь C:\chromedriver
   ![img.png](img/img2.png)
   ![img.png](img/img3.png)
   ![img.png](img/img4.png)
   ![img.png](img/img5.png)
3. Проверка установки командой >>> chromedriver
4. Установка selenium командой >>> pip install selenium

### Linux:
1. Переходим в директорию /soft_for_script/linux
2. Выполняем команды
   - sudo mv chromedriver /usr/local/bin/chromedriver
   - sudo chown root:root /usr/local/bin/chromedriver
   - sudo chmod +x /usr/local/bin/chromedriver
3. Проверка установки командой >>> chromedriver
4. Установка selenium командой >>> pip install selenium
