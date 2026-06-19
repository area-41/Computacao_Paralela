import polars as pl
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import time
from pathlib import Path


# --- FUNÇÃO DE PROCESSAMENTO (O que cada worker fará) ---
def processar_dataset_imoveis(file_id):
    """
    Simula o processamento de um dataset pesado de imóveis.
    """
    print(f"Processo {file_id} iniciado...")

    # 1. Simulação de criação/leitura de dados pesados com Polars
    # Criando 1 milhão de linhas por processo
    df = pl.DataFrame({
        "id_imovel": np.arange(1_000_000),
        "lat": np.random.uniform(-25.5, -25.3, 1_000_000),
        "long": np.random.uniform(-48.6, -48.4, 1_000_000),
        "area_m2": np.random.normal(70, 20, 1_000_000),
    })

    # 2. Lógica de Negócio: Cálculo de distância da praia (fator crítico de preço)
    # Coordenada hipotética de uma praia central
    PRAIA_LAT, PRAIA_LONG = -25.4284, -49.2733

    # Engenharia de Recursos usando expressões otimizadas do Polars
    df = df.with_columns([
        (
            ((pl.col("lat") - PRAIA_LAT) ** 2 + (pl.col("long") - PRAIA_LONG) ** 2).sqrt()
        ).alias("distancia_praia"),
        (pl.col("area_m2") * 1500).alias("base_price")  # Valor base fictício
    ])

    # 3. Filtros e Limpeza
    df = df.filter(pl.col("area_m2") > 10)

    print(f"Processo {file_id} concluído.")
    return df


# --- ORQUESTRADOR DO PIPELINE ---
if __name__ == "__main__":
    num_datasets = 8  # Simulando 8 arquivos pesados de dados históricos
    start_time = time.time()

    print(f"Iniciando pré-processamento paralelo de {num_datasets} milhões de registros...")

    # Usando ProcessPoolExecutor para distribuir a carga entre os núcleos da CPU
    with ProcessPoolExecutor(max_workers=4) as executor:
        # Mapeia a função para os IDs dos datasets
        resultados = list(executor.map(processar_dataset_imoveis, range(num_datasets)))

    # Concatenando todos os resultados de volta em um único DataFrame Polars
    # pl.concat é extremamente eficiente para unir DataFrames na memória
    df_final = pl.concat(resultados)

    end_time = time.time()

    # --- RESULTADOS ---
    print("-" * 30)
    print(f"Shape Final do Dataset: {df_final.shape}")
    print(f"Tempo total de processamento: {end_time - start_time:.2f} segundos")

    # Salvando em Parquet (Padrão ouro em MLOps para persistência eficiente)
    df_final.write_parquet("dataset_imoveis_treinamento.parquet")
    print("Dataset persistido em 'dataset_imoveis_treinamento.parquet' para o modelo.")