import random

def sortear_times(jogadores, num_times=2):
    goleiros = [j for j in jogadores if j.posicao == 'goleiro']
    linha = [j for j in jogadores if j.posicao != 'goleiro']

    random.shuffle(goleiros)
    random.shuffle(linha)

    # Ordena jogadores de linha por habilidade
    linha.sort(key=lambda j: j.habilidade, reverse=True)

    times = [[] for _ in range(num_times)]
    somas = [0] * num_times]

    # Distribui goleiros primeiro
    for i, goleiro in enumerate(goleiros):
        idx = i % num_times
        times[idx].append(goleiro)
        somas[idx] += goleiro.habilidade

    # Distribui jogadores equilibrando habilidade
    for jogador in linha:
        menor_time = somas.index(min(somas))
        times[menor_time].append(jogador)
        somas[menor_time] += jogador.habilidade

    return times