from mapa import jogo, comando_clear
import os
import sqlite3 as sq
from colorama import Fore, Back, init, Style
import time

init(autoreset=True)

conn = sq.connect("database.db")
cursor = conn.cursor()

clear = comando_clear()

os.system(clear)

print(Fore.MAGENTA + "Bem vindo ao Game...")
time.sleep(1)
os.system(clear)
print(Fore.MAGENTA + "Desenvolvido por Antunes...")
time.sleep(3)

while True:
    os.system(clear)
    print(Fore.BLUE + """ Selecione uma opção:
          (1) Entrar no jogo 
          (2) Upgrades
          (0) Sair""")
    prompt = input(">>> ")
    if prompt == "1":
        jogo()
    elif prompt == "2":
        os.system(clear)
        print(Fore.YELLOW + "EM BREVE")
        time.sleep(2)
    elif prompt == "0":
        break
    else:
        os.system(clear)
        print(Fore.YELLOW + "Selecione uma opção correta!")
        time.sleep(2)