import os

print("\n\n\nFTP start")
print("----------------------------------------------------------------------------")

print("\n Download ts.zip\n")
os.system("wget ftp://alta.ru/packets/distr/ts.zip")

print("\n\nDownload gtdw.zip\n")
os.system("wget ftp://alta.ru/packets/distr/gtdw.zip")

print("\n\nDownload maximum.zip\n")
os.system("wget ftp://alta.ru/packets/distr/maximum.zip")

print("\n----------------------------------------------------------------------------")
print("FTP end")