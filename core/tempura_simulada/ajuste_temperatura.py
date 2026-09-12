import random
from core.uteis.uteis import (calcular_custo, swap, 
                   calculate_natural_log, 
                   gerar_entrada_aleatoria, 
                   calcular_custo_swap_aleatorio)

def ajustar_temperatura_inicial(matriz_custo, tamanho: int, aceitacao: float) -> float: 
    n_amostras = int(tamanho * 5)
    
    amostras = variacao_por_random_walk(matriz_custo, n_amostras, tamanho)
    
    if not amostras:
        return 100
        
    media_delta_E = sum(amostras) / len(amostras)
    
    T0 = - media_delta_E / calculate_natural_log(aceitacao)
    return T0


def variacao_por_random_walk(matriz_custo, n_amostras: int, tamanho: int) -> list:
    amostras = []
    atual = gerar_entrada_aleatoria(tamanho)
    
    iteracoes = 0
    max_iteracoes = n_amostras * 10
    
    while len(amostras) < n_amostras and iteracoes < max_iteracoes:
        custo_1 = calcular_custo(matriz_custo, atual)
        custo_2, novo = calcular_custo_swap_aleatorio(matriz_custo, atual, tamanho)

        delta_E = custo_2 - custo_1
        
        if delta_E > 0:
            amostras.append(delta_E)
            
        atual = novo
        iteracoes += 1
        
    return amostras