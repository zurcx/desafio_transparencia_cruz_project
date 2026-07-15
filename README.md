Desafio Transparência - Análise Consolidada de Viagens Corporativas
Este projeto faz parte do pipeline de engenharia e análise de dados da iniciativa SCTec Dados (projetos_cruz). Ele realiza a extração, transformação e análise de dados sobre diárias, passagens e viagens corporativas a partir de um banco de dados MySQL, organizando as tabelas no conceito de arquitetura de medalhas (Bronze, Silver e Gold).

O objetivo principal é responder a perguntas estratégicas de negócio, consolidar indicadores e gerar relatórios visuais automáticos diretamente através do ambiente Jupyter.

📋 Funcionalidades
Mapeamento Dinâmico: Identificação automatizada da estrutura e colunas de tabelas no banco de dados diretamente no notebook (evitando quebras por colunas como cidade_destino ou uf_destino).

Pipeline de Dados (Arquitetura Medalhão): Organização das etapas de transformação para garantir dados limpos, tipados e prontos para consumo na camada Gold.

Visualização Avançada: Geração automática de gráficos com Plotly que são exportados em alta resolução (.png) na pasta do projeto.

Layout Profissional: Gráficos com tratamento de margens para textos longos e inclinação de eixos em 45° para melhor leitura.

🛠️ Estrutura do Projeto
Plaintext
desafio_transparencia_cruz_project/
├── _MySQL/
│   └── banco.py          # Script de gerenciamento e conexão com o banco de dados
├── graficos_png/         # Diretório onde as imagens dos gráficos são exportadas
├── scripts/
│   └── 3_analise.ipynb   # Cópia de segurança do notebook de análise
├── venv/                 # Ambiente virtual Python
└── 3_analise.ipynb       # Notebook Jupyter principal (Camada Gold)
📊 Relatório Geral & Insights (Camada Gold)
Abaixo estão listadas as 7 perguntas de negócio respondidas pelo ecossistema do notebook, acompanhadas de suas respectivas análises e dos gráficos gerados automaticamente na pasta graficos_png/.

1. Os 5 órgãos com maior custo total
Gráfico Gerado: graficos_png/1_maior_custo_total_orgao.png

Explicação: Um gráfico de barras horizontais ordenado de forma ascendente. Ele isola os 5 maiores órgãos públicos em volume absoluto de gastos (R$). É ideal para auditoria focada e para identificar onde estão concentrados os maiores budgets de viagem.

2. Os 3 destinos com maior custo médio por viagem
Gráfico Gerado: graficos_png/2_custo_medio_destino.png

Explicação: Gráfico de barras verticais focado no custo médio (passagens + diárias). Ajuda a detectar cidades que, embora possam não ter o maior volume de viagens, possuem um custo logístico ou de estadia significativamente mais alto por ocorrência.

3. A viagem de maior duração e seu custo total
Exibição: Tabela de Dados (DataFrame)

Explicação: Identifica o caso extremo (outlier) de permanência em viagem corporativa. O relatório exibe o ID da viagem, o nome do viajante, o motivo oficial registrado e a duração em dias combinada ao custo total, essencial para avaliar a aderência às regras de concessão de diárias longas.

4. Qual o tipo de pagamento com maior valor médio?
Gráfico Gerado: graficos_png/4_valor_medio_pagamento.png

Explicação: Apresenta o comportamento financeiro por modalidade de pagamento (ex: boleto, cartão corporativo, ordem bancária). Permite entender qual meio de pagamento costuma centralizar as transações de maior valor unitário.

5. Qual o meio de transporte mais usado nos trechos?
Gráfico Gerado: graficos_png/5_meio_transporte_mais_usado.png

Explicação: Gráfico de setores (Donut/Pizza) com exibição de porcentagem e rótulo dinâmico. Demonstra a matriz de transporte utilizada pelos servidores (Aéreo, Rodoviário, Ferroviário), servindo como base para contratos de frotas ou convênios com companhias aéreas.

6. Qual UF de destino aparece em mais trechos?
Gráfico Gerado: graficos_png/6_uf_destino_frequencia.png

Explicação: Gráfico de barras verticais cobrindo a distribuição por estado. Possui eixos rotacionados em 45° para evitar sobreposição de texto. Revela o polo geográfico que mais atrai ou demanda missões e viagens corporativas da instituição.

7. Qual órgão pagou mais no total?
Gráfico Gerado: graficos_png/7_orgao_que_mais_pagou.png

Explicação: Cruzamento da tabela de pagamentos efetivos com as viagens por órgão superior. Diferente do "custo total planejado", este indicador de barras horizontais foca no fluxo de caixa real despendido por cada unidade gestora.

🚀 Como Executar o Projeto
1. Pré-requisitos
Certifique-se de ter o Python 3.12+ e o banco MySQL configurados corretamente. O arquivo _MySQL/banco.py deve estar parametrizado com as credenciais corretas do seu ambiente.

2. Ativar o Ambiente Virtual
No terminal, navegue até a raiz do projeto e ative seu ambiente virtual:

Bash
source venv/bin/activate  # No Linux/macOS
# ou
.\venv\Scripts\activate  # No Windows
3. Executar as Análises
Abra o arquivo principal 3_analise.ipynb (localizado na raiz do projeto) utilizando o VS Code ou Jupyter Lab:

Selecione o Kernel do seu ambiente virtual (venv) no canto superior direito do editor.

Clique na opção "Run All" (Executar Tudo).

Ao final da execução:

Os resultados serão exibidos em tabelas estilizadas (DataFrames).

Os gráficos customizados e com eixos corrigidos serão renderizados na tela.

Arquivos estáticos de alta resolução serão salvos automaticamente na pasta graficos_png/.

📦 Principais Tecnologias Utilizadas
Python 3.12

Pandas: Manipulação de dados e execução de queries estruturadas diretamente para dataframes.

Plotly Express & Plotly.io: Criação de gráficos dinâmicos e controle de renderização estática.

Kaleido: Biblioteca de backend para exportação limpa de gráficos para arquivos de imagem .png.

MySQL Connector: Interface nativa e estável de comunicação com o banco de dados.

Desenvolvido como parte do desafio de transparência e eficiência pública. 📊✨# Desafio Transparência - Análise Consolidada de Viagens Corporativas

Este projeto faz parte do pipeline de engenharia e análise de dados da iniciativa **SCTec Dados** (`projetos_cruz`). Ele realiza a extração, transformação e análise de dados sobre diárias, passagens e viagens corporativas a partir de um banco de dados MySQL, organizando as tabelas no conceito de arquitetura de medalhas (**Bronze**, **Silver** e **Gold**).

O objetivo principal é responder a perguntas estratégicas de negócio, consolidar indicadores e gerar relatórios visuais automáticos diretamente através do ambiente Jupyter.

---

## 📋 Funcionalidades

- **Mapeamento Dinâmico:** Identificação automatizada da estrutura e colunas de tabelas no banco de dados diretamente no notebook (ex: variação de nomes de colunas como `cidade_destino` ou `uf_destino`).
- **Pipeline de Dados (Arquitetura Medalhão):** Organização das etapas de transformação para garantir dados limpos, tipados e prontos para consumo na camada Gold.
- **Visualização Avançada:** Geração automática de gráficos interativos com Plotly que são exportados em alta resolução (`.png`).
- **Layout Profissional:** Gráficos com tratamento de margens para textos longos e inclinação de rótulos (eixos em 45°).

---

## 🛠️ Estrutura do Projeto

```text
desafio_transparencia_cruz_project/
├── _MySQL/
│   └── banco.py          # Script de gerenciamento e conexão com o banco de dados
├── graficos_png/         # Diretório onde as imagens dos gráficos são exportadas
├── scripts/
│   └── 3_analise.ipynb   # Cópia de segurança do notebook de análise
├── venv/                 # Ambiente virtual Python
└── 3_analise.ipynb       # Notebook Jupyter principal (Camada Gold)

📊 Perguntas de Negócio Respondidas (Camada Gold)
O notebook principal (3_analise.ipynb) realiza análises complexas para responder a 7 questões fundamentais de governança e gastos:

Top 5 Órgãos com maior custo total acumulado.

Top 3 Destinos com maior custo médio por viagem individual.

Detalhamento da viagem de maior duração registrada e seu impacto financeiro.

Análise do tipo de pagamento que possui o maior valor médio.

Identificação do meio de transporte mais utilizado nas rotas corporativas.

Frequência e volumetria de trechos utilizando a UF de destino (com eixos otimizados em 45°).

Identificação de qual órgão efetuou o maior volume de pagamentos reais.

🚀 Como Executar o Projeto
1. Pré-requisitos
Certifique-se de ter o Python 3.12+ e o banco MySQL configurados corretamente. O arquivo banco.py deve estar parametrizado com as credenciais corretas do seu ambiente.

2. Ativar o Ambiente Virtual
No terminal, navegue até a raiz do projeto e ative seu ambiente virtual:

source venv/bin/activate  # No Linux/macOS
# ou
.\venv\Scripts\activate  # No Windows

3. Executar as Análises
Abra o arquivo principal 3_analise.ipynb (localizado na raiz do projeto) utilizando o VS Code ou Jupyter Lab:

Selecione o Kernel do seu ambiente virtual (venv) no canto superior direito do editor.

Clique na opção "Run All" (Executar Tudo).

Ao final da execução:

Os resultados serão exibidos em tabelas estilizadas (DataFrames).

Os gráficos customizados e com eixos corrigidos serão renderizados na tela.

Arquivos estáticos de alta resolução serão salvos automaticamente na pasta graficos_png/.

📦 Principais Tecnologias Utilizadas
Python 3.12

Pandas: Manipulação de dados e execução de queries estruturadas diretamente para dataframes.

Plotly Express: Criação de gráficos dinâmicos de barras, setores (pizza) e linhas.

Kaleido: Biblioteca utilitária para exportação estática de gráficos Plotly para arquivos .png.

MySQL Connector: Interface nativa e performática de comunicação com o banco de dados.

Desenvolvido como parte do desafio de transparência e eficiência pública. 📊✨