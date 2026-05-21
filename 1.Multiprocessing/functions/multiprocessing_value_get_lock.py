from multiprocessing import Process, Value

def incrementa(contador):
    print(f"Processo: {contador.value}")
    for _ in range(10):
        with contador.get_lock():  # Garantir que o acesso ao valor seja seguro
            contador.value = contador.value + 1
            print(contador.value)

if __name__ == "__main__":
    contador = Value('i', 0)  # 'i' indica um inteiro

    processos = []
    p1 = Process(target=incrementa, args=(contador,))
    p2 = Process(target=incrementa, args=(contador,))
    p3 = Process(target=incrementa, args=(contador,))


    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()