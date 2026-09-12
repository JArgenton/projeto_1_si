import pandas as pd
import matplotlib.pyplot as plt

def analisar_e_plotar_resultados(caminho_csv: str = "resultados_sa_cidades50.csv"):
    """
    Lê o CSV de resultados da Têmpera Simulada, agrupa as repetições por média e 
    desvio padrão, e gera gráficos de sensibilidade paramétrica para Custo e Tempo.
    """
    # Carrega os dados gerados nos experimentos
    df = pd.read_csv(caminho_csv)
    
    # Identifica quais parâmetros foram testados isoladamente
    parametros_unicos = df['parametro_testado'].unique()
    n_params = len(parametros_unicos)
    
    # Configura a grade de subplots (N parâmetros x 2 colunas: Custo e Tempo)
    fig, axes = plt.subplots(n_params, 2, figsize=(14, 4 * n_params))
    fig.suptitle("Análise de Sensibilidade Paramétrica - Simulated Annealing (PCV 50 Cidades)", fontsize=14, fontweight='bold')
    
    # Ajuste para garantir bidimensionalidade da matriz de eixos
    if n_params == 1:
        axes = [axes]

    for idx, param in enumerate(parametros_unicos):
        df_param = df[df['parametro_testado'] == param]
        
        # Agrupa repetições estocásticas calculando Média e Desvio Padrão
        agrupado = df_param.groupby('valor_parametro').agg(
            custo_medio=('melhor_custo', 'mean'),
            custo_std=('melhor_custo', 'std'),
            tempo_medio=('tempo_execucao_seg', 'mean'),
            tempo_std=('tempo_execucao_seg', 'std')
        ).reset_index()
        
        ax_custo = axes[idx][0]
        ax_tempo = axes[idx][1]
        
        # Usar escala logarítmica no eixo X para a Temperatura Mínima
        usar_escala_log = True if param == 'temp_minima' else False
        
        # --- Gráfico 1: Valor do Parâmetro vs. Melhor Custo ---
        ax_custo.plot(agrupado['valor_parametro'], agrupado['custo_medio'], marker='o', color='tab:blue', linewidth=2, label='Custo Médio')
        ax_custo.fill_between(
            agrupado['valor_parametro'], 
            agrupado['custo_medio'] - agrupado['custo_std'].fillna(0), 
            agrupado['custo_medio'] + agrupado['custo_std'].fillna(0), 
            color='tab:blue', alpha=0.2, label='Desvio Padrão'
        )
        ax_custo.set_title(f"Impacto de '{param}' no Custo da Rota")
        ax_custo.set_xlabel(param)
        ax_custo.set_ylabel("Custo Total (Distância)")
        ax_custo.grid(True, linestyle='--', alpha=0.6)
        ax_custo.legend(loc='best')
        if usar_escala_log:
            ax_custo.set_xscale('log')
            
        # --- Gráfico 2: Valor do Parâmetro vs. Tempo de Execução ---
        ax_tempo.plot(agrupado['valor_parametro'], agrupado['tempo_medio'], marker='s', color='tab:red', linewidth=2, label='Tempo Médio')
        ax_tempo.fill_between(
            agrupado['valor_parametro'], 
            agrupado['tempo_medio'] - agrupado['tempo_std'].fillna(0), 
            agrupado['tempo_medio'] + agrupado['tempo_std'].fillna(0), 
            color='tab:red', alpha=0.2, label='Desvio Padrão'
        )
        ax_tempo.set_title(f"Impacto de '{param}' no Tempo de Execução")
        ax_tempo.set_xlabel(param)
        ax_tempo.set_ylabel("Tempo Execução (s)")
        ax_tempo.grid(True, linestyle='--', alpha=0.6)
        ax_tempo.legend(loc='best')
        if usar_escala_log:
            ax_tempo.set_xscale('log')

    plt.tight_layout()
    plt.subplots_adjust(top=0.93)
    
    plt.savefig("grafico_sensibilidade_sa.png", dpi=300)
    plt.show()

if __name__ == '__main__':
    analisar_e_plotar_resultados("resultados_sa_cidades50.csv")