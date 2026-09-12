import statistics
import time

import matplotlib.pyplot as plt

from core.genetico import AG
from core.tempura_simulada.tempera_simulada import executar_tempera_simulada
from core.uteis.uteis import gerar_matriz_custo_aleatoria


def executar_analise_parametros():
    TAMANHO = 100
    REPETICOES = 3
    matriz_custo = gerar_matriz_custo_aleatoria(TAMANHO)

    print(f"=== ANÁLISE DE SENSIBILIDADE DE PARÂMETROS (N = {TAMANHO}) ===\n")

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # ------------------------------------------------------------------
    # 1. AG: Efeito da Taxa de Mutação
    # ------------------------------------------------------------------
    taxas_mutacao = [
        1 / (100 * TAMANHO),
        1 / (10 * TAMANHO),
        1 / TAMANHO,
        2 / TAMANHO,
    ]
    labels_mut = ["1/(100N)", "1/(10N)", "1/N", "2/N"]
    custos_mut, tempos_mut = [], []

    for tm in taxas_mutacao:
        c_list, t_list = [], []
        for _ in range(REPETICOES):
            t0 = time.perf_counter()
            ag = AG(
                n_cidades=TAMANHO,
                matriz_custo=matriz_custo,
                pressao_fitness=3.0,
                taxa_crossover=0.85,
                max_execucoes=500,
                chance_mutacao=tm,
            )
            c, _ = ag.executar()
            tf = time.perf_counter()
            c_list.append(c)
            t_list.append(tf - t0)
        custos_mut.append(statistics.mean(c_list))
        tempos_mut.append(statistics.mean(t_list))

    axes[0].plot(labels_mut, custos_mut, marker="o", color="blue", linewidth=2)
    axes[0].set_title("AG: Impacto da Taxa de Mutação")
    axes[0].set_xlabel("Taxa de Mutação (Chance por Gene)")
    axes[0].set_ylabel("Custo Médio de Rota")
    axes[0].grid(True, linestyle="--", alpha=0.6)

    # ------------------------------------------------------------------
    # 2. AG: Efeito da Pressão de Fitness
    # ------------------------------------------------------------------
    pressoes = [0.5, 1.5, 3.5, 6.0]
    custos_press, tempos_press = [], []

    for pf in pressoes:
        c_list, t_list = [], []
        for _ in range(REPETICOES):
            t0 = time.perf_counter()
            ag = AG(
                n_cidades=TAMANHO,
                matriz_custo=matriz_custo,
                pressao_fitness=pf,
                taxa_crossover=0.85,
                max_execucoes=500,
                chance_mutacao=1 / TAMANHO,
            )
            c, _ = ag.executar()
            tf = time.perf_counter()
            c_list.append(c)
            t_list.append(tf - t0)
        custos_press.append(statistics.mean(c_list))
        tempos_press.append(statistics.mean(t_list))

    axes[1].plot(pressoes, custos_press, marker="s", color="green", linewidth=2)
    axes[1].set_title("AG: Impacto da Pressão de Fitness")
    axes[1].set_xlabel("Pressão de Fitness")
    axes[1].set_ylabel("Custo Médio de Rota")
    axes[1].grid(True, linestyle="--", alpha=0.6)

    # ------------------------------------------------------------------
    # 3. TS: Efeito do Decaimento Térmico vs. Custo e Tempo
    # ------------------------------------------------------------------
    decaimentos = [0.90, 0.95, 0.98, 0.999]
    custos_ts, tempos_ts = [], []

    for dec in decaimentos:
        c_list, t_list = [], []
        for _ in range(REPETICOES):
            t0 = time.perf_counter()
            _, melhor_custo, _, _, _ = executar_tempera_simulada(
                matriz_custo=matriz_custo,
                tamanho=TAMANHO,
                constante_resfriamento=dec,
                aceitacao=0.90,
                temp_minima=0.001,
                estabilidade_termica=1,
            )
            tf = time.perf_counter()
            c_list.append(melhor_custo)
            t_list.append(tf - t0)
        custos_ts.append(statistics.mean(c_list))
        tempos_ts.append(statistics.mean(t_list))

    ax3_twin = axes[2].twinx()
    axes[2].plot(
        decaimentos,
        custos_ts,
        marker="^",
        color="red",
        linewidth=2,
        label="Custo",
    )
    ax3_twin.plot(
        decaimentos,
        tempos_ts,
        marker="d",
        color="orange",
        linewidth=2,
        linestyle="--",
        label="Tempo",
    )

    axes[2].set_title("TS: Decaimento vs. Custo e Tempo")
    axes[2].set_xlabel("Fator de Decaimento (α)")
    axes[2].set_ylabel("Custo Médio de Rota", color="red")
    ax3_twin.set_ylabel("Tempo Médio (s)", color="orange")
    axes[2].grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.show()

    # ------------------------------------------------------------------
    # Relatório no Console
    # ------------------------------------------------------------------
    print(f"{'Experimento':<25} | {'Melhor Config':<20} | {'Menor Custo':<12}")
    print("-" * 62)
    print(
        f"{'AG - Mutação':<25} | {labels_mut[custos_mut.index(min(custos_mut))]:<20} | {min(custos_mut):<12.2f}"
    )
    print(
        f"{'AG - Pressão':<25} | {pressoes[custos_press.index(min(custos_press))]:<20.1f} | {min(custos_press):<12.2f}"
    )
    print(
        f"{'TS - Decaimento':<25} | {decaimentos[custos_ts.index(min(custos_ts))]:<20.3f} | {min(custos_ts):<12.2f}"
    )


if __name__ == "__main__":
    executar_analise_parametros()
