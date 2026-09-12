import csv
import time
from core.tempura_simulada.tempera_simulada import executar_tempera_simulada, gerar_matriz_custo_aleatoria

def gerar_valores_variados(valor_base: float, delta: float, min_limite: float, max_limite: float, n_passos: int = 10) -> list:
    valores = []
    for i in range(n_passos, 0, -1):
        v = valor_base - (i * delta)
        if v >= min_limite:
            valores.append(round(v, 6))
            
    valores.append(valor_base)
    
    for i in range(1, n_passos + 1):
        v = valor_base + (i * delta)
        if v <= max_limite:
            valores.append(round(v, 6))
            
    return sorted(list(set(valores)))


def rodar_experimentos_individuais(
    nome_arquivo_csv: str = "experimentos_sa_tsp.csv",
    tamanho_grafo: int = 50,
    n_repeticoes: int = 5
):
    matriz_custo = gerar_matriz_custo_aleatoria(tamanho_grafo)
    
    # Valores base (controlados) para os testes isolados
    base_aceitacao = 0.85
    base_decaimento = 0.95
    base_temp_min = 0.001
    base_estabilidade = 5  # Fator base intermediario para estabilidade termica

    faixas = {
        'aceitacao': gerar_valores_variados(base_aceitacao, delta=0.03, min_limite=0.50, max_limite=0.98),
        'decaimento': gerar_valores_variados(base_decaimento, delta=0.01, min_limite=0.75, max_limite=0.999),
        'temp_minima': [0.0001 * (2**i) for i in range(0, 15)],
        'estabilidade_termica': list(range(1, 11))  # Variacao inteira de 1 a 10
    }

    cabecalho = [
        "parametro_testado", "valor_parametro", "repeticao",
        "aceitacao", "decaimento", "temp_minima", "estabilidade_termica",
        "melhor_custo", "tempo_execucao_seg"
    ]

    with open(nome_arquivo_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(cabecalho)

        # 1. Testando Taxa de Aceitação Inicial
        for val in faixas['aceitacao']:
            executar_e_gravar_bloco(
                writer, file, "aceitacao", val,
                matriz_custo, tamanho_grafo,
                decaimento=base_decaimento, aceitacao=val, temp_min=base_temp_min,
                estabilidade=base_estabilidade, n_repeticoes=n_repeticoes
            )

        # 2. Testando Constante de Resfriamento (Decaimento)
        for val in faixas['decaimento']:
            executar_e_gravar_bloco(
                writer, file, "decaimento", val,
                matriz_custo, tamanho_grafo,
                decaimento=val, aceitacao=base_aceitacao, temp_min=base_temp_min,
                estabilidade=base_estabilidade, n_repeticoes=n_repeticoes
            )

        # 3. Testando Temperatura Mínima
        for val in faixas['temp_minima']:
            executar_e_gravar_bloco(
                writer, file, "temp_minima", val,
                matriz_custo, tamanho_grafo,
                decaimento=base_decaimento, aceitacao=base_aceitacao, temp_min=val,
                estabilidade=base_estabilidade, n_repeticoes=n_repeticoes
            )

        # 4. Testando Estabilidade Térmica (Tamanho do Patamar)
        for val in faixas['estabilidade_termica']:
            executar_e_gravar_bloco(
                writer, file, "estabilidade_termica", val,
                matriz_custo, tamanho_grafo,
                decaimento=base_decaimento, aceitacao=base_aceitacao, temp_min=base_temp_min,
                estabilidade=val, n_repeticoes=n_repeticoes
            )

    print(f"Experimentos concluídos! Dados gravados em '{nome_arquivo_csv}'.")


def executar_e_gravar_bloco(
    writer, file, nome_param, valor_param, matriz, tamanho, 
    decaimento, aceitacao, temp_min, estabilidade, n_repeticoes
):
    for rep in range(1, n_repeticoes + 1):
        inicio = time.time()
        
        sol, melhor_custo, _, _ = executar_tempera_simulada(
            matriz_custo=matriz,
            tamanho=tamanho,
            constante_resfriamento=decaimento,
            aceitacao=aceitacao,
            temp_minima=temp_min,
            estabilidade_termica=estabilidade
        )
        
        fim = time.time()
        tempo_total = round(fim - inicio, 4)

        writer.writerow([
            nome_param, valor_param, rep,
            aceitacao, decaimento, temp_min, estabilidade,
            melhor_custo, tempo_total
        ])
    
    file.flush()


if __name__ == '__main__':
    rodar_experimentos_individuais(
        nome_arquivo_csv="resultados_sa_cidades50.csv",
        tamanho_grafo=50,
        n_repeticoes=3
    )