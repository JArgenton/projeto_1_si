import time

from core.genetico import AG
from core.tempura_simulada.tempera_simulada import executar_tempera_simulada
from core.uteis.uteis import (
    gerar_matriz_custo_aleatoria,
    resolver_forca_bruta,
)


def comparar_algoritmos():
    TAMANHO = 100
    # tempura
    TEMP_MIN = 0.001
    ACEITACAO = 0.90
    DECAIMENTO = 0.999
    ESTABILIDADE_TERMICA = 1

    # AG
    MAX_EXECUCOES_AG = 600
    P_FITNESS = 2.5
    TAXA_CROSSOVER = 0.8
    TAXA_MUTACAO = 1 / (20 * TAMANHO)

    MAX_EXECUCOES_FB = 100000

    matriz_custo = gerar_matriz_custo_aleatoria(TAMANHO)

    print(f"=== TESTE {TAMANHO} CIDADES ===\n")

    inicio_ts = time.perf_counter()
    sol_ts, custo_ts, _, _, _ = executar_tempera_simulada(
        matriz_custo,
        TAMANHO,
        DECAIMENTO,
        ACEITACAO,
        TEMP_MIN,
        ESTABILIDADE_TERMICA,
    )
    tempo_ts = time.perf_counter() - inicio_ts

    inicio_ag = time.perf_counter()
    ag = AG(
        TAMANHO,
        matriz_custo,
        P_FITNESS,
        TAXA_CROSSOVER,
        MAX_EXECUCOES_AG,
        TAXA_MUTACAO,
    )
    custo_ag, sol_ag = ag.executar()
    tempo_ag = time.perf_counter() - inicio_ag

    inicio_fb = time.perf_counter()
    sol_fb, custo_fb, total_avaliado = resolver_forca_bruta(
        matriz_custo, TAMANHO, max_execucoes=MAX_EXECUCOES_FB
    )
    tempo_fb = time.perf_counter() - inicio_fb

    resultados = [
        {
            "nome": "Têmpera Simulada",
            "custo": custo_ts,
            "tempo": tempo_ts,
            "rota": sol_ts,
        },
        {
            "nome": "Algoritmo Genético",
            "custo": custo_ag,
            "tempo": tempo_ag,
            "rota": sol_ag,
        },
        {
            "nome": f"Força Bruta ({total_avaliado} eval)",
            "custo": custo_fb,
            "tempo": tempo_fb,
            "rota": sol_fb,
        },
    ]

    resultados.sort(key=lambda x: x["custo"])
    melhor_custo_global = resultados[0]["custo"]

    print(
        f"{'Algoritmo':<28} | {'Melhor Custo':<12} | {'Tempo (s)':<10} | {'Gap (%)':<8}"
    )
    print("-" * 65)
    for res in resultados:
        gap = ((res["custo"] - melhor_custo_global) / melhor_custo_global) * 100
        print(
            f"{res['nome']:<28} | {res['custo']:<12.2f} | {res['tempo']:<10.4f} | +{gap:<7.2f}%"
        )
    print("-" * 65)

    print("\nDetalhamento das Melhores Rotas Encontradas:")
    for res in resultados:
        print(f"-> {res['nome']}: {res['rota']}")


if __name__ == "__main__":
    comparar_algoritmos()
