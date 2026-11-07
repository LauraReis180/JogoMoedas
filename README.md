# 🪙 Caça às Moedas

**30 segundos para provar sua agilidade!**

Colete o máximo de moedas que conseguir antes do tempo acabar e tente superar o seu recorde.

## 🎮 Como jogar

- Clique em **▶ INICIAR JOGO**
- Clique nas moedas que aparecem na tela
  - 🟡 Moeda dourada: **+1 ponto**
  - 🔴 Moeda vermelha: **+5 pontos** (20% de chance)
- No máximo 6 moedas ficam na tela ao mesmo tempo
- Quando o tempo chega a zero, a partida acaba e o recorde fica salvo

## ▶️ Como executar

Requisito: **Python 3** (o Tkinter já vem junto no Windows).

```bash
python main.py
```

## 📁 Estrutura do projeto

```
JogoMoedas/
├── main.py         → ponto de entrada
├── estado.py       → dados compartilhados + semáforo
├── threads.py      → cronômetro e gerador de moedas
└── interface.py    → tela, desenhos e cliques (Tkinter)
```

## 🧵 Threads

| Thread | Função |
|---|---|
| Cronômetro | Desconta 1 segundo do tempo da partida |
| Gerador de moedas | Cria uma moeda em posição aleatória a cada 0,8 s |
| Principal (interface) | Mantém a janela responsiva, recebe os cliques e desenha a tela |

## 🔒 Semáforo

As threads acessam os mesmos dados (pontos, tempo, moedas e recorde). Para evitar **condição de corrida**, o jogo usa um semáforo binário:

```python
self.semaforo = threading.Semaphore(1)
```

Toda leitura e escrita desses dados acontece dentro de `with estado.semaforo:`, garantindo que **apenas uma thread por vez** entre na região crítica.

## 📚 Bibliotecas

`tkinter` · `threading` · `random` · `time`

## 👩‍💻 Autoras

- Laura da Silva Reis
- Letícia Camilo de Souza
