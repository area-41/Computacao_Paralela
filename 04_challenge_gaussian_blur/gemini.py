import sys
import subprocess

# 1. GARANTE AS DEPENDÊNCIAS NO AMBIENTE VIRTUAL
try:
    import PIL
    import skimage
except ImportError:
    print("[AVISO] Dependências não encontradas no ambiente virtual. Instalando...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", 
        "Pillow", "scikit-image", "scipy", "matplotlib"
    ])
    print("[SUCESSO] Ambiente configurado com sucesso! Iniciando o programa...\n")

# 2. IMPORTAÇÕES GLOBAIS (Obrigatório estarem aqui para os subprocessos lerem)
import os
import concurrent.futures
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
from skimage import io, color, restoration, img_as_ubyte

# Configurações de diretório e filtro
PASTA_ORIGEM = Path("imagens")
PASTA_DESTINO = Path("convertidas")
PASTA_FOCO = Path("desconvertidas")
RAIO_BLUR = 15

def aplicar_gaussian_blur(caminho_imagem: Path) -> str:
    """
    Função executada por cada processo.
    """
    try:
        caminho_saida = PASTA_DESTINO / caminho_imagem.name

        # Agora 'Image' está visível globalmente para este processo
        with Image.open(caminho_imagem) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            img_filtrada = img.filter(ImageFilter.GaussianBlur(radius=RAIO_BLUR))
            img_filtrada.save(caminho_saida, quality=95)

        return f"[SUCESSO] Processada: {caminho_imagem.name} -> {caminho_saida}"

    except Exception as e:
        return f"[ERRO] Falha ao processar {caminho_imagem.name}: {str(e)}"

def main():
    # Garante que as pastas de destino existam
    PASTA_DESTINO.mkdir(parents=True, exist_ok=True)
    PASTA_FOCO.mkdir(parents=True, exist_ok=True)

    extensoes_validas = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".jfif"}

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

    print(f"Iniciando o processamento paralelo de {total_imagens} imagens...")
    print("-" * 50)

    # Processamento paralelo utilizando um Pool de Processos
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futuros = [executor.submit(aplicar_gaussian_blur, img) for img in imagens]

        for i, futuro in enumerate(concurrent.futures.as_completed(futuros), 1):
            resultado = futuro.result()
            print(f"[{i}/{total_imagens}] {resultado}")

    print("-" * 50)
    print("Processamento de desfoque concluído!")
    print("-" * 50)

    # PROCESSAMENTO DE FOCO (DECONVOLUÇÃO)
    imagens_convertidas = list(PASTA_DESTINO.iterdir())
    if not imagens_convertidas:
        print("Nenhuma imagem convertida disponível para o teste de foco.")
        return
    
    imagem_teste = imagens_convertidas[0]
    print(f"Iniciando métodos de recuperação de foco na imagem: {imagem_teste.name}")

    # Substitua a parte do processamento da Deconvolução por esta:
    # Substitua a parte da Deconvolução por esta:
    try:
        from skimage import io, color, restoration, img_as_ubyte
        
        # 1. Carrega a imagem gerada pelo desfoque
        img_gray = color.rgb2gray(io.imread(str(imagem_teste)))

        # 2. PSF (Point Spread Function) - Matriz 15x15
        psf = np.ones((15, 15)) / 225

        print("[PROCESSANDO] Executando Deconvolução de Richardson-Lucy Estabilizada...")
        
        # O parâmetro clip=True impede que flutuações matemáticas estourem os limites dos pixels
        # filter_epsilon ajuda a mitigar o ruído gerado pelas descontinuidades das bordas
        array_deconv = restoration.richardson_lucy(
            img_gray, 
            psf, 
            num_iter=30, 
            clip=True, 
            filter_epsilon=1e-4
        )
        
        # Se mesmo assim as bordas continuarem incomodando, podemos simplesmente recortá-las (crop)
        # removemos uma margem correspondente ao tamanho do raio do desfoque (15 pixels)
        raio = RAIO_BLUR
        array_cortado = array_deconv[raio:-raio, raio:-raio]
        
        # Converte e salva
        img_reconstruida = Image.fromarray(img_as_ubyte(array_cortado))
        caminho_reconstruido = PASTA_FOCO / f"RECONSTRUCAO_CORRIGIDA_{imagem_teste.stem}.webp"
        img_reconstruida.save(caminho_reconstruido)
        print(f"[SUCESSO] Imagem reconstruída salva em: {caminho_reconstruido}")
        
    except Exception as e:
        print(f"[ERRO] Falha no método de deconvolução: {e}")

if __name__ == "__main__":
    main()