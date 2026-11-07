import threading

# CONFIGURACOES DO JOGO
LARGURA = 720
ALTURA = 350
DURACAO = 30
MAX_MOEDAS = 6


# DADOS COMPARTILHADOS ENTRE AS THREADS
class EstadoJogo:
    def __init__(self):
        # SEMAFORO
        self.semaforo = threading.Semaphore(1)

        # DADOS COMPARTILHADOS
        self.pontos = 0
        self.tempo = DURACAO
        self.recorde = 0
        self.rodando = False
        self.partida = 0
        self.moedas = []
