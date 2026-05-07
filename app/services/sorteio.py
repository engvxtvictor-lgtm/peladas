import random

def sortear_times(jogadores, num_times=2):
    # Ordena por habilidade decrescente
    jogadores_ordenados = sorted(jogadores, key=lambda j: j.habilidade, reverse=True)
    
    # Cria os times vazios
    times = [[] for _ in range(num_times)]
    somas = [0] * num_times

    # Distribui os jogadores equilibrando a soma de habilidades
    for jogador in jogadores_ordenados:
        # Coloca no time com menor soma
        time_mais_fraco = somas.index(min(somas))
        times[time_mais_fraco].append(jogador)
        somas[time_mais_fraco] += jogador.habilidade

    return times