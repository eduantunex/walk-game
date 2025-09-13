import sqlite3 as sq
from colorama import Fore, init
import os
import random as rd
import time

init(autoreset=True)

conn = sq.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS save (
    jogador_x INTEGER, jogador_y INTEGER, passos INTEGER, money INTEGER,
    premio_x INTEGER, premio_y INTEGER
)
""")
conn.commit()

# Carrega save ou inicializa com valores padrão
save = cursor.execute("SELECT jogador_x, jogador_y, passos, money, premio_x, premio_y FROM save").fetchone()
if save is None:
    jogador_x, jogador_y, passos, money, premio_x, premio_y = 0, 0, 0, 0, None, None
    cursor.execute("INSERT INTO save VALUES (?, ?, ?, ?, ?, ?)", (jogador_x, jogador_y, passos, money, premio_x, premio_y))
    conn.commit()
else:
    jogador_x, jogador_y, passos, money, premio_x, premio_y = save

def gerar_premio():
    global premio_x, premio_y
    while True:
        novo_x = rd.randint(0, 29)
        novo_y = rd.randint(0, 9)
        if novo_x != jogador_x or novo_y != jogador_y:
            premio_x, premio_y = novo_x, novo_y
            cursor.execute("UPDATE save SET premio_x = ?, premio_y = ?", (premio_x, premio_y))
            conn.commit()
            break

def view_mapa(mapa):
    for linha in mapa:
        print(*linha)

# Loop principal
while True:
    if premio_x is None or premio_y is None:
        gerar_premio()

    os.system("clear")
    mapa = [["." for _ in range(30)] for _ in range(10)]
    mapa[jogador_y][jogador_x] = Fore.RED + "0"
    mapa[premio_y][premio_x] = Fore.GREEN + "P"
    view_mapa(mapa)

    print(f"X: {jogador_x} || Y: {jogador_y} || Dinheiro: ${money} || Passos: {passos}")

    comando = input("Digite w/a/s/d para mover: ").lower()

    if comando == "d" and jogador_x < 29:
        jogador_x += 1
        passos += 1
    elif comando == "a" and jogador_x > 0:
        jogador_x -= 1
        passos += 1
    elif comando == "s" and jogador_y < 9:
        jogador_y += 1
        passos += 1
    elif comando == "w" and jogador_y > 0:
        jogador_y -= 1
        passos += 1

    if jogador_x == premio_x and jogador_y == premio_y:
        ganho = rd.randint(100, 500)
        print(Fore.GREEN + f"Você pegou o prêmio! Ganhou ${ganho}")
        money += ganho
        gerar_premio()
        time.sleep(1)

    # Salva progresso
    cursor.execute("""
        UPDATE save SET jogador_x=?, jogador_y=?, passos=?, money=? 
    """, (jogador_x, jogador_y, passos, money))
    conn.commit()
