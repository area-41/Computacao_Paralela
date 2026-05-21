# Projetos de Computação Paralela

Este repositório reúne implementações práticas, algoritmos de processamento de imagens e pipelines de dados desenvolvidos para explorar o uso eficiente de múltiplos núcleos de processamento, concorrência, concorrência assíncrona e paralelismo puro.

---

### Estrutura do Repositório

O repositório está organizado de forma a contrastar diferentes abordagens de concorrência e paralelismo no ecossistema Python:

| Módulo / Pasta | Descrição Teórica & Prática | Tecnologias Utilizadas |
| :--- | :--- | :--- |
| **`.devcontainer`** | Ambiente de desenvolvimento conteinerizado isolado para garantir que todas as dependências rodem de forma consistente em qualquer máquina ou via GitHub Codespaces. | Docker, Dev Containers |
| **`4.Desafio_Monitoramento_Sites`** | Sistema de checagem de integridade e latência de múltiplos servidores web rodando de forma concorrente para evitar o bloqueio por conexões de rede (*I/O Bound*). | Python `threading` / `asyncio` |
| **`5.Desafio_Gaussian_Blur`** | Algoritmo de processamento de imagem (Filtro de Desfoque Gaussiano) paralelizado. Divisão de matrizes de pixels para computação intensiva de CPU (*CPU Bound*). | Python `multiprocessing` / NumPy |
| **`ConcurrentFutures`** | Laboratório utilizando a API de alto nível `concurrent.futures` para abstrair o gerenciamento de pools de threads (`ThreadPoolExecutor`) e processos (`ProcessPoolExecutor`). | `concurrent.futures` |
| **`Multiprocessing`** | Implementação de paralelismo real contornando o *GIL (Global Interpreter Lock)* do Python por meio da criação de subprocessos com memória isolada. | Python `multiprocessing` |
| **`PipelinePolars`** | Criação de pipelines de análise de dados rápidos e otimizados, utilizando processamento paralelo nativo em queries estruturadas através da engine Polars. | Polars, Python |


#### Como Executar os Desafios

### 1. Filtro Desfoque Gaussiano Paralelo (`5.Desafio_Gaussian_Blur`)
Este desafio demonstra o ganho de performance ao quebrar uma tarefa pesada de processamento de imagem em múltiplos processos concorrentes.

1. Navegue até a pasta do desafio:

               cd 5.Desafio_Gaussian_Blur


2. Instale as dependências de imagem (caso não esteja usando o Dev Container):

                pip install -r ../requirements.txt


3. Execute o script principal:

                python gaussian_blur.py



### 2. Monitoramento de Sites (`4.Desafio_Monitoramento_Sites`)

Otimização de requisições de rede assíncronas/concorrentes para verificar o status de múltiplos endpoints simultaneamente.

1. Navegue até a pasta:

                cd 4.Desafio_Monitoramento_Sites



2. Execute o monitor:

                python monitoramento.py



### Configuração do Ambiente Virtual (`.devcontainer`)

Este repositório possui suporte integrado para **Dev Containers** e **GitHub Codespaces**. O container padrão utiliza o gerenciador de pacotes moderno **UV** para pré-instalar ferramentas como o `tabulate` (utilizado para formatação de tabelas e logs de performance no console).

Se preferir rodar localmente sem Docker, configure o ambiente usando o arquivo de dependências geral:

                pip install -r requirements.txt


---

*Repositório desenvolvido para fins acadêmicos e análise de benchmarks de performance computacional.*