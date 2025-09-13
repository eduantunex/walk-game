import sqlite3 as sq
from colorama import Fore, init
import os
import random as rd
import time
import platform

init(autoreset=True)

# Função para definir o comando de limpar tela
def comando_clear():
    sistema = platform.system()
    if sistema == "Windows":
        return "cls"
    else:
        return "clear"

clear = comando_clear()

# Função para gerar um novo prêmio
def gerar_premio(jogador_x, jogador_y):
    while True:
        novo_x = rd.randint(1, 28)
        novo_y = rd.randint(1, 8)
        if novo_x != jogador_x or novo_y != jogador_y:
            return novo_x, novo_y

# Função para exibir o mapa
def view_mapa(mapa):
    for linha in mapa:
        print(*linha)

# Função principal do jogo
def jogo():
    conn = sq.connect("database.db")
    cursor = conn.cursor()

    # Cria tabela caso não exista
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS save (
            jogador_x INTEGER, jogador_y INTEGER, passos INTEGER, money INTEGER,
            premio_x INTEGER, premio_y INTEGER
        )
    """)
    conn.commit()

    # Carrega save ou inicializa com valores padrão
    save = cursor.execute("""
        SELECT jogador_x, jogador_y, passos, money, premio_x, premio_y FROM save
    """).fetchone()

    if save is None:
        jogador_x, jogador_y, passos, money = 1, 1, 0, 0
        premio_x, premio_y = gerar_premio(jogador_x, jogador_y)
        cursor.execute("""
            INSERT INTO save VALUES (?, ?, ?, ?, ?, ?)
        """, (jogador_x, jogador_y, passos, money, premio_x, premio_y))
        conn.commit()
    else:
        jogador_x, jogador_y, passos, money, premio_x, premio_y = save

    while True:
        os.system(clear)
        # Cria o mapa
        mapa = [["." for _ in range(30)] for _ in range(10)]
        mapa[jogador_y][jogador_x] = Fore.RED + "0"  # jogador
        mapa[premio_y][premio_x] = Fore.GREEN + "P"  # prêmio

        # Bordas em ciano
        for y in range(10):
            mapa[y][0] = Fore.CYAN + "."
            mapa[y][29] = Fore.CYAN + "."
        for x in range(30):
            mapa[0][x] = Fore.CYAN + "."
            mapa[9][x] = Fore.CYAN + "."

        view_mapa(mapa)
        print(f"X: {jogador_x} || Y: {jogador_y} || Dinheiro: ${money} || Passos: {passos}")

        comando = input("Digite w/a/s/d para mover (0 para sair): ").lower()

        if comando == "d" and jogador_x < 28:
            jogador_x += 1
            passos += 1
        elif comando == "a" and jogador_x > 1:
            jogador_x -= 1
            passos += 1
        elif comando == "s" and jogador_y < 8:
            jogador_y += 1
            passos += 1
        elif comando == "w" and jogador_y > 1:
            jogador_y -= 1
            passos += 1
        elif comando == "0":
            print("Saindo do jogo...")
            time.sleep(1)
            break

        # Coleta do prêmio
        if jogador_x == premio_x and jogador_y == premio_y:
            ganho = rd.randint(100, 500)
            print(Fore.GREEN + f"Você pegou o prêmio! Ganhou ${ganho}")
            money += ganho
            premio_x, premio_y = gerar_premio(jogador_x, jogador_y)
            time.sleep(1)

        # Salva progresso no banco
        cursor.execute("""
            UPDATE save SET jogador_x=?, jogador_y=?, passos=?, money=?, premio_x=?, premio_y=?
        """, (jogador_x, jogador_y, passos, money, premio_x, premio_y))
        conn.commit()

# Rodar o jogo
if __name__ == "__main__":
    jogo()
