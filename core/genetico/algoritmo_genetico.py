import copy
import math
import random

from ..uteis.uteis import swap


class AG:
    def __init__(
        self,
        n_cidades,
        matriz_custo,
        pressao_fitness,
        taxa_crossover,
        max_execucoes,
        chance_mutacao,
    ):
        self.matriz_custo = matriz_custo
        self.n_cidades = n_cidades
        self.pressao_fitness = pressao_fitness
        self.taxa_crossover = taxa_crossover
        self.max_execucoes = max_execucoes
        self.chance_mutacao = chance_mutacao

        self.best = math.inf
        self.best_gen = None

    def populate(self):
        self.n_individuos = max(int(self.n_cidades * 5), 50)
        cidades_restantes = list(range(1, self.n_cidades))
        self.individuos = [
            [0] + random.sample(cidades_restantes, len(cidades_restantes))
            for _ in range(self.n_individuos)
        ]

    def sortear_candidatos(self, individuos: list, fitnesses: list) -> list:
        melhor_adaptado = min(fitnesses)
        pior_adaptado = max(fitnesses)

        if melhor_adaptado == pior_adaptado:
            return random.choices(individuos, k=self.n_individuos)

        pesos = []
        for fit in fitnesses:
            normalizacao = (fit - melhor_adaptado) / (pior_adaptado - melhor_adaptado)
            pesos.append(math.exp(-self.pressao_fitness * normalizacao))

        return random.choices(individuos, weights=pesos, k=self.n_individuos)

    def _selecionar_casais(self, candidatos: list) -> list[tuple]:
        pais = candidatos.copy()
        random.shuffle(pais)

        casais = []
        while len(pais) >= 2:
            pai1 = pais.pop(0)

            idx_pai2 = -1
            for idx, candidato in enumerate(pais):
                if candidato != pai1:
                    idx_pai2 = idx
                    break
            if idx_pai2 != -1:
                pai2 = pais.pop(idx_pai2)
            else:
                pai2 = pais.pop(0)

            casais.append((pai1, pai2))

        return casais

    def reproduzir_elitista(self) -> None:
        fitnesses = [self.funcao_fitness(elem) for elem in self.individuos]
        self._separar_melhor(fitnesses)

        n_pop = len(self.individuos)
        self.n_elite = max(int(n_pop * 0.10), 1)

        indices_ordenados = sorted(range(n_pop), key=lambda i: fitnesses[i])

        novos_individuos = [
            self.individuos[i].copy() for i in indices_ordenados[: self.n_elite]
        ]

        candidatos = self.sortear_candidatos(self.individuos, fitnesses)
        casais = self._selecionar_casais(candidatos)

        for casal in casais:
            if len(novos_individuos) >= n_pop:
                break

            ind1, ind2 = self.crossover(casal)
            novos_individuos.append(ind1)

            if len(novos_individuos) < n_pop:
                novos_individuos.append(ind2)

        self.individuos = novos_individuos

    def crossover(self, casal: tuple[list, list]) -> tuple[list, list]:
        pai1, pai2 = casal[0], casal[1]

        if random.random() > self.taxa_crossover:
            return pai1.copy(), pai2.copy()

        cidade_inicial = pai1[0]

        # Isola os genes permutáveis omitindo apenas o índice 0
        p1_inter = pai1[1:]
        p2_inter = pai2[1:]
        tamanho = len(p1_inter)
        d1, d2 = sorted(random.sample(range(tamanho + 1), 2))

        def _gerar_filho(p_doador: list, p_receptor: list) -> list:
            filho = [None] * tamanho
            filho[d1:d2] = p_doador[d1:d2]

            pos = d2 % tamanho
            ordem_receptor = p_receptor[d2:] + p_receptor[:d2]

            for gene in ordem_receptor:
                if gene not in filho:
                    filho[pos] = gene
                    pos = (pos + 1) % tamanho

            return [cidade_inicial] + filho

        filho1 = _gerar_filho(p1_inter, p2_inter)
        filho2 = _gerar_filho(p2_inter, p1_inter)

        return filho1, filho2

    def funcao_fitness(self, individuo: list):
        custo = 0
        n = len(individuo)
        for i in range(n):
            u = individuo[i]
            v = individuo[(i + 1) % n]
            custo += self.matriz_custo[u][v]
        return custo

    def _separar_melhor(self, fitnesses):
        for i, fit in enumerate(fitnesses):
            if fit < self.best:
                self.best = fit
                self.best_gen = copy.deepcopy(self.individuos[i])

    def mutate(self):
        inicio_mutacao = getattr(self, "n_elite", 0)

        for idx in range(inicio_mutacao, len(self.individuos)):
            individuo = self.individuos[idx]

            for i in range(1, self.n_cidades):
                if random.random() < self.chance_mutacao:
                    pos_swap = i
                    while pos_swap == i:
                        pos_swap = random.randint(1, self.n_cidades - 1)
                    individuo = swap(individuo, i, pos_swap)

            self.individuos[idx] = individuo

    def reproduzir(self) -> list:
        fitnesses = [self.funcao_fitness(elem) for elem in self.individuos]
        self._separar_melhor(fitnesses)
        candidatos = self.sortear_candidatos(self.individuos, fitnesses)
        casais = self._selecionar_casais(candidatos)
        novos_individuos = []
        for casal in casais:
            ind1, ind2 = self.crossover(casal)
            novos_individuos.append(ind1)
            novos_individuos.append(ind2)

        self.individuos = novos_individuos

    def executar(self):
        self.populate()
        for _ in range(self.max_execucoes):
            self.reproduzir_elitista()
            # self.reproduzir()
            self.mutate()
        return self.best, self.best_gen
