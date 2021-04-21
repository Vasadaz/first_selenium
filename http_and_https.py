import time

# webdriver это и есть набор команд для управления браузером
from selenium import webdriver


def cmd_time():
    # Месное время
    local_time = time.localtime()
    local_time_str = "{:0>2d}:{:0>2d}:{:0>2d}".format(local_time.tm_hour, local_time.tm_min, local_time.tm_sec)

    # UTC время
    utc_time = time.gmtime()
    utc_time_str = "{:0>2d}:{:0>2d}:{:0>2d}".format(utc_time.tm_hour, utc_time.tm_min, utc_time.tm_sec)

    return "{} (utc {})".format(local_time_str, utc_time_str)


def http_test(protocol: str, sait_list: list):
    print("\n\n{} start".format(protocol))
    print("----------------------------------------------------------------------------")
    print("Open browser")

    # Инициализируем драйвер браузера. После этой команды вы должны увидеть новое открытое окно браузера
    driver = webdriver.Chrome()
    time.sleep(5)

    for el in sait_list:
        print("\n{}\n{} {}".format(cmd_time(), protocol, el))
        # Перенаправление ошибки вдля заблокированых ресурсов
        try:
            # Метод get сообщает браузеру, что нужно открыть сайт по указанной ссылке
            driver.get(el)
        except:
            print("***** CONTROL ERROR *****")
        time.sleep(10)

    # После выполнения всех действий мы должны не забыть закрыть окно браузера
    driver.quit()
    driver.quit()
    print("\nClose browser")
    print("----------------------------------------------------------------------------")
    print("{} end".format(protocol))
    return


http_list = ["http://kremlin.ru",
             "http://kremlin.ru/acts/constitution",
             "http://kremlin.ru/static/pdf/constitution.pdf?6fbd2dc717",
             "http://fsb.ru",
             "http://khann.ru",
             "http://khann.ru/wallpapers/",
             "http://alex-kuznetsov.ru/test",
             "http://www.thesheep.info",
             "http://www.grani.ru"]
http_test("HTTP", http_list)

https_list = ["https://yandex.ru",
              "https://mail.ru",
              "https://rambler.ru",
              "https://2ip.ru",
              "https://cia.gov",
              "https://nsa.gov",
              "https://ssu.gov.ua",
              "https://mossad.gov.il",
              "https://sis.gov.uk",
              "https://bnd.bund.de"]
http_test("HTTPS", https_list)
