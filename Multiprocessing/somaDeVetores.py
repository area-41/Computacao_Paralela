# Soma de Vetores
# Vetor_A = [1,2,3]
# Vetor_B = [3,3,3]
# Vetor_C = [4, 5, 6]

# def soma_vetores(A, B):
#     C = []

#     for i in range(0, len(A)):
#         C.append(A[i] + B[i])

#     return C

# if __name__ == '__main__':
#     A = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#     B = [9, 8, 7, 6, 5, 4, 3, 2, 1]

#     R = soma_vetores(A, B)

#     print(f"Resultado: {R}")

import threading


def soma_parte(A, B, R, inicio, fim):
    print(f"Inicinado a thread: {threading.current_thread().getName}")
    for i in range(inicio, fim):
        R[i] = A[i] + B[i]
    print(f"Finalizando a thread: {threading.current_thread().getName}")


def soma_vetores_thread(A, B, num_threads):
    if len(A) != len(B):
        print("Vetores de tamanho diferentes!")
        return []

    C = [0] * len(A)  # [0, 0, 0, ... n]

    # Divisão da carga de trabalho
    threads = []
    tamanho_parte = len(C) // num_threads  # 9 // 4 = 2

    for i in range(num_threads):
        inicio = i * tamanho_parte  # Thread 0: 0 * 2 = 0 | Thread 1: 1 * 2 = 2 | Thread 2: 2*2 = 4 | Thread 3: 3*2 = 6
        fim = (i + 1) * tamanho_parte if i != num_threads - 1 else len(
            C)  # Thread 0: 1 * 2 = 2 | Thread 1: 2 * 2 = 4 | Thread 2: 3*2 = 6 | Thread 3: 4*2 = 9

        thread = threading.Thread(target=soma_parte, args=(A, B, C, inicio, fim))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return C


if __name__ == '__main__':
    A = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40]
    B = [9, 8, 7, 6, 5, 4, 3, 2, 1, 5, 5, 5, 5]

    R = soma_vetores_thread(A, B, 4)

    print(f"Resultado: {R}")