from multiprocessing import Process, Pipe

def envia(canal_B):
    """
    Recebe a mensagem, quebra e devolve as palavras na ordem inversa na frase.
    :param canal_B: msg
    :return: frase invertida
    """
    while True:
        msg = canal_B.recv()
        if msg.lower() == "sair":
            print("Processo B: encerrando...")
            break
        print(f"Processo B recebeu a mensagem: {msg}")
        msg = msg.split()
        resposta = " ".join(msg[::-1]).lower()
        canal_B.send(resposta)

if __name__ == "__main__":
    ponta_A, ponta_B = Pipe()

    filho = Process(target=envia, args=(ponta_B,))
    filho.start()

    print("Digite 'sair' caso queira encerrar. Senão, digite uma mensagem para enviar.")

    while True:
        msg = input("Você: ")
        ponta_A.send(msg)
        if msg.lower() == "sair":
            break

        resposta=ponta_A.recv()
        print(f"Resposta do processo filho: {resposta}")


    filho.join()