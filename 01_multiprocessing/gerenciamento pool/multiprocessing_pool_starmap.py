from multiprocessing import Pool

def potencia(base, expoente, elemento_1, elemento_2):
    return base ** expoente + elemento_1 / elemento_2

if __name__ == '__main__':

    valores = [(2,3,8,2), (5,2,98,4), (4,3,4,6), (2,8,3,6), (2,10,12,3), (3,3,12,12)]

    with Pool(processes=4) as pool:
        resultados = pool.starmap(potencia, valores)

    print(resultados)

