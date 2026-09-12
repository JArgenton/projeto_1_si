from core.tempura_simulada.ajuste_temperatura import ajustar_temperatura_inicial
from core.uteis.uteis import gerar_entrada_aleatoria, calcular_custo_swap_aleatorio, calcular_custo,gerar_matriz_custo_aleatoria, resolver_forca_bruta
import time

import math
import random

def aceitar_swap(custo_atual,  custo_novo, temperatura):
    diff = custo_novo - custo_atual
    
    if diff <= 0: # verificar -> H com mov laterais
        return True
    
    probabilidade = math.exp(-diff / temperatura)
    r = random.random()
    
    return r < probabilidade

def executar_tempera_simulada(
    matriz_custo, 
    tamanho, 
    constante_resfriamento, 
    aceitacao, 
    temp_minima, estabilidade_termica): 

    T0 = ajustar_temperatura_inicial(matriz_custo, tamanho, aceitacao)

    atual = gerar_entrada_aleatoria(tamanho)
    custo_atual = calcular_custo(matriz_custo, atual)
    melhor_custo = custo_atual
    melhor_solucao = atual.copy()
    temperatura = T0
    exc_apos_melhor = 0
    estabilidade = tamanho * estabilidade_termica if estabilidade_termica > 0 else 1
    while temperatura > temp_minima:
        for i in range(0,estabilidade):
            custo_novo, novo = calcular_custo_swap_aleatorio(matriz_custo, atual, tamanho)

            if aceitar_swap(custo_atual, custo_novo, temperatura): 
                atual = novo
                custo_atual = custo_novo

                if custo_atual < melhor_custo:
                    exc_apos_melhor = 0
                    melhor_custo = custo_atual
                    melhor_solucao = atual.copy()
            exc_apos_melhor +=1
        temperatura = temperatura * constante_resfriamento
    return melhor_solucao, melhor_custo, custo_atual, atual, exc_apos_melhor

if __name__ == '__main__':
    TAMANHO = 22

    TEMP_MIN = 0.01
    ACEITACAO = 0.85
    DECAIMENTO = 0.97
    ESTABILIDADE_TERMICA = 0
    
    matriz_custo = gerar_matriz_custo_aleatoria(TAMANHO)
    
    inicio_tempera = time.time()
    melhor_solucao, melhor_custo, custo_atual, atual, tempo_apos_melhor = executar_tempera_simulada(
        matriz_custo, TAMANHO, DECAIMENTO, ACEITACAO, TEMP_MIN, ESTABILIDADE_TERMICA
    )
    fim_tempera = time.time()
    tempo_tempera = fim_tempera - inicio_tempera

    MAX_EXECUCOES_FB = 100000
    sol_fb, custo_fb, total_avaliado = resolver_forca_bruta(
        matriz_custo, TAMANHO, max_execucoes=MAX_EXECUCOES_FB
    )
    
    print(f"tempera -> Melhor Rota:| Melhor Custo: {melhor_custo} (ultima solucao: | ultimo custo: {custo_atual}) | Tempo: {tempo_tempera:.4f}s")
    print(f"Força Bruta -> Melhor Rota:  | Melhor Custo: {custo_fb} (Avaliadas {total_avaliado} rotas)")
    print("tempo apos melhor", tempo_apos_melhor)