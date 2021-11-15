import os

#
RELEASE = "v1.5.3"

__LOGS_NAME = "nameless"


def print_in_log(text: str):
    try:
        os.mkdir("logs")
    except FileExistsError:
        pass

    os.chdir("./logs")  # Меняем рабочую директорию

    # Проверяем создан ли файл для записи в списке файлов внутри директории logs
    if __LOGS_NAME in tuple(os.walk(os.getcwd()))[0][-1]:
        print("yes")
        logs_file = open(__LOGS_NAME, mode="a")
        logs_file.write(text + '\n')
    else:
        print("no")
        logs_file = open(__LOGS_NAME, mode="x")
        logs_file.write(text + '\n')

    print(text)
    os.chdir("../")  # Меняем рабочую директорию


#print_in_log("DSF")
