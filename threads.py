import random
import time

from estado import LARGURA, ALTURA, MAX_MOEDAS


# THREAD RESPONSAVEL PELO TEMPO
def cronometro(estado, atual):
    while True:
        time.sleep(1)

        with estado.semaforo:
            if not estado.rodando or atual != estado.partida:
                return

            estado.tempo -= 1

            if estado.tempo <= 0:
                estado.tempo = 0
                estado.rodando = False
                return


# THREAD RESPONSAVEL PELAS MOEDAS
def gerar_moedas(estado, atual):
    while True:
        time.sleep(0.8)

        x = random.randint(38, LARGURA - 38)
        y = random.randint(38, ALTURA - 65)

        # 20% de chance de moeda especial
        valor = 5 if random.random() < 0.2 else 1

        with estado.semaforo:
            if not estado.rodando or atual != estado.partida:
                return

            if len(estado.moedas) < MAX_MOEDAS:
                estado.moedas.append((x, y, valor))
