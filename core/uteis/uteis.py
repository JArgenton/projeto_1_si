import itertools
import math
import random


def calcular_custo(matriz_custo, caminho):
    custo = 0
    n = len(caminho)
    for i in range(n):
        u = caminho[i]
        v = caminho[(i + 1) % n]
        custo += matriz_custo[u][v]
    return custo


def swap(vetor: list, pos1: int, pos2: int) -> list:
    copia = vetor.copy()
    copia[pos1], copia[pos2] = copia[pos2], copia[pos1]
    return copia


def calculate_avg(values: list):
    if not values:
        return 0
    return sum(values) / len(values)


def calculate_natural_log(value):
    return math.log(value)


def calculate_desv_pad(values: list):
    if not values:
        return 0

    media = calculate_avg(values)
    soma_diferencas_quadrado = sum((value - media) ** 2 for value in values)

    variancia = soma_diferencas_quadrado / len(values)

    return math.sqrt(variancia)


def gerar_entrada_aleatoria(tamanho: int) -> list:
    return random.sample(range(tamanho), tamanho)


def calcular_custo_swap_aleatorio(matriz_custo, atual, tamanho) -> int:
    pos1, pos2 = random.sample(range(tamanho), 2)
    novo = swap(atual, pos1, pos2)
    return calcular_custo(matriz_custo, novo), novo


def gerar_matriz_custo_aleatoria(
    tamanho: int, min_dist: int = 10, max_dist: int = 25, simetrica: bool = True
) -> list:
    matriz = [[0] * tamanho for _ in range(tamanho)]
    for i in range(tamanho):
        for j in range(i + 1, tamanho):
            dist = random.randint(min_dist, max_dist)
            matriz[i][j] = dist
            if simetrica:
                matriz[j][i] = dist
            else:
                matriz[j][i] = random.randint(min_dist, max_dist)
    return matriz


def resolver_forca_bruta(matriz_custo: list, tamanho: int, max_execucoes: int = 100000):
    cidades_restantes = list(range(1, tamanho))
    melhor_custo = math.inf
    melhor_solucao = []

    execucoes = 0
    for perm in itertools.permutations(cidades_restantes):
        if execucoes >= max_execucoes:
            break

        rota = [0] + list(perm)
        custo = calcular_custo(matriz_custo, rota)

        if custo < melhor_custo:
            melhor_custo = custo
            melhor_solucao = rota

        execucoes += 1

    return melhor_solucao, melhor_custo, execucoes
