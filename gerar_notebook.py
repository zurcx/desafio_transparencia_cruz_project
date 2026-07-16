import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Desafio Transparência - Análise Consolidada (Camada Gold)\n",
                "Este notebook realiza a extração, transformação e análise de dados sobre diárias, passagens e viagens corporativas. Os resultados são apresentados em DataFrames e exportados como imagens estáticas em alta resolução (`.png`) na pasta `graficos_png/`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import sys\n",
                "import os\n",
                "import pandas as pd\n",
                "import plotly.express as px\n",
                "import plotly.io as pio\n",
                "\n",
                "# Garantir que a pasta de gráficos exista\n",
                "os.makedirs('graficos_png', exist_ok=True)\n",
                "\n",
                "# Definir renderizador estático como padrão para visualização limpa e exportação\n",
                "pio.renderers.default = 'png'\n",
                "\n",
                "# Conexão com o banco de dados (Importando diretamente do banco.py da raiz)\n",
                "import banco\n",
                "\n",
                "conn = banco.criar_conexao()\n",
                "print('Conexão estabelecida com sucesso!')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Top 5 Órgãos com Maior Custo Total\n",
                "**Pergunta de Negócio:** Quais são os 5 órgãos públicos que acumularam o maior valor em gastos com viagens e diárias?"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "query_1 = '''\n",
                "SELECT \n",
                "    `Nome do órgão superior` AS orgao,\n",
                "    SUM(`Valor total da viagem`) AS custo_total\n",
                "FROM gold_viagens_consolidadas\n",
                "GROUP BY 1\n",
                "ORDER BY custo_total DESC\n",
                "LIMIT 5;\n",
                "'''\n",
                "df1 = pd.read_sql(query_1, conn)\n",
                "df1_sorted = df1.sort_values('custo_total', ascending=True)\n",
                "\n",
                "fig1 = px.bar(\n",
                "    df1_sorted,\n",
                "    x='custo_total',\n",
                "    y='orgao',\n",
                "    orientation='h',\n",
                "    text=df1_sorted['custo_total'].apply(lambda x: f'R$ {x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.').strip()),\n",
                "    title='Top 5 Órgãos por Custo Total de Viagens'\n",
                ")\n",
                "\n",
                "max_val1 = df1_sorted['custo_total'].max()\n",
                "fig1.update_traces(\n",
                "    textposition='outside',\n",
                "    texttemplate='  %{text}',\n",
                "    cliponaxis=False\n",
                ")\n",
                "fig1.update_layout(\n",
                "    margin=dict(l=260, r=180, t=60, b=50),\n",
                "    xaxis=dict(range=[0, max_val1 * 1.35], title='Custo Total (R$)'),\n",
                "    yaxis=dict(title='')\n",
                ")\n",
                "\n",
                "fig1.write_image('graficos_png/1_maior_custo_total_orgao.png', scale=2)\n",
                "fig1.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Top 3 Destinos com Maior Custo Médio por Viagem\n",
                "**Pergunta de Negócio:** Quais destinos possuem a maior média de custo por ocorrência individual de viagem?"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "query_2 = '''\n",
                "SELECT \n",
                "    `Destinos` AS destino,\n",
                "    AVG(`Valor total da viagem`) AS custo_medio\n",
                "FROM gold_viagens_consolidadas\n",
                "WHERE `Destinos` IS NOT NULL AND `Destinos` != ''\n",
                "GROUP BY 1\n",
                "ORDER BY custo_medio DESC\n",
                "LIMIT 3;\n",
                "'''\n",
                "df2 = pd.read_sql(query_2, conn)\n",
                "\n",
                "fig2 = px.bar(\n",
                "    df2,\n",
                "    x='destino',\n",
                "    y='custo_medio',\n",
                "    text=df2['custo_medio'].apply(lambda x: f'R$ {x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.').strip()),\n",
                "    title='Top 3 Destinos com Maior Custo Médio'\n",
                ")\n",
                "\n",
                "max_val2 = df2['custo_medio'].max()\n",
                "fig2.update_traces(\n",
                "    textposition='outside',\n",
                "    cliponaxis=False\n",
                ")\n",
                "fig2.update_layout(\n",
                "    margin=dict(l=60, r=60, t=80, b=60),\n",
                "    yaxis=dict(range=[0, max_val2 * 1.35], title='Custo Médio (R$)'),\n",
                "    xaxis=dict(title='Destino')\n",
                ")\n",
                "\n",
                "fig2.write_image('graficos_png/2_custo_medio_destino.png', scale=2)\n",
                "fig2.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Viagem de Maior Duração\n",
                "**Pergunta de Negócio:** Qual foi o registro de viagem corporativa com o maior número de dias contínuos e qual foi o valor total associado?"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "query_3 = '''\n",
                "SELECT \n",
                "    `Identificador do processo de viagem` AS id_viagem,\n",
                "    `Nome` AS viajante,\n",
                "    `Motivo do afastamento` AS motivo,\n",
                "    `Duração em Dias` AS duracao_dias,\n",
                "    `Valor total da viagem` AS custo_total\n",
                "FROM gold_viagens_consolidadas\n",
                "ORDER BY duracao_dias DESC\n",
                "LIMIT 1;\n",
                "'''\n",
                "df3 = pd.read_sql(query_3, conn)\n",
                "display(df3)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Tipo de Pagamento com Maior Valor Médio\n",
                "**Pergunta de Negócio:** Qual a modalidade financeira/tipo de pagamento que apresenta o maior ticket médio transacionado?"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "query_4 = '''\n",
                "SELECT \n",
                "    `Tipo de pagamento` AS tipo_pagamento,\n",
                "    AVG(`Valor`) AS valor_medio\n",
                "FROM gold_pagamento_limpo\n",
                "WHERE `Tipo de pagamento` IS NOT NULL AND `Tipo de pagamento` != ''\n",
                "GROUP BY 1\n",
                "ORDER BY valor_medio DESC;\n",
                "'''\n",
                "df4 = pd.read_sql(query_4, conn)\n",
                "\n",
                "fig4 = px.bar(\n",
                "    df4,\n",
                "    x='tipo_pagamento',\n",
                "    y='valor_medio',\n",
                "    text=df4['valor_medio'].apply(lambda x: f'R$ {x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.').strip()),\n",
                "    title='Valor Médio por Tipo de Pagamento'\n",
                ")\n",
                "\n",
                "max_val4 = df4['valor_medio'].max()\n",
                "fig4.update_traces(\n",
                "    textposition='outside',\n",
                "    cliponaxis=False\n",
                ")\n",
                "fig4.update_layout(\n",
                "    margin=dict(l=60, r=60, t=80, b=60),\n",
                "    yaxis=dict(range=[0, max_val4 * 1.35], title='Valor Médio (R$)'),\n",
                "    xaxis=dict(title='Tipo de Pagamento')\n",
                ")\n",
                "\n",
                "fig4.write_image('graficos_png/4_valor_medio_pagamento.png', scale=2)\n",
                "fig4.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Meio de Transporte Mais Utilizado\n",
                "**Pergunta de Negócio:** Qual a proporção e distribuição do uso de meios de transporte nos trechos realizados?"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "query_5 = '''\n",
                "SELECT \n",
                "    `Meio de transporte` AS meio_transporte,\n",
                "    COUNT(*) AS total_trechos\n",
                "FROM gold_trecho_limpo\n",
                "WHERE `Meio de transporte` IS NOT NULL AND `Meio de transporte` != ''\n",
                "GROUP BY 1\n",
                "ORDER BY total_trechos DESC;\n",
                "'''\n",
                "df5 = pd.read_sql(query_5, conn)\n",
                "\n",
                "fig5 = px.pie(\n",
                "    df5,\n",
                "    values='total_trechos',\n",
                "    names='meio_transporte',\n",
                "    title='Distribuição dos Meios de Transporte Utilizados',\n",
                "    hole=0.4\n",
                ")\n",
                "fig5.update_traces(textinfo='percent+label')\n",
                "fig5.update_layout(margin=dict(l=50, r=50, t=60, b=50))\n",
                "\n",
                "fig5.write_image('graficos_png/5_meio_transporte_mais_usado.png', scale=2)\n",
                "fig5.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6. Frequência de Trechos por UF de Destino\n",
                "**Pergunta de Negócio:** Quais estados da federação (UF) concentram o maior volume de trechos em viagens corporativas?"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "query_6 = '''\n",
                "SELECT \n",
                "    `UF - Destino` AS uf_destino,\n",
                "    COUNT(*) AS frequencia\n",
                "FROM gold_trecho_limpo\n",
                "WHERE `UF - Destino` IS NOT NULL AND `UF - Destino` != ''\n",
                "GROUP BY 1\n",
                "ORDER BY frequencia DESC;\n",
                "'''\n",
                "df6 = pd.read_sql(query_6, conn)\n",
                "\n",
                "fig6 = px.bar(\n",
                "    df6,\n",
                "    x='uf_destino',\n",
                "    y='frequencia',\n",
                "    text='frequencia',\n",
                "    title='Frequência de Trechos por UF de Destino'\n",
                ")\n",
                "\n",
                "max_val6 = df6['frequencia'].max()\n",
                "fig6.update_traces(\n",
                "    textposition='outside',\n",
                "    cliponaxis=False\n",
                ")\n",
                "fig6.update_layout(\n",
                "    margin=dict(l=50, r=50, t=80, b=100),\n",
                "    xaxis=dict(tickangle=-45, title='UF de Destino'),\n",
                "    yaxis=dict(range=[0, max_val6 * 1.3], title='Total de Trechos')\n",
                ")\n",
                "\n",
                "fig6.write_image('graficos_png/6_uf_destino_frequencia.png', scale=2)\n",
                "fig6.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 7. Órgão Superior que Efetivamente Pagou Mais no Total\n",
                "**Pergunta de Negócio:** Qual unidade gestora realizou a maior soma em pagamentos liquidados/efetivados?"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "query_7 = '''\n",
                "SELECT \n",
                "    v.`Nome do órgão superior` AS orgao,\n",
                "    SUM(p.`Valor`) AS total_pago\n",
                "FROM gold_pagamento_limpo p\n",
                "JOIN gold_viagens_consolidadas v \n",
                "  ON p.`Identificador do processo de viagem` = v.`Identificador do processo de viagem`\n",
                "WHERE v.`Nome do órgão superior` IS NOT NULL\n",
                "GROUP BY 1\n",
                "ORDER BY total_pago DESC\n",
                "LIMIT 5;\n",
                "'''\n",
                "df7 = pd.read_sql(query_7, conn)\n",
                "df7_sorted = df7.sort_values('total_pago', ascending=True)\n",
                "\n",
                "fig7 = px.bar(\n",
                "    df7_sorted,\n",
                "    x='total_pago',\n",
                "    y='orgao',\n",
                "    orientation='h',\n",
                "    text=df7_sorted['total_pago'].apply(lambda x: f'R$ {x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.').strip()),\n",
                "    title='Top Órgãos por Total Efetivamente Pago'\n",
                ")\n",
                "\n",
                "max_val7 = df7_sorted['total_pago'].max()\n",
                "fig7.update_traces(\n",
                "    textposition='outside',\n",
                "    texttemplate='  %{text}',\n",
                "    cliponaxis=False\n",
                ")\n",
                "fig7.update_layout(\n",
                "    margin=dict(l=260, r=180, t=60, b=50),\n",
                "    xaxis=dict(range=[0, max_val7 * 1.35], title='Total Pago (R$)'),\n",
                "    yaxis=dict(title='')\n",
                ")\n",
                "\n",
                "fig7.write_image('graficos_png/7_orgao_que_mais_pagou.png', scale=2)\n",
                "fig7.show()"
            ]
        }
    ],
    "metadata": {
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

with open("3_analise.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("Notebook '3_analise.ipynb' recriado com sucesso!")