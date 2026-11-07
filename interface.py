import tkinter as tk
import threading

from estado import EstadoJogo, LARGURA, ALTURA, DURACAO
from threads import cronometro, gerar_moedas

# CORES
FUNDO = "#0f172a"
PAINEL = "#1e293b"
AMARELO = "#facc15"
AZUL = "#38bdf8"
ROSA = "#fb7185"


class JogoMoedas:
    def __init__(self, janela):
        self.janela = janela
        janela.title("Caça às Moedas")
        janela.configure(bg=FUNDO)
        janela.resizable(False, False)

        # DADOS COMPARTILHADOS + SEMAFORO (estado.py)
        self.estado = EstadoJogo()

        # TITULO
        titulo = tk.Label(
            janela,
            text="CAÇA ÀS MOEDAS",
            bg=FUNDO,
            fg=AMARELO,
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=(10, 0))

        tk.Label(
            janela,
            text="30 segundos para provar sua agilidade!",
            bg=FUNDO,
            fg="white",
            font=("Arial", 11)
        ).pack(pady=(2, 8))

        # PAINEL DE PONTUACAO
        painel = tk.Frame(janela, bg=PAINEL)
        painel.pack(fill="x", padx=16)

        self.lbl_pontos = self.criar_indicador(
            painel, "PONTOS", AMARELO, 0, 0
        )

        self.lbl_tempo = self.criar_indicador(
            painel, "TEMPO", AZUL, 0, 1
        )

        self.lbl_recorde = self.criar_indicador(
            painel, "RECORDE", ROSA, 0, 2
        )

        for i in range(3):
            painel.columnconfigure(i, weight=1)

        # STATUS
        self.status = tk.Label(
            janela,
            text="Pronto para jogar!",
            bg=FUNDO,
            fg="#cbd5e1",
            font=("Arial", 10)
        )
        self.status.pack(pady=(5, 3))

        # AREA DO JOGO
        self.tela = tk.Canvas(
            janela,
            width=LARGURA,
            height=ALTURA,
            bg="#dbeafe",
            highlightthickness=0
        )
        self.tela.pack(padx=16, pady=(0, 8))
        self.tela.bind("<Button-1>", self.clicar)

        # BOTAO INICIAR JOGO
        self.botao = tk.Button(
            janela,
            text="▶ INICIAR JOGO",
            command=self.iniciar,
            bg="#22c55e",
            fg="white",
            activebackground="#16a34a",
            font=("Arial", 13, "bold"),
            relief="flat",
            cursor="hand2",
            padx=28,
            pady=7
        )
        self.botao.pack(pady=(0, 4))

        # INSTRUCOES
        tk.Label(
            janela,
            text="MOEDA DOURADA: +1     |     MOEDA VERMELHA: +5",
            bg=FUNDO,
            fg="#cbd5e1",
            font=("Arial", 10)
        ).pack(pady=(0, 10))

        self.tela_inicial()

        janela.protocol(
            "WM_DELETE_WINDOW",
            self.fechar
        )

    # CRIAR PAINEL DE INFORMACOES
    def criar_indicador(self, pai, nome, cor, linha, coluna):
        quadro = tk.Frame(pai, bg=PAINEL)

        quadro.grid(
            row=linha,
            column=coluna,
            sticky="ew",
            pady=7
        )

        tk.Label(
            quadro,
            text=nome,
            bg=PAINEL,
            fg=cor,
            font=("Arial", 11, "bold")
        ).pack()

        valor = tk.Label(
            quadro,
            text="0",
            bg=PAINEL,
            fg="white",
            font=("Arial", 18, "bold")
        )
        valor.pack()

        return valor

    # DESENHAR FUNDO DO JOGO
    def desenhar_fundo(self):
        self.tela.delete("all")

        self.tela.create_rectangle(
            0, 0, LARGURA, ALTURA,
            fill="#dbeafe",
            outline=""
        )

        # GRAMA
        self.tela.create_rectangle(
            0, ALTURA - 42,
            LARGURA, ALTURA,
            fill="#86efac",
            outline=""
        )

        # NUVENS
        for x, y in ((95, 48), (560, 65)):
            for dx, dy, rx, ry in (
                (-35, 0, 40, 18),
                (0, -10, 45, 25),
                (35, 0, 40, 18)
            ):
                self.tela.create_oval(
                    x + dx - rx,
                    y + dy - ry,
                    x + dx + rx,
                    y + dy + ry,
                    fill="white",
                    outline=""
                )

    # CAIXA CENTRAL
    def caixa_central(self, titulo, linhas, cor=AMARELO):
        self.tela.create_rectangle(
            92, 83,
            LARGURA - 92, 280,
            fill=FUNDO,
            outline=cor,
            width=3
        )

        self.tela.create_text(
            LARGURA // 2, 128,
            text=titulo,
            fill=cor,
            font=("Arial", 24, "bold")
        )

        self.tela.create_text(
            LARGURA // 2, 205,
            text=linhas,
            fill="white",
            width=490,
            justify="center",
            font=("Arial", 13)
        )

    # TELA INICIAL
    def tela_inicial(self):
        self.desenhar_fundo()

        self.caixa_central(
            "CAÇA ÀS MOEDAS",
            "Colete o máximo de moedas em 30 segundos!\n\n"
            "Dourada = 1 ponto       Vermelha = 5 pontos\n\n"
            "Clique no botão abaixo para começar."
        )

    # INICIAR PARTIDA
    def iniciar(self):
        estado = self.estado

        with estado.semaforo:
            if estado.rodando:
                return

            estado.partida += 1
            atual = estado.partida

            estado.pontos = 0
            estado.tempo = DURACAO
            estado.moedas.clear()
            estado.rodando = True

        self.botao.config(
            text="JOGANDO...",
            state="disabled"
        )

        self.atualizar_tela(atual)

        # THREAD 1: CRONOMETRO (threads.py)
        threading.Thread(
            target=cronometro,
            args=(estado, atual),
            daemon=True
        ).start()

        # THREAD 2: GERACAO DE MOEDAS (threads.py)
        threading.Thread(
            target=gerar_moedas,
            args=(estado, atual),
            daemon=True
        ).start()

    # COLETAR MOEDAS
    def clicar(self, evento):
        estado = self.estado

        with estado.semaforo:
            if not estado.rodando:
                return

            for moeda in estado.moedas:
                x, y, valor = moeda

                raio = 26 if valor == 5 else 22

                distancia = (
                    (evento.x - x) ** 2
                    + (evento.y - y) ** 2
                )

                if distancia <= raio ** 2:
                    estado.moedas.remove(moeda)
                    estado.pontos += valor

                    estado.recorde = max(
                        estado.recorde,
                        estado.pontos
                    )
                    break

    # DESENHAR MOEDAS
    def desenhar_moeda(self, x, y, valor):
        raio = 26 if valor == 5 else 22

        cor = ROSA if valor == 5 else AMARELO

        borda = (
            "#be123c"
            if valor == 5
            else "#ca8a04"
        )

        # SOMBRA
        self.tela.create_oval(
            x - raio + 3,
            y - raio + 4,
            x + raio + 3,
            y + raio + 4,
            fill="#94a3b8",
            outline=""
        )

        # MOEDA
        self.tela.create_oval(
            x - raio,
            y - raio,
            x + raio,
            y + raio,
            fill=cor,
            outline=borda,
            width=3
        )

        self.tela.create_text(
            x, y,
            text=f"+{valor}",
            fill=(
                "white"
                if valor == 5
                else "#78350f"
            ),
            font=("Arial", 14, "bold")
        )

    # ATUALIZAR INTERFACE
    def atualizar_tela(self, atual):
        estado = self.estado

        with estado.semaforo:
            if atual != estado.partida:
                return

            pontos = estado.pontos
            tempo = estado.tempo
            recorde = estado.recorde
            rodando = estado.rodando
            moedas = list(estado.moedas)

        self.lbl_pontos.config(text=str(pontos))
        self.lbl_tempo.config(text=f"{tempo}s")
        self.lbl_recorde.config(text=str(recorde))

        if not rodando:
            self.desenhar_fundo()

            self.caixa_central(
                "FIM DE JOGO!",
                f"Pontuação final: {pontos}\n"
                f"Recorde: {recorde}\n\n"
                "Clique em Jogar novamente!",
                "#22c55e"
            )

            self.botao.config(
                text="↻ JOGAR NOVAMENTE",
                state="normal"
            )

            self.status.config(
                text="Partida encerrada"
            )
            return

        self.status.config(
            text="Partida em andamento - clique nas moedas!"
        )

        self.desenhar_fundo()

        for x, y, valor in moedas:
            self.desenhar_moeda(x, y, valor)

        self.janela.after(
            50,
            lambda: self.atualizar_tela(atual)
        )

    # FECHAR O JOGO
    def fechar(self):
        estado = self.estado

        with estado.semaforo:
            estado.rodando = False
            estado.partida += 1

        self.janela.destroy()
