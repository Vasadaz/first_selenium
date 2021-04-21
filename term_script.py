import subprocess
import time


def cmd_time():
    a = str(subprocess.check_output("date /t", shell=True).strip()).strip("b'")
    b = str(subprocess.check_output("time /t", shell=True).strip()).strip("b'")
    time.sleep(1)
    return str(a + " " + b)

my_timeout = 10

print("\n\n\nTELNET start")
print("----------------------------------------------------------------------------")

print("\n{}\nTELNET connecting towel.blinkenlights.nl ip:213.136.8.188".format(cmd_time()))
print("NOT CONNECTION")
subprocess.Popen(["putty", "-telnet", "towel.blinkenlights.nl"])
time.sleep(my_timeout)
subprocess.run("taskkill /IM putty.exe /F")

cmd_time()
print("\n{}\nTELNET connecting lord.stabs.org ip:192.241.222.161".format(cmd_time()))
subprocess.Popen(["putty", "-telnet", "lord.stabs.org"])
time.sleep(my_timeout)
subprocess.run("taskkill /IM putty.exe /F")

cmd_time()
print("\n{}\n\TELNET connecting 35.185.12.150".format(cmd_time()))
subprocess.Popen(["putty", "-telnet", "35.185.12.150"])
subprocess.run("taskkill /IM putty.exe /F")
time.sleep(my_timeout)
subprocess.run("taskkill /IM putty.exe /F")

print("----------------------------------------------------------------------------")
print("TELNET end")

print("\n\nSSH start")
print("----------------------------------------------------------------------------")

print("\n{}\nSSH connecting 195.144.107.198".format(cmd_time()))
subprocess.Popen(["putty", "-ssh", "195.144.107.198"])
time.sleep(my_timeout)
subprocess.run("taskkill /IM putty.exe /F")


print("\n{}\nSSH connecting sdf.org ip:205.166.94.16".format(cmd_time()))
subprocess.Popen(["putty", "-ssh", "sdf.org"])
time.sleep(my_timeout)
subprocess.run("taskkill /IM putty.exe /F")

print("\n----------------------------------------------------------------------------")
print("SSH end")
