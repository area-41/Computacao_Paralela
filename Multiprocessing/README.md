# Python Parallel Computing: Multiprocessing, IPC & Shared Memory

Esta pasta do repositório reúne implementações práticas focadas em **Computação Paralela** utilizando a biblioteca `multiprocessing` do Python. O objetivo principal é explorar como superar o *Global Interpreter Lock (GIL)*, criando processos independentes que executam tarefas simultaneamente e se comunicam de forma eficiente.

### Conceitos e Aprendizados

### 1. Memória Compartilhada (`Value` e `Array`)
Em sistemas paralelos, processos não compartilham o mesmo espaço de memória por padrão. Para permitir que processos colaborem nos mesmos dados, utilizei objetos de memória compartilhada:
*   **`Value`**: Utilizado para compartilhar um valor único (ex: um contador inteiro) entre múltiplos processos.
*   **`Array`**: Permite o compartilhamento de vetores de dados de tamanho fixo.
*   **Sincronização (`Lock`)**: Implementação do uso de `get_lock()` para evitar **Condições de Corrida** (*Race Conditions*), garantindo que apenas um processo altere o dado por vez.

### 2. Comunicação Interprocesso (IPC)
Diferentes estratégias para troca de informações entre processos:

#### **Pipes**
Implementação de comunicação **bidirecional** direta (ponta-a-ponta). 
*   Utilizado para criar um fluxo de mensagem entre um processo pai e um processo filho.
*   Demonstração de como enviar strings, processá-las em um processo isolado e retornar o resultado.

#### **Queues (Filas)**
Implementação de uma estrutura de dados **Thread-safe e Process-safe**.
*   Utilizada no modelo clássico **Produtor-Consumidor**.
*   A fila gerencia o fluxo de trabalho, permitindo que processos em velocidades diferentes (ex: produtor rápido e consumidor lento) operem sem perda de dados.

### 3. Gerenciamento de Ciclo de Vida e Sincronização
*   **`Process.start()` e `Process.join()`**: Controle fino sobre a criação e a espera pelo término da execução de cada processo, garantindo que o programa principal não finalize antes das tarefas paralelas.
*   **`Event`**: Uso de sinalizadores (*flags*) de sincronização para comunicar estados entre processos (como o sinal de interrupção/parada do sistema).

---

## Tecnologias Utilizadas
*   **Python 3.x**
*   **Multiprocessing Library**: Para paralelismo real baseado em processos (CPU-bound tasks).

## Estrutura do Repositório

| Arquivo | Descrição | Conceito Chave |
| :--- | :--- | :--- |
| `GetLock.py` | Incremento de contador entre 3 processos. | `Value` + `Lock` |
| `MultiprocessingArray.py` | Transformações matemáticas em um vetor compartilhado. | `Array` |
| `Pipe.py` | Inversor de frases via canal de comunicação. | `Pipe` (Send/Recv) |
| `Queue.py` | Sistema de fila com produtor e consumidor randômicos. | `Queue` + `Event` |


## Conclusão
O estudo desses scripts permitiu a compreensão de que a computação paralela em Python vai além da simples execução simultânea.
Ela exige um design cuidadoso sobre como os dados trafegam entre processos (podendo gerar resultados diferentes em razão 
da ordem que foram executados) e como evitar gargalos de sincronização para garantir a integridade da informação.

---
*Este repositório faz parte dos meus estudos em Python Avançado e Engenharia de Dados.*