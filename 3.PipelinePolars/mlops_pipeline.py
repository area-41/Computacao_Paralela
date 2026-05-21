# uv init
# uv add polars numpy requests
# uv run mlops_pipeline.py


import polars as pl
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import time
from pathlib import Path

# --- CONFIGURAÇÕES DE MLOPS ---
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FILE_NAME = OUTPUT_DIR / "dataset_imoveis_treinamento.parquet"


def engenharia_de_features(file_id: int) -> pl.DataFrame:
    """
    Simula o processamento pesado de um lote de dados.
    Aqui o Polars brilha com cálculos vetorizados.
    """
    print(f"[Worker {file_id}] Gerando e processando 1 milhão de registros...")

    # Gerando dados sintéticos (Simulando leitura de um CSV/Database)
    df = pl.DataFrame({
        "id_imovel": np.arange(1_000_000),
        "lat": np.random.uniform(-25.5, -25.3, 1_000_000),
        "long": np.random.uniform(-48.6, -48.4, 1_000_000),
        "area_m2": np.random.normal(70, 20, 1_000_000),
    })

    # Fator Crítico: Distância da Praia (Coordenadas de Curitiba/Litoral como exemplo)
    PRAIA_LAT, PRAIA_LONG = -25.4284, -49.2733

    # Otimização Polars: Expressões são executadas em paralelo internamente
    df = df.with_columns([
        (
            ((pl.col("lat") - PRAIA_LAT) ** 2 + (pl.col("long") - PRAIA_LONG) ** 2).sqrt()
        ).alias("distancia_praia"),
        (pl.col("area_m2") * 1500).alias("preco_base_estimado")
    ]).filter(pl.col("area_m2") > 15)  # Limpeza de outliers/erros de medição

    return df


def executar_pipeline():
    # Definimos o número de processos (geralmente igual ao número de núcleos físicos)
    # Para 8 milhões de linhas, usaremos 4 workers
    num_lotes = 8

    print(f"🚀 Iniciando Pipeline com UV e Polars...")
    start_time = time.perf_counter()

    # O ProcessPoolExecutor isola cada tarefa em um processo Python diferente (Adeus GIL)
    with ProcessPoolExecutor(max_workers=4) as executor:
        # Disparamos o processamento paralelo
        resultados = list(executor.map(engenharia_de_features, range(num_lotes)))

    # Concatenação eficiente: Polars une os dataframes sem copiar os dados desnecessariamente
    df_final = pl.concat(resultados)

    duration = time.perf_counter() - start_time

    print("-" * 50)
    print(f"✅ Processamento Concluído!")
    print(f"📊 Total de Registros: {df_final.shape[0]:,}")
    print(f"⏱️ Tempo de Execução: {duration:.2f} segundos")

    # Persistência do modelo treinado/dados processados
    df_final.write_parquet(FILE_NAME)
    print(f"💾 Dataset persistido em: {FILE_NAME}")


if __name__ == "__main__":
    # Importante: No Windows/PyCharm, o uso de if __name__ == "__main__"
    # é obrigatório para evitar recursão infinita ao criar novos processos.
    executar_pipeline()
