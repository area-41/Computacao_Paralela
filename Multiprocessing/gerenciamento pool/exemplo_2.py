from multiprocessing import Pool
import numpy as np


# Função que soma duas partes do vetor
def soma_parcial(vetor1, vetor2, inicio, fim):
    return np.sum(vetor1[inicio:fim] + vetor2[inicio:fim])


if __name__ == '__main__':
    # Tamanho dos vetores e número de processos
    tamanho_vetor = 10 ** 6  # 1 milhão de elementos
    num_processos = 4  # Número de processos no pool

    # Criando dois vetores grandes aleatórios
    vetor1 = np.random.randint(0, 100, tamanho_vetor)
    vetor2 = np.random.randint(0, 100, tamanho_vetor)

    # Calculando o tamanho de cada fragmento que será processado por cada processo
    fragmento_size = tamanho_vetor // num_processos
    tarefas = [(vetor1, vetor2, i * fragmento_size, (i + 1) * fragmento_size) for i in range(num_processos)]

    # Criando o pool de processos
    with Pool(processes=num_processos) as pool:
        # Usando starmap para distribuir as tarefas de soma
        resultados_parciais = pool.starmap(soma_parcial, tarefas)

    # Soma final de todos os resultados parciais
    soma_total = sum(resultados_parciais)

    # Exibindo a soma total
    print(f"Soma total dos vetores: {soma_total}")