from multiprocessing import Pool
import time

def tarefa(x):
    time.sleep(1)
    return x * 10

if __name__ == '__main__':
    with Pool(processes=2) as pool:
        resultados = [pool.apply_async(tarefa, args=(i,)) for i in range(4)]
        print("Tarefas submetidas, aguardando resultados...")
        saidas = [r.get() for r in resultados]
        # chamada r.get() bloqueia até que o resultado esteja disponível,
        # o que permite processar os resultados de forma controlada
    print(saidas)  # [0, 10, 20, 30]