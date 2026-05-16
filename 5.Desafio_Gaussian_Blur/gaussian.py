import os
import concurrent.futures
from pathlib import Path
from PIL import Image, ImageFilter

# Configurações de diretório e filtro
PASTA_ORIGEM = Path("imagens")
PASTA_DESTINO = Path("convertidas")
RAIO_BLUR = 15

def aplicar_gaussian_blur(caminho_imagem: Path) -> str:
    """
    Função executada por cada processo. 
    Aplica o filtro Gaussian Blur e salva a imagem na pasta de destino.
    """
    try:
        # Define o caminho de saída mantendo o nome original
        caminho_saida = PASTA_DESTINO / caminho_imagem.name
        
        # Abre, processa e salva a imagem
        with Image.open(caminho_imagem) as img:
            # Garante que a imagem está em modo RGB para evitar problemas com alguns formatos
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
                
            img_filtrada = img.filter(ImageFilter.GaussianBlur(radius=RAIO_BLUR))
            img_filtrada.save(caminho_saida, quality=95)
            
        return f"[SUCESSO] Processada: {caminho_imagem.name} -> {caminho_saida}"
    
    except Exception as e:
        return f"[ERRO] Falha ao processar {caminho_imagem.name}: {str(e)}"

def main():
    # 1. Garante que a pasta de destino exista
    PASTA_DESTINO.mkdir(parents=True, exist_ok=True)
    
    # 2. Extensões de imagem suportadas
    extensoes_validas = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".jfif"}
    
    # 3. Lista todas as imagens da pasta de origem
    if not PASTA_ORIGEM.exists():
        print(f"[ERRO] A pasta de origem '{PASTA_ORIGEM}' não existe.")
        return

    imagens = [
        p for p in PASTA_ORIGEM.iterdir() 
        if p.is_file() and p.suffix.lower() in extensoes_validas
    ]
    
    total_imagens = len(imagens)
    if total_imagens == 0:
        print(f"Nenhuma imagem válida encontrada em '{PASTA_ORIGEM}'.")
        return
        
    print(f"Iniciando o processamento de {total_imagens} imagens...")
    print("-" * 50)

    # 4. Processamento paralelo utilizando um Pool de Processos
    # O ProcessPoolExecutor gerencia os processos separados automaticamente
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Envia todas as tarefas para o pool
        futuros = [executor.submit(aplicar_gaussian_blur, img) for img in imagens]
        
        # Monitora o progresso conforme os processos terminam
        for i, futuro in enumerate(concurrent.futures.as_completed(futuros), 1):
            resultado = futuro.result()
            print(f"[{i}/{total_imagens}] {resultado}")

    print("-" * 50)
    print("Processamento concluído com sucesso!")

if __name__ == "__main__":
    # Proteção necessária para evitar loops infinitos ao criar novos processos no Windows/macOS
    main()