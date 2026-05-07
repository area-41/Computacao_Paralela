# Computacao_Paralela
## concurrent.futures
O módulo concurrent.futures, introduzido no Python 3.2, fornece uma abstração seguras e práticas
de alto nível para execução concorrente de chamadas assíncronas menos sujeito a problemas de race
conditions ou vazamento de recursos, via executores baseados em threads ou processos.

Criado para simplificar a execução de tarefas de forma concorrente ou paralela
em Python. Executores ThreadPoolExecutor e ProcessPoolExecutor iniciam tarefas com
métodos simples como submit() ou map(), monitoram com Future.result()
e liberam recursos automaticamente usando a instrução with.


Fornece utilitários as_completed() e wait() que facilitam o
controle do ciclo de vida das tarefas — permitindo que o programa trate
os resultados conforme prontos, o que é fundamental em grande volume de tarefas
independentes, útil para aplicações eficientes e responsivas.

Casos de uso onde desempenho e simplicidade importantes, especialmente 
em scripts, aplicações web, tarefas automatizadas ou sistemas distribuídos simples.

Quando usar concorrência e quando usar paralelismo?


# ConcurrentFutures

Este repositório contém exemplos práticos sobre Computação Paralela e Concorrente em Python utilizando o módulo `concurrent.futures`. O objetivo é demonstrar a diferença entre tarefas **I/O-bound** e **CPU-bound**, e como escolher o executor correto para cada cenário.

### Visão Geral

O módulo `concurrent.futures` fornece uma abstração de alto nível para execução assíncrona.

### Diferença Fundamental:

| Recurso | ThreadPoolExecutor | ProcessPoolExecutor |
| :--- | :--- | :--- |
| **Abordagem** | Concorrência | Paralelismo |
| **Melhor para** | Tarefas I/O-bound (Rede, Disco, DB) | Tarefas CPU-bound (Cálculos, Imagens) |
| **Limitação** | Sujeito ao Global Interpreter Lock (GIL) | Maior uso de memória (Overhead de processos) |

### Conteúdo do Repositório

1.  **I/O-bound (Concorrência):** Exemplos de downloads simultâneos de URLs.
2.  **CPU-bound (Paralelismo):** Verificação de números primos de alta magnitude.
3.  **Gerenciamento de Futures:** Demonstração de `map()` vs `as_completed()`.

### Como Executar

Certifique-se de ter o `requests` instalado:

```
     pip install requests
```

## ThreadPoolExecutor
ThreadPoolExecutor para tarefas I/O-bound (como acesso a arquivos, redes, bancos de dados).

Tipo de Tarefa:	
- ### Leitura/escrita de arquivos
  - Melhor abordagem:
    - #### Concorrência com threads
  - Executor em Python:
    - #### ThreadPoolExecutor

Tipo de Tarefa:	
- #### Requisições HTTP simultâneas
  - Melhor abordagem:
    - #### Concorrência com threads
  - Executor em Python:
    - #### ThreadPoolExecutor

## ProcessPoolExecutor
ProcessPoolExecutor: para tarefas CPU-bound (como cálculos pesados).

Tipo de Tarefa:	
- #### Processamento de imagens
  - Melhor abordagem:
    - #### Paralelismo com processos
  - Executor em Python:
    - #### ProcessPoolExecutor

Tipo de Tarefa:	
- #### Cálculos matemáticos pesados
  - Melhor abordagem:
     - #### Paralelismo com processos
   - Executor em Python:
     - #### ProcessPoolExecutor
     