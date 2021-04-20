import os

print("\n\n\nTERMINAL TELNET start")
print("----------------------------------------------------------------------------")

print("\nTELNET connecting towel.blinkenlights.nl")
os.system("putty -telnet towel.blinkenlights.nl")

print("\nTELNET connecting lord.stabs.org")
os.system("putty -telnet  lord.stabs.org")

print("\n\TELNET connecting 35.185.12.150")
os.system("putty -telnet 35.185.12.150")
# taskkill /IM putty.exe /F
print("----------------------------------------------------------------------------")
print("TERMINAL TELNET end")

print("\n\n\nTERMINAL SSH start")
print("----------------------------------------------------------------------------")

print("\nSSH connecting 195.144.107.198")
os.system("putty -ssh  195.144.107.198")

print("\n\SSH connecting sdf.org")
os.system("putty -ssh sdf.org")

print("\n----------------------------------------------------------------------------")
print("TERMINAL SSH end")
