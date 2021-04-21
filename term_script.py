import subprocess
import time


def cmd_time():
    # Месное время
    local_time = time.localtime()
    local_time_str = "{:0>2d}:{:0>2d}:{:0>2d}".format(local_time.tm_hour, local_time.tm_min, local_time.tm_sec)

    # UTC время
    utc_time = time.gmtime()
    utc_time_str = "{:0>2d}:{:0>2d}:{:0>2d}".format(utc_time.tm_hour, utc_time.tm_min, utc_time.tm_sec)

    return "{} (utc {})".format(local_time_str, utc_time_str)


def terminal_test(protocol: str, hosts_list: list):
    print("\n\n{} start".format(protocol))
    print("----------------------------------------------------------------------------")

    flag = "-telnet" if len(protocol) > 3 else "-ssh"

    for el in hosts_list:
        print("\n{}\n{} {}".format(cmd_time(), protocol, el))
        subprocess.Popen(["putty", flag, el])
        time.sleep(10)
        subprocess.run("taskkill /IM putty.exe /F")

    print("\n----------------------------------------------------------------------------")
    print("{} end".format(protocol))
    return


telnet_list = ["towel.blinkenlights.nl",
               "lord.stabs.org",
               "35.185.12.150"]
terminal_test("TELNET", telnet_list)

ssh_list = ["195.144.107.198",
            "sdf.org"]
terminal_test("SSH", ssh_list)
