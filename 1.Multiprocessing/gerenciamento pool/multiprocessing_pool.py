from multiprocessing import Pool
import time


def tarefa(x):
    time.sleep(1)
    return x * 10


if __name__ == '__main__':
    with Pool(processes=2) as pool:
        resultados = [pool.apply_async(tarefa, args=(i,)) for i in range(10)]
        print("Tarefas submetidas aos processos. Vou aguadar o término da execução...")
        saidas = [r.get() for r in resultados]  # r.get bloqueia até finalizar as tarefas

    print(saidas)
