from multiprocessing import Process
import time


def trabalho_longo(tempo):
    time.sleep(tempo)


def rodar_processo():
    tempo = int(input("Quantos segundos deseja em cada processo? (ex.: 3): "))
    p = Process(target=trabalho_longo(tempo))
    print("Ligando processo..."), p.start()
    print("Processo vivo?", p.is_alive())
    print("Finalizando processo..."), p.join()
    print("Processo vivo?", p.is_alive())


if __name__ == '__main__':

    rodar_processo()
