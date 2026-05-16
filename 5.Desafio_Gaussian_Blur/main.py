from PIL import Image, ImageFilter

"""
O programa deve:

    Ler todas as imagens .jpg da pasta imagens/.

    Aplicar o filtro Gaussian Blur com raio 15 a cada imagem.

    Salvar a nova imagem na pasta convertidas/, mantendo o mesmo nome de arquivo.

O processamento das imagens deve ser feito em processos separados, um para cada imagem, utilizando o módulo multiprocessing.

    O programa deve:

        Criar a pasta convertidas/ se ela ainda não existir.

        Utilizar a biblioteca Pillow (PIL) para abrir, processar e salvar as imagens.

Exibir mensagens no terminal indicando o progresso da aplicação do filtro.
"""


# Abre a imagem como um objeto do Pillow
imagem = Image.open("imagens/imagem.webp")
#imagem = Image.open("imagens/foto.jpg")

# Aplica um filtro de desfoque
imagem_blur = imagem.filter(ImageFilter.GaussianBlur(radius=15))

# Salva a nova imagem
imagem_blur.save("convertidas/foto_blur.jpg")