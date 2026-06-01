from multiprocessing import Process, Array

def dobra(valores2):
    for i in range(len(valores2)):
        valores2[i] = valores2[i] * 2
    print(valores2[:])

def triplica(valores3):
    for i in range(len(valores3)):
        valores3[i] = valores3[i] * 3
    print(valores3[:])

def quadriplica(valores4):
    for i in range(len(valores4)):
        valores4[i] = valores4[i] * 4
    print(valores4[:])

if __name__ == "__main__":
    vetor = Array('i', [1, 2, 3, 4,])

    p0 = Process(target=quadriplica, args=(vetor,))
    p1 = Process(target=dobra, args=(vetor,))
    p2 = Process(target=triplica, args=(vetor,))

    p0.start()
    p1.start()
    p2.start()

    p0.join()
    print(f"Terminou o processo 00: {p0.name}\n"
          f"Lista de vetores do Array neste momento: {list(vetor)}\n")

    p1.join()  # trava e só avança se p1 terminar
    print(f"Terminou o processo 01: {p1.name}\n"
          f"Lista de vetores do Array neste momento: {list(vetor)}\n")

    p2.join()
    print(f"Terminou o processo 02: {p2.name}\n"
          f"Lista de vetores do Array neste momento: {list(vetor)}\n")

