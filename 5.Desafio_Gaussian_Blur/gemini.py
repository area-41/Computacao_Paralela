import os
import concurrent.futures
from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np

# Configurações de diretório e filtro
PASTA_ORIGEM = Path("imagens")
PASTA_DESTINO = Path("convertidas")
PASTA_FOCO = Path("desconvertidas")  # Nova pasta para os testes de foco
RAIO_BLUR = 15


def aplicar_gaussian_blur(caminho_imagem: Path) -> str:
    """
    Função executada por cada processo.
    Aplica o filtro Gaussian Blur e salva a imagem na pasta de destino.
    """
    try:
        caminho_saida = PASTA_DESTINO / caminho_imagem.name

        with Image.open(caminho_imagem) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Aqui aplica-se o desfoque original
            img_filtrada = img.filter(ImageFilter.GaussianBlur(radius=RAIO_BLUR))
            img_filtrada.save(caminho_saida, quality=95)

        return f"[SUCESSO] Processada: {caminho_imagem.name} -> {caminho_saida}"

    except Exception as e:
        return f"[ERRO] Falha ao processar {caminho_imagem.name}: {str(e)}"


def main():
    # 1. Garante que as pastas de destino existam
    PASTA_DESTINO.mkdir(parents=True, exist_ok=True)
    PASTA_FOCO.mkdir(parents=True, exist_ok=True)

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

    print(f"Iniciando o processamento paralelo de {total_imagens} imagens...")
    print("-" * 50)

    # 4. Processamento paralelo utilizando um Pool de Processos
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futuros = [executor.submit(aplicar_gaussian_blur, img) for img in imagens]

        for i, futuro in enumerate(concurrent.futures.as_completed(futuros), 1):
            resultado = futuro.result()
            print(f"[{i}/{total_imagens}] {resultado}")

    print("-" * 50)
    print("Processamento de desfoque concluído!")
    print("-" * 50)

    # 5. Demonstração dos métodos de Foco com foco TOTAL na Deconvolução

    # Importações do scikit-image necessárias (certifique-se de instalá-las)
    from skimage import io, color, restoration, img_as_ubyte

    # Pega dinamicamente a primeira imagem que foi salva na pasta de convertidas
    imagens_convertidas = list(PASTA_DESTINO.iterdir())
    if not imagens_convertidas:
        print("Nenhuma imagem convertida disponível para o teste de foco.")
        return

    imagem_teste = imagens_convertidas[0]
    print(f"Iniciando métodos de recuperação de foco na imagem: {imagem_teste.name}")

    # --- Método C: Deconvolução de Richardson-Lucy (Único método que pode reverter) ---
    try:
        # Carrega a imagem desconvertida (com o desfoque raio 15) em escala de cinza
        img_gray = color.rgb2gray(io.imread(str(imagem_teste)))

        # PSF (Point Spread Function) - Kernel 15x15 para simular o raio 15 original
        # É crucial que este kernel seja bem estimado
        psf = np.ones((15, 15)) / 225

        # Executa a deconvolução (retorna um array float de 0.0 a 1.0)
        # O Richardson-Lucy tenta reconstruir o objeto original minimizando a chance de ruído
        print("[PROCESSANDO] Deconvolução de Richardson-Lucy... isso pode demorar.")
        array_deconv = restoration.richardson_lucy(img_gray, psf, num_iter=30)

        # Converte o array float de volta para uma imagem uint8 (0-255) do Pillow para poder salvar
        img_reconstruida = Image.fromarray(img_as_ubyte(array_deconv))
        caminho_reconstruido = PASTA_FOCO / f"RECONSTRUCAO_{imagem_teste.stem}.webp"
        img_reconstruida.save(caminho_reconstruido)
        print(f"[SUCESSO] Imagem reconstruída salva em: {caminho_reconstruido}")

    except Exception as e:
        print(f"[ERRO] Falha no método de deconvolução: {e}")


if __name__ == "__main__":
    # Proteção para o Windows/macOS
    main()