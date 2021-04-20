import time

# webdriver это и есть набор команд для управления браузером
from selenium import webdriver

print("\n\n\nHTTPS start")
print("----------------------------------------------------------------------------")
# инициализируем драйвер браузера. После этой команды вы должны увидеть новое открытое окно браузера
driver = webdriver.Chrome()

# команда time.sleep устанавливает паузу в 5 секунд, чтобы мы успели увидеть, что происходит в браузере
time.sleep(5)

# Метод get сообщает браузеру, что нужно открыть сайт по указанной ссылке

driver.get("https://yandex.ru")
time.sleep(5)

driver.get("https://mail.ru")
time.sleep(5)

driver.get("https://rambler.ru")
time.sleep(5)

driver.get("https://2ip.ru")
time.sleep(5)

driver.get("https://cia.gov")
time.sleep(5)

driver.get("https://nsa.gov")
time.sleep(5)

driver.get("https://ssu.gov.ua")
time.sleep(5)

driver.get("https://mossad.gov.il")
time.sleep(5)

driver.get("https://sis.gov.uk")
time.sleep(5)

driver.get("https://bnd.bund.de")
time.sleep(5)

# После выполнения всех действий мы должны не забыть закрыть окно браузера
driver.quit()
print("\n----------------------------------------------------------------------------")
print("HTTPS end")