import numpy as np
from numba import cuda, njit
from PIL import Image
import time

Image.MAX_IMAGE_PIXELS = 1000000000

# --- Kernel CUDA para blur ---
@cuda.jit
def blur_gpu(input_img, output_img):
    x, y = cuda.grid(2)
    altura, largura = input_img.shape

    raio = 7


    if x < largura and y < altura:
        soma = 0.0
        contador = 0
        for dy in range(-raio, raio + 1):
            for dx in range(-raio, raio + 1):
                nx = x + dx
                ny = y + dy
                if 0 <= nx < largura and 0 <= ny < altura:
                    soma += input_img[ny, nx]
                    contador += 1
        output_img[y, x] = soma / contador

# --- Função blur CPU ---
def blur_cpu(input_img):
    altura, largura = input_img.shape
    output_img = np.zeros_like(input_img)

    raio = 3
    for y in range(altura):
        for x in range(largura):
            soma = 0.0
            contador = 0
            for dy in range(-raio, raio + 1):
                for dx in range(-raio, raio + 1):
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < largura and 0 <= ny < altura:
                        soma += input_img[ny, nx]
                        contador += 1
            output_img[y, x] = soma / contador
    return output_img

# --- Função principal ---
def aplicar_blur(imagem_path, output_path_gpu, output_path_cpu):
    img = Image.open(imagem_path).convert('L')
    img_np = np.asarray(img)

    # CPU
    start_cpu = time.time()
    output_cpu = blur_cpu(img_np)
    fim_cpu = time.time()
    print(f"Tempo CPU: {fim_cpu - start_cpu:.4f} segundos")

    # GPU
    altura, largura = img_np.shape
    input_device = cuda.to_device(img_np)
    output_device = cuda.device_array_like(img_np)

    threads_por_bloco = (16, 16)
    blocos_x = (largura + threads_por_bloco[0] - 1) // threads_por_bloco[0]
    blocos_y = (altura + threads_por_bloco[1] - 1) // threads_por_bloco[1]
    grid = (blocos_x, blocos_y)

    start_gpu = time.time()
    blur_gpu[grid, threads_por_bloco](input_device, output_device)
    cuda.synchronize()
    fim_gpu = time.time()
    print(f"Tempo GPU: {fim_gpu - start_gpu:.4f} segundos")

    output_gpu = output_device.copy_to_host()

    # Salvar resultados
    Image.fromarray(np.uint8(output_cpu)).save(output_path_cpu)
    Image.fromarray(np.uint8(output_gpu)).save(output_path_gpu)
    print(f"Imagens salvas: GPU -> {output_path_gpu}, CPU -> {output_path_cpu}")

if __name__ == "__main__":
    aplicar_blur("sua_imagem.jpg", "imagem_blur_gpu.jpg", "imagem_blur_cpu.jpg")