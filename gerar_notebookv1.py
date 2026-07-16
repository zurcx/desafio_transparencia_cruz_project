import json

# Inicializa a estrutura limpa do Notebook
notebook_data = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

def add_markdown(texto_lista):
    notebook_data["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in texto_lista]
    })

def add_code(codigo_lista):
    notebook_data["cells"].append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [line + "\n" for line in codigo_lista]
    })

# --- CÉLULA 1: INTRODUÇÃO ---
add_markdown([
    "# Camada GOLD - Análise Consolidada de Viagens Corporativas",
    "",
    "Este notebook responde às perguntas estratégicas de negócio utilizando dados consolidados das tabelas **SILVER**. Para cada questão, apresentamos a consulta SQL, a tabela de resultados e o respectivo gráfico (exportado automaticamente em PNG).",
    "",
    "**Perguntas Respondidas:**",
    "1. Os 5 órgãos com maior custo total.",
    "2. Os 3 destinos com maior custo médio por viagem.",
    "3. A viagem de maior duração e seu custo total.",
    "4. Qual o tipo de pagamento com maior valor médio?",
    "5. Qual o meio de transporte mais usado nos trechos?",
    "6. Qual UF de destino aparece em mais trechos?",
    "7. Qual órgão pagou mais no total?"
])

# --- CÉLULA 2: CÓDIGO CONEXÃO, SETUP E INSPEÇÃO DE COLUNAS ---
add_code([
    "import os",
    "import sys",
    "import pandas as pd",
    "import plotly.express as px",
    "import plotly.io as pio",
    "",
    "# Define o renderizador como png para evitar dependência do pacote nbformat no VS Code",
    "pio.renderers.default = 'png'",
    "",
    "# Mapeia os caminhos absolutos baseados na estrutura de pastas real",
    "diretorio_raiz = os.path.abspath(os.path.join(os.getcwd()))",
    "pasta_mysql = os.path.join(diretorio_raiz, '_MySQL')",
    "pasta_mysql_alt = os.path.abspath(os.path.join(os.getcwd(), '..', '_MySQL'))",
    "",
    "# Adiciona as pastas de scripts e banco ao sistema de busca do Python",
    "for caminho in [diretorio_raiz, pasta_mysql, pasta_mysql_alt]:",
    "    if os.path.exists(caminho) and caminho not in sys.path:",
    "        sys.path.append(caminho)",
    "",
    "try:",
    "    import banco",
    "    print('Módulo \"banco\" importado com sucesso!')",
    "except ModuleNotFoundError:",
    "    raise ModuleNotFoundError('Não foi possível encontrar o módulo \"banco.py\".')",
    "",
    "# Garante a pasta para salvar os arquivos PNG na raiz do projeto",
    "pasta_graficos = os.path.join(diretorio_raiz, 'graficos_png')",
    "os.makedirs(pasta_graficos, exist_ok=True)",
    "",
    "conexao = banco.conectar()",
    "",
    "def consultar(sql):",
    "    return pd.read_sql(sql, conexao)",
    "",
    "def salvar_grafico(fig, nome_arquivo):",
    "    caminho_completo = os.path.join(pasta_graficos, nome_arquivo)",
    "    try:",
    "        fig.write_image(caminho_completo, scale=2, width=1000, height=550)",
    "        print(f'Gráfico Retornado com sucesso em: {caminho_completo}')",
    "    except Exception as e:",
    "        print(f'Erro ao salvar imagem (Certifique-se que o pacote kaleido está instalado): {e}')",
    "",
    "# --- MAPEAMENTO DINÂMICO DE COLUNAS DE DESTINO ---",
    "df_sample = pd.read_sql(\"SELECT * FROM silver_trecho LIMIT 1\", conexao)",
    "colunas_disponiveis = list(df_sample.columns)",
    "",
    "# Identifica a coluna correta para cidade de destino",
    "col_cidade = 'cidade_destino'",
    "for c in ['cidade_destino', 'destino', 'destino_cidade', 'cidade']:",
    "    if c in colunas_disponiveis:",
    "        col_cidade = c",
    "        break",
    "",
    "# Identifica a coluna correta para uf de destino",
    "col_uf = 'uf_destino'",
    "for u in ['uf_destino', 'uf', 'destino_uf', 'estado_destino']:",
    "    if u in colunas_disponiveis:",
    "        col_uf = u",
    "        break",
    "",
    "print(f'Ambiente inicializado! Colunas mapeadas em silver_trecho -> Cidade: {col_cidade}, UF: {col_uf}')"
])

# --- CÉLULA 3: PERGUNTA 1 ---
add_markdown(["## 1. Os 5 órgãos com maior custo total"])
add_code([
    "sql_p1 = \"\"\"",
    "SELECT nome_orgao_superior, SUM(valor_total) AS custo_total",
    "FROM silver_viagem",
    "GROUP BY nome_orgao_superior",
    "ORDER BY custo_total DESC",
    "LIMIT 5;",
    "\"\"\"",
    "df_p1 = consultar(sql_p1)",
    "display(df_p1)",
    "",
    "fig_p1 = px.bar(",
    "    df_p1, x='custo_total', y='nome_orgao_superior', orientation='h',",
    "    title='Top 5 Órgãos por Custo Total',",
    "    labels={'custo_total': 'Custo Total (R$)', 'nome_orgao_superior': 'Órgão Orgânico'},",
    "    text_auto='.2f', color_discrete_sequence=['#1f77b4']",
    ")",
    "fig_p1.update_layout(",
    "    template='plotly_white', ",
    "    title_font_family='Arial Black', ",
    "    yaxis={'categoryorder': 'total ascending'},",
    "    margin=dict(l=200, r=40, t=60, b=60),",
    "    height=500",
    ")",
    "fig_p1.show()",
    "salvar_grafico(fig_p1, '1_maior_custo_total_orgao.png')"
])

# --- CÉLULA 4: PERGUNTA 2 ---
add_markdown(["## 2. Os 3 destinos com maior custo médio por viagem"])
add_code([
    "sql_p2 = f\"\"\"",
    "SELECT t.{col_cidade} AS destino, AVG(v.valor_total) AS custo_medio",
    "FROM silver_trecho t",
    "INNER JOIN silver_viagem v ON t.id_viagem = v.id_viagem",
    "WHERE t.{col_cidade} IS NOT NULL AND t.{col_cidade} <> ''",
    "GROUP BY t.{col_cidade}",
    "ORDER BY custo_medio DESC",
    "LIMIT 3;",
    "\"\"\"",
    "df_p2 = consultar(sql_p2)",
    "display(df_p2)",
    "",
    "fig_p2 = px.bar(",
    "    df_p2, x='destino', y='custo_medio',",
    "    title='Top 3 Destinos por Custo Médio por Viagem',",
    "    labels={'custo_medio': 'Custo Médio (R$)', 'destino': 'Destino (Cidade)'},",
    "    text_auto='.2f', color_discrete_sequence=['#e377c2']",
    ")",
    "fig_p2.update_layout(",
    "    template='plotly_white', ",
    "    title_font_family='Arial Black',",
    "    margin=dict(l=40, r=40, t=60, b=60)",
    ")",
    "fig_p2.update_traces(textposition='outside')",
    "fig_p2.show()",
    "salvar_grafico(fig_p2, '2_custo_medio_destino.png')"
])

# --- CÉLULA 5: PERGUNTA 3 ---
add_markdown(["## 3. A viagem de maior duração e seu custo total"])
add_code([
    "sql_p3 = \"\"\"",
    "SELECT id_viagem, nome_viajante, duracao_dias, valor_total, motivo",
    "FROM silver_viagem",
    "ORDER BY duracao_dias DESC",
    "LIMIT 1;",
    "\"\"\"",
    "df_p3 = consultar(sql_p3)",
    "display(df_p3)"
])

# --- CÉLULA 6: PERGUNTA 4 ---
add_markdown(["## 4. Qual o tipo de pagamento com maior valor médio?"])
add_code([
    "sql_p4 = \"\"\"",
    "SELECT tipo_pagamento, AVG(valor) AS valor_medio",
    "FROM silver_pagamento",
    "GROUP BY tipo_pagamento",
    "ORDER BY valor_medio DESC;",
    "\"\"\"",
    "df_p4 = consultar(sql_p4)",
    "display(df_p4)",
    "",
    "fig_p4 = px.bar(",
    "    df_p4, x='tipo_pagamento', y='valor_medio',",
    "    title='Valor Médio por Tipo de Pagamento',",
    "    labels={'valor_medio': 'Valor Médio (R$)', 'tipo_pagamento': 'Tipo de Pagamento'},",
    "    text_auto='.2f', color_discrete_sequence=['#bcbd22']",
    ")",
    "fig_p4.update_layout(",
    "    template='plotly_white', ",
    "    title_font_family='Arial Black',",
    "    margin=dict(l=40, r=40, t=60, b=60)",
    ")",
    "fig_p4.update_traces(textposition='outside')",
    "fig_p4.show()",
    "salvar_grafico(fig_p4, '4_valor_medio_pagamento.png')"
])

# --- CÉLULA 7: PERGUNTA 5 ---
add_markdown(["## 5. Qual o meio de transporte mais usado nos trechos?"])
add_code([
    "sql_p5 = \"\"\"",
    "SELECT meio_transporte, COUNT(*) AS quantidade_uso",
    "FROM silver_trecho",
    "WHERE meio_transporte IS NOT NULL AND meio_transporte <> ''",
    "GROUP BY meio_transporte",
    "ORDER BY quantidade_uso DESC;",
    "\"\"\"",
    "df_p5 = consultar(sql_p5)",
    "display(df_p5)",
    "",
    "fig_p5 = px.pie(",
    "    df_p5, values='quantidade_uso', names='meio_transporte',",
    "    title='Meios de Transporte Mais Utilizados nos Trechos',",
    "    hole=0.4, color_discrete_sequence=px.colors.qualitative.Safe",
    ")",
    "fig_p5.update_traces(textinfo='percent+label', texttemplate='%{label}: %{percent:.2%}')",
    "fig_p5.update_layout(",
    "    template='plotly_white', ",
    "    title_font_family='Arial Black',",
    "    margin=dict(l=40, r=40, t=60, b=60)",
    ")",
    "fig_p5.show()",
    "salvar_grafico(fig_p5, '5_meio_transporte_mais_usado.png')"
])

# --- CÉLULA 8: PERGUNTA 6 (ROTACIONADA EM 45°) ---
add_markdown(["## 6. Qual UF de destino aparece em mais trechos?"])
add_code([
    "sql_p6 = f\"\"\"",
    "SELECT {col_uf} AS uf_destino, COUNT(*) AS quantidade_trechos",
    "FROM silver_trecho",
    "WHERE {col_uf} IS NOT NULL AND {col_uf} <> ''",
    "GROUP BY {col_uf}",
    "ORDER BY quantidade_trechos DESC;",
    "\"\"\"",
    "df_p6 = consultar(sql_p6)",
    "display(df_p6)",
    "",
    "fig_p6 = px.bar(",
    "    df_p6, x='uf_destino', y='quantidade_trechos',",
    "    title='Frequência de Trechos por UF de Destino',",
    "    labels={'quantidade_trechos': 'Nº de Trechos', 'uf_destino': 'UF Destino'},",
    "    text_auto='d', color_discrete_sequence=['#17becf']",
    ")",
    "fig_p6.update_layout(",
    "    template='plotly_white', ",
    "    title_font_family='Arial Black',",
    "    xaxis=dict(tickangle=-45),",
    "    margin=dict(l=50, r=40, t=60, b=100)",
    ")",
    "fig_p6.update_traces(textposition='outside')",
    "fig_p6.show()",
    "salvar_grafico(fig_p6, '6_uf_destino_frequencia.png')"
])

# --- CÉLULA 9: PERGUNTA 7 ---
add_markdown(["## 7. Qual órgão pagou mais no total?"])
add_code([
    "sql_p7 = \"\"\"",
    "SELECT v.nome_orgao_superior, SUM(p.valor) AS total_pago",
    "FROM silver_pagamento p",
    "INNER JOIN silver_viagem v ON p.id_viagem = v.id_viagem",
    "GROUP BY v.nome_orgao_superior",
    "ORDER BY total_pago DESC",
    "LIMIT 5;",
    "\"\"\"",
    "df_p7 = consultar(sql_p7)",
    "display(df_p7)",
    "",
    "fig_p7 = px.bar(",
    "    df_p7, x='total_pago', y='nome_orgao_superior', orientation='h',",
    "    title='Top Órgãos por Total Efetivamente Pago',",
    "    labels={'total_pago': 'Total Pago (R$)', 'nome_orgao_superior': 'Órgão'},",
    "    text_auto='.2f', color_discrete_sequence=['#ff7f0e']",
    ")",
    "fig_p7.update_layout(",
    "    template='plotly_white', ",
    "    title_font_family='Arial Black', ",
    "    yaxis={'categoryorder': 'total ascending'},",
    "    margin=dict(l=200, r=40, t=60, b=60),",
    "    height=500",
    ")",
    "fig_p7.show()",
    "salvar_grafico(fig_p7, '7_orgao_que_mais_pagou.png')"
])

# --- CÉLULA 10: FECHAMENTO ---
add_code([
    "conexao.close()",
    "print('Análise das 7 questões finalizada e salva com sucesso!')"
])

# Grava nas duas pastas encontradas no comando tree
for caminho_saida in ["3_analise.ipynb", "scripts/3_analise.ipynb"]:
    try:
        with open(caminho_saida, "w", encoding="utf-8") as f:
            json.dump(notebook_data, f, indent=2, ensure_ascii=False)
        print(f"Notebook gerado com sucesso em: {caminho_saida}")
    except FileNotFoundError:
        pass