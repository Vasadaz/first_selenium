import time

# webdriver это и есть набор команд для управления браузером
from selenium import webdriver
print("\n\n\nHTTP start")
print("----------------------------------------------------------------------------")
# инициализируем драйвер браузера. После этой команды вы должны увидеть новое открытое окно браузера
driver = webdriver.Chrome()

my_timeout = 10

# команда time.sleep устанавливает паузу в 5 секунд, чтобы мы успели увидеть, что происходит в браузере
time.sleep(my_timeout)

# Метод get сообщает браузеру, что нужно открыть сайт по указанной ссылке
driver.get("http://kremlin.ru")
time.sleep(my_timeout)

driver.get("http://kremlin.ru/acts/constitution")
time.sleep(my_timeout)

driver.get("http://kremlin.ru/static/pdf/constitution.pdf?6fbd2dc717")
time.sleep(my_timeout)

driver.get("http://fsb.ru")
time.sleep(my_timeout)

driver.get("http://khann.ru")
time.sleep(my_timeout)

driver.get("http://khann.ru/wallpapers/")
time.sleep(my_timeout)

driver.get("http://alex-kuznetsov.ru/test")
time.sleep(my_timeout)

try:
    driver.get("http://www.thesheep.info")
    time.sleep(my_timeout)
except:
    pass

try:
    driver.get("http://www.grani.ru")
    time.sleep(my_timeout)
except:
    pass


# После выполнения всех действий мы должны не забыть закрыть окно браузера
driver.quit()
print("\n----------------------------------------------------------------------------")
print("HTTP end")
