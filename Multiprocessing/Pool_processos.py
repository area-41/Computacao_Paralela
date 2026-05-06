from multiprocessing import Pool
import numpy as np


def soma_parcial(A, B, idx_inicio, idx_fim):
    return np.sum(A[idx_inicio:idx_fim] + B[idx_inicio:idx_fim])


if __name__ == '__main__':
    tamanho_vetor = 100000
    num_processos = 4

    A = np.random.randint(0, 100, tamanho_vetor)
    B = np.random.randint(0, 100, tamanho_vetor)

    print(f"Vetor A com {len(A)} elementos:\n{A}")
    print(f"Vetor B com {len(B)} elementos:\n{B}")

    fragmento_tam = tamanho_vetor // num_processos

    tarefas = [(A, B, i * fragmento_tam, (i + 1) * fragmento_tam) for i in range(num_processos)]

    with Pool(processes=num_processos) as pool:
        resultados_parciais = pool.starmap(soma_parcial, tarefas)

    print(f"Resultados parciais: {resultados_parciais}")
    soma_total = sum(resultados_parciais)

    print(f"Soma total dos valores é: {soma_total}")