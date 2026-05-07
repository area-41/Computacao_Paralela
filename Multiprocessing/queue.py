# Produtor e Consumidor
"""
Produtor gera mais rapidamente que o consumidor consome para que seja formada uma fila
ex.:
Produtor gerou: 53
Consumiu: 31
Fila: [53]
"""

from multiprocessing import Process, Queue, Event
import random
import time


def listar_fila(queue):
    itens = []
    while not queue.empty():
        try:
            item = queue.get_nowait()
            itens.append(item)
        except:
            break
    for item in itens:
        queue.put(item)

    return itens


def prod(queue, stop_event):
    while not stop_event.is_set():
        item = random.randint(1, 100)
        queue.put(item)
        print(f"Produtor gerou: {item}")
        time.sleep(random.randint(1, 10) / 10)
        print(f"Fila: {listar_fila(queue)}")


def consu(queue, stop_event):
    while not stop_event.is_set():
        try:
            item = queue.get(timeout=1)
            print(f"Consumiu: {item}")
        except:
            print("A fila estava vazia.")
        time.sleep(random.randint(1, 15) / 10)


if __name__ == '__main__':

    fila = Queue()
    stop_event = Event()

    produtor = Process(target=prod, args=(fila, stop_event))
    consumidor = Process(target=consu, args=(fila, stop_event))

    produtor.start()
    consumidor.start()

    print("Digite 'sair' para encerrar.")

    while True:
        comando = input()
        if comando.strip().lower() == "sair":
            stop_event.set()
            break

    produtor.start()
    consumidor.start()

    produtor.join()
    consumidor.join()
