from multiprocessing import Pool

def quadrado(x):
    return x*x

if __name__ == '__main__':

    valores = list(range(10000))

    with Pool(processes=6) as pool:
        resultados = pool.map(quadrado, valores)

    print(f"Lista dos quadrados dos elementos:\n{resultados}\n"
          f"Quantidade de elementos: {len(resultados)}")