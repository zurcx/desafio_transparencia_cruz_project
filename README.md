# Desafio Transparência - Análise de Dados Públicos (Pipeline ETL e Camada Gold)

Este projeto consiste em uma pipeline completa de Engenharia e Análise de Dados para extração, limpeza, transformação e visualização de dados públicos sobre viagens corporativas, diárias e passagens do Governo Federal.

---

## Tecnologias Utilizadas

- Linguagem: Python 3.12
- Banco de Dados: MySQL 8.0
- Bibliotecas Python: pandas, mysql-connector-python, plotly, kaleido
- Interface/Visualização: Jupyter Notebook / VS Code
- Ambiente de Desenvolvimento: Linux

---

## Estrutura do Projeto

desafio_transparencia_cruz_project/
├── _MySQL/                   # Módulos de conexão e configuração do MySQL
│   ├── banco.py              # Script com funções de conexão com o banco
│   └── config.py             # Credenciais e parâmetros do banco de dados
├── data/                     # Dados brutos em CSV e arquivos compactados (.zip)
├── graficos_png/             # Imagens estáticas exportadas dos gráficos em alta resolução
├── logs/                     # Registros de execução da pipeline
├── scripts/                  # Scripts da pipeline ETL
│   ├── 1_extrair.py          # Script de ingestão dos dados brutos (Camada Bronze)
│   ├── 2_transformar.py      # Script de tratamento e carga (Camada Silver / Gold)
│   └── banco.py              # Auxiliar de banco
├── sql/                      # Scripts DDL/DML e dumps SQL
│   └── transparencia20260710_Cruz.sql
├── 3_analise.ipynb           # Notebook Jupyter com a análise exploratória e geração de gráficos
├── gerar_notebook.py         # Script Python para recriar/automatizar o notebook de análise
└── README.md                 # Documentação do projeto

---

## Arquitetura da Pipeline (Medallion Architecture)

1. Camada Bronze (Raw): Ingestão dos arquivos CSV brutos baixados do Portal da Transparência (2025_Viagem.csv, 2025_Passagem.csv, etc.) diretamente na pasta data/.
2. Camada Silver (Clean): Limpeza de dados, remoção de duplicatas, tratamento de encoding (UTF-8/Latin1), padronização de datas, moedas e valores nulos.
3. Camada Gold (Consolidated): Tabelas agregadas e otimizadas no MySQL (gold_viagens_consolidadas, gold_pagamento_limpo, gold_trecho_limpo) para alimentar relatórios e visualizações de negócios.

---

## Como Executar o Projeto

### 1. Pré-requisitos
Garantir que o Python 3.12+ e o MySQL Server estejam instalados e configurados no ambiente.

### 2. Configuração do Ambiente Virtual
1. Criar o ambiente virtual:
   python3 -m venv venv

2. Ativar o ambiente virtual:
   source venv/bin/activate

3. Instalar as dependências necessárias:
   pip install pandas mysql-connector-python plotly kaleido

### 3. Configuração do Banco de Dados
Edite o arquivo _MySQL/config.py com as credenciais do seu MySQL local:
DB_CONFIG = {
    'host': 'localhost',
    'user': 'seu_usuario',
    'password': 'sua_senha',
    'database': 'transparencia'
}

Importe a estrutura do banco de dados (opcional, caso vá utilizar o dump pronto):
mysql -u seu_usuario -p transparencia < sql/transparencia20260710_Cruz.sql

### 4. Executando a Pipeline ETL
1. Extração dos dados:
   python3 scripts/1_extrair.py

2. Transformação e carga na camada Gold:
   python3 scripts/2_transformar.py

### 5. Gerando e Executando a Análise Consolidada
Para gerar/atualizar o notebook de análise e exportar os gráficos em .png:
python3 gerar_notebook.py

Em seguida, abra o Jupyter Notebook ou VS Code para executar e visualizar o arquivo 3_analise.ipynb.

---

## Principais Perguntas de Negócio Respondidas

1. Top 5 Órgãos por Custo Total: Quais órgãos públicos acumulam maiores gastos com viagens?
2. Custo Médio por Destino: Quais cidades/locais possuem o maior custo médio por viagem?
3. Análise de Duração: Qual viagem registrada teve a maior duração contínua em dias?
4. Ticket Médio por Modalidade de Pagamento: Qual meio de pagamento transaciona os maiores valores médios?
5. Distribuição do Meio de Transporte: Proporção do uso de modal aéreo, terrestre e outros nos trechos.
6. Frequência de Trechos por UF: Estados (UF) com maior concentração de deslocamentos corporativos.
7. Total Efetivamente Pago por Órgão Superior: Análise financeira comparativa de desembolso real.

---

## Autor

Desenvolvido por Luiz Cruz como parte do Desafio de Dados/Transparência.