# Automação de Análise de Crédito - Case CERC

O objetivo é demonstrar uma solução escalável para lidar com o aumento exponencial no volume de operações de crédito previsto com a nova regulamentação da Duplicata Escritural.

##  O Desafio

Com a entrada em vigor da regulamentação da duplicata escritural, estima-se um aumento de **10x no volume de operações**. O time de analistas atual não conseguirá absorver essa demanda manualmente. O objetivo deste projeto é automatizar a "carpintaria intelectual" da análise de crédito, permitindo que os analistas foquem apenas em casos complexos.

## Tarefas Selecionadas (O*NET)

Para criar um fluxo de automação coerente e funcional, selecionei as seguintes tarefas do dataset O*NET, organizadas em uma sequência lógica de execução:

1.  **Task 1: Analyze credit data and financial statements**

2.  **Task 6: Compare liquidity, profitability, and credit histories with similar establishments**

3.  **Task 4: Prepare reports that include the degree of risk**

##  Arquitetura e Stack Tecnológica

A solução foi desenhada utilizando uma abordagem híbrida: **Lógica Determinística + Inteligência Generativa**.

*   **Python (Core Logic):**
    *   Utilizado para o processamento e cálculos matemáticos.
    *   Scripts: `analise_credito.py` (cálculos) e manipulação de JSONs.
*   **Agentes de IA (Raciocínio):**
    *   Responsáveis por interpretar os dados, entender a intenção do usuário e gerar os insights textuais.
    *   **Google Agent Development Kit (ADK):** Implementado em `my_agent/`, focado em uma estrutura robusta de agentes.
    *   **LangChain + Groq (openai/gpt-oss-120b):** Implementado em `langchain_agent.py`, demonstrando flexibilidade de modelos e uso de *Tools* para conectar a IA aos dados.
*   **n8n (Orquestração):**
    *   Utilizado (conceitualmente/externamente) para gatilhos de entrada (ex: recebimento de um novo pedido de crédito) e conexão dos fluxos.

# Google ADK e Langchain arquitetura
<img width="1305" height="436" alt="image" src="https://github.com/user-attachments/assets/e8845765-d434-4164-a384-7db56bfa199d" />


# n8N arquitetua
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/580d4f97-6110-4400-a0e5-32fdc4aead45" />



### Estrutura de Arquivos

```
/root/cerc/
├── analise_credito.py      # Lógica de negócio e classes (Dataclasses) para cálculos financeiros
├── empresa_dados.json      # Dados de entrada (simulação de um cliente)
├── benchmark.json          # Dados de mercado para comparação (Task 6)
├── langchain_agent.py      # Agente LangChain que utiliza Tools para acessar os dados
├── my_agent/               # Estrutura do Google ADK
│   └── agent.py            # Definição do agente e ferramentas do ADK
└── README.md               # Documentação do projeto
```

##  Como Executar

### Pré-requisitos

```bash
pip install google-adk langchain langchain-groq langchain-core
```

### 1. Executando o Agente LangChain (Recomendado)

Este agente possui ferramentas para calcular indicadores e comparar com o benchmark.

```bash
# É necessário uma chave de API do Groq
export GROQ_API_KEY="sua_chave_aqui"
python3 langchain_agent.py
```

**Exemplos de perguntas:**
*   "Qual a situação de liquidez desta empresa?"
*   "Compare a margem líquida da empresa com o mercado."
*   "Gere um relatório resumido."

### 2. Executando o Agente Google ADK

```bash
python3 my_agent/agent.py
```

##  Decisões de Design

1.  **Separação de Responsabilidades:** O cálculo financeiro (Liquidez Corrente = Ativo Circulante / Passivo Circulante) é feito via código Python (`analise_credito.py`). A IA apenas *chama* essa função. Isso garante 100% de precisão nos números.
2.  **Uso de Tools:** Os agentes não "leem" o arquivo inteiro de uma vez para tentar adivinhar. Eles possuem ferramentas específicas (`obter_indicadores`, `comparar_benchmark`) que buscam a informação precisa quando solicitada.
3.  **Escalabilidade:** A estrutura permite que, ao receber 10x mais duplicatas, o sistema processe os dados automaticamente e entregue ao analista apenas o relatório final comparativo, reduzindo drasticamente o tempo de análise manual.

# Links
* link do chat n8n: https://vanger7.app.n8n.cloud/webhook/a3c1fc4a-8918-4ae8-8feb-591b9a4fed36/chat
* link do video: https://www.youtube.com/watch?v=OUOnsR4UtZA
