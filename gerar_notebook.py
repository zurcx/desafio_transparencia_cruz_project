"""
Módulo de Geração e Automação Visual de Analíticos de Viagens.

Este script executa consultas analíticas no banco de dados relacional MySQL,
trata e mapeia dinamicamente os dados, aplica padrões rígidos de 
design de alta legibilidade (DataViz) e exporta os ativos em alta resolução.
"""

import os
import sys
import logging
from typing import Dict, Any, List, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# --- CONFIGURAÇÃO DE LOGS ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("AnalyticsEngine")


class PipelineAnalyticsViagens:
    """Orquestrador do Pipeline de Extração, Visualização e Exportação de Viagens."""

    def __init__(self, largura_exportacao: int = 1200, altura_exportacao: int = 650):
        self.largura_exportacao = largura_exportacao
        self.altura_exportacao = altura_exportacao
        
        # Define renderizador estático para compatibilidade técnica
        pio.renderers.default = "png"
        
        # Configuração de diretórios do projeto
        self.diretorio_raiz = os.path.abspath(os.getcwd())
        self.pasta_graficos = os.path.join(self.diretorio_raiz, "graficos_png")
        os.makedirs(self.pasta_graficos, exist_ok=True)
        
        self._inicializar_dependencias_banco()
        self.conexao = self._conectar_banco()

    def _inicializar_dependencias_banco(self) -> None:
        """Garante a inclusão dos caminhos do módulo de banco de dados no sistema."""
        pasta_mysql = os.path.join(self.diretorio_raiz, "_MySQL")
        pasta_mysql_alt = os.path.abspath(os.path.join(self.diretorio_raiz, "..", "_MySQL"))

        for caminho in [self.diretorio_raiz, pasta_mysql, pasta_mysql_alt]:
            if os.path.exists(caminho) and caminho not in sys.path:
                sys.path.append(caminho)

    def _conectar_banco(self) -> Any:
        """Estabelece conexão segura com o módulo de banco de dados."""
        try:
            import banco
            logger.info("Módulo de conexão 'banco' importado com sucesso.")
            return banco.conectar()
        except ModuleNotFoundError:
            logger.error("Falha crítica: Módulo 'banco.py' não encontrado nos caminhos especificados.")
            raise

    def consultar(self, sql: str) -> pd.DataFrame:
        """Executa consultas SQL estruturadas e retorna um DataFrame do Pandas."""
        try:
            return pd.read_sql(sql, self.conexao)
        except Exception as err:
            logger.error(f"Erro ao executar a consulta SQL: {err}")
            raise

    def aplicar_design_executivo(
        self, 
        fig: go.Figure, 
        titulo: str, 
        eixo_x_title: str, 
        eixo_y_title: str
    ) -> go.Figure:
        """
        Aplica o padrão executivo de Data Visualization (Alto contraste, 
        tema plotly_white e eliminação de truncamento de texto).
        """
        fig.update_layout(
            template="plotly_white",
            title={
                "text": f"<b>{titulo}</b>",
                "x": 0.5,
                "xanchor": "center",
                "font": {"size": 18, "color": "#111111"}
            },
            font=dict(size=12, color="#222222"),
            xaxis=dict(
                title=f"<b>{eixo_x_title}</b>",
                showgrid=True,
                gridcolor="#E5E5E5",
                tickangle=-25
            ),
            yaxis=dict(
                title=f"<b>{eixo_y_title}</b>",
                showgrid=True,
                gridcolor="#E5E5E5"
            ),
            margin=dict(l=140, r=50, t=80, b=120),
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        return fig

    def salvar_grafico(self, fig: go.Figure, nome_arquivo: str) -> None:
        """Persiste o gráfico estático em alta definição na pasta de destino."""
        caminho_completo = os.path.join(self.pasta_graficos, nome_arquivo)
        try:
            fig.write_image(
                caminho_completo, 
                scale=2, 
                width=self.largura_exportacao, 
                height=self.altura_exportacao
            )
            logger.info(f"Ativo visual salvo em: {caminho_completo}")
        except Exception as err:
            logger.error(f"Falha ao salvar a imagem '{nome_arquivo}'. Certifique-se de ter a biblioteca 'kaleido' instalada. Erro: {err}")

    def mapear_colunas_trecho(self) -> Dict[str, str]:
        """Verifica dinamicamente a estrutura de schema da tabela 'silver_trecho'."""
        df_sample = self.consultar("SELECT * FROM silver_trecho LIMIT 1")
        colunas_disponiveis = list(df_sample.columns)

        col_cidade = "cidade_destino"
        for c in ["cidade_destino", "destino", "destino_cidade", "cidade"]:
            if c in colunas_disponiveis:
                col_cidade = c
                break

        col_uf = "uf_destino"
        for u in ["uf_destino", "uf", "destino_uf", "estado_destino"]:
            if u in colunas_disponiveis:
                col_uf = u
                break

        logger.info(f"Schema resolvido para 'silver_trecho' -> Cidade: '{col_cidade}', UF: '{col_uf}'")
        return {"cidade": col_cidade, "uf": col_uf}

    # --- PROCESSAMENTO DAS PERGUNTAS E ANÁLISES EXECUTIVE-LEVEL ---

    def gerar_analise_custo_orgaos((self) -> None:
        """Gera a análise top 5 órgãos superiores por custo total."""
        sql = """
            SELECT nome_orgao_superior, SUM(custo_total) as custo_total
            FROM silver_viagem
            GROUP BY nome_orgao_superior
            ORDER BY custo_total DESC
            LIMIT 5
        """
        df = self.consultar(sql).sort_values(by="custo_total", ascending=True)

        fig = px.bar(
            df,
            x="custo_total",
            y="nome_orgao_superior",
            orientation="h",
            text_auto=".2s",
            color_discrete_sequence=["#0055A5"]
        )
        fig.update_traces(textposition="outside", textfont=dict(size=12, color="#000000"))
        fig = self.aplicar_design_executivo(
            fig,
            titulo="Top 5 Órgãos com Maior Custo Total",
            eixo_x_title="Custo Total (R$)",
            eixo_y_title="Órgão Superior"
        )
        self.salvar_grafico(fig, "q1_orgaos_maior_custo.png")

    def gerar_analise_cidades_visitadas(self, col_cidade: str) -> None:
        """Gera a análise top 10 cidades de destino mais visitadas."""
        sql = f"""
            SELECT {col_cidade} AS cidade, COUNT(*) AS total_viagens
            FROM silver_trecho
            GROUP BY {col_cidade}
            ORDER BY total_viagens DESC
            LIMIT 10
        """
        df = self.consultar(sql).sort_values(by="total_viagens", ascending=True)

        fig = px.bar(
            df,
            x="total_viagens",
            y="cidade",
            orientation="h",
            text_auto=True,
            color_discrete_sequence=["#2E7D32"]
        )
        fig.update_traces(textposition="outside", textfont=dict(size=12, color="#000000"))
        fig = self.aplicar_design_executivo(
            fig,
            titulo="Top 10 Cidades de Destino Mais Visitadas",
            eixo_x_title="Quantidade de Viagens",
            eixo_y_title="Cidade"
        )
        self.salvar_grafico(fig, "q2_cidades_mais_visitadas.png")

    def gerar_analise_sazonalidade_previsao(self) -> None:
        """Gera a evolução histórica e projeção de custos com base na tendência temporal."""
        sql = """
            SELECT 
                DATE_FORMAT(data_inicio, '%Y-%m-01') AS mes,
                SUM(custo_total) AS custo_total
            FROM silver_viagem
            WHERE data_inicio IS NOT NULL
            GROUP BY DATE_FORMAT(data_inicio, '%Y-%m-01')
            ORDER BY mes ASC
        """
        df = self.consultar(sql)
        df["mes"] = pd.to_datetime(df["mes"])
        df["media_movel_3m"] = df["custo_total"].rolling(window=3, min_periods=1).mean()

        # Cálculo de Projeção Preditiva (Simplificada)
        ultimos_meses = df.tail(3)
        taxa_crescimento = ultimos_meses["custo_total"].pct_change().mean()
        taxa_crescimento = taxa_crescimento if not pd.isna(taxa_crescimento) else 0.02

        ultimo_valor = df["custo_total"].iloc[-1]
        ultima_data = df["mes"].iloc[-1]

        datas_futuras = [ultima_data + pd.DateOffset(months=i) for i in range(1, 4)]
        valores_projetados = []
        valor_atual = ultimo_valor

        for _ in range(3):
            valor_atual *= (1 + taxa_crescimento)
            valores_projetados.append(valor_atual)u

        df_projecao = pd.DataFrame({"mes": datas_futuras, "custo_total": valores_projetados, "tipo": "Projeção"})
        df["tipo"] = "Histórico"
        df_completo = pd.concat([df[["mes", "custo_total", "tipo"]], df_projecao], ignore_index=True)

        # Renderização do Gráfico Preditivo
        fig = go.Figure()
        df_hist = df_completo[df_completo["tipo"] == "Histórico"]
        
        fig.add_trace(go.Scatter(
            x=df_hist["mes"], y=df_hist["custo_total"],
            mode="lines+markers", name="Gasto Real (R$)",
            line=dict(color="#0055A5", width=3)
        ))
        fig.add_trace(go.Scatter(
            x=df["mes"], y=df["media_movel_3m"],
            mode="lines", name="Tendência (Média Móvel 3M)",
            line=dict(color="#FF9800", width=2, dash="dash")
        ))
        
        df_proj = df_completo[df_completo["tipo"] == "Projeção"]
        df_proj_concat = pd.concat([df_hist.tail(1), df_proj])
        
        fig.add_trace(go.Scatter(
            x=df_proj_concat["mes"], y=df_proj_concat["custo_total"],
            mode="lines+markers", name="Projeção Preditiva",
            line=dict(color="#E53935", width=3, dash="dot")
        ))

        fig.update_layout(
            template="plotly_white",
            title={"text": "<b>Evolução Histórica e Previsão de Gastos com Viagens</b>", "x": 0.5, "xanchor": "center"},
            xaxis=dict(title="<b>Período (Mês/Ano)</b>", showgrid=True, gridcolor="#E5E5E5"),
            yaxis=dict(title="<b>Custo Total (R$)</b>", showgrid=True, gridcolor="#E5E5E5"),
            margin=dict(l=100, r=50, t=80, b=80),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        self.salvar_grafico(fig, "q3_sazonalidade_previsao.png")

    def executar_pipeline_completo(self) -> None:
        """Executa sequencialmente o pipeline analítico."""
        logger.info("Iniciando Pipeline Executivo de Analíticos de Viagens...")
        
        mapeamento = self.mapear_colunas_trecho()
        
        logger.info("Processando Pergunta 1: Top órgãos por custo...")
        self.gerar_analise_custo_orgaos()
        
        logger.info("Processando Pergunta 2: Destinos mais visitados...")
        self.gerar_analise_cidades_visitadas(col_cidade=mapeamento["cidade"])
        
        logger.info("Processando Pergunta 3: Análise temporal e preditiva...")
        self.gerar_analise_sazonalidade_previsao()
        
        logger.info("Pipeline executado com sucesso! Todos os ativos foram gerados.")


# --- PONTO DE ENTRADA EXECUTIVO ---
if __name__ == "__main__":
    try:
        pipeline = PipelineAnalyticsViagens()
        pipeline.executar_pipeline_completo()
    except Exception as e:
        logger.critical(f"Execução do pipeline interrompida por erro fatal: {e}")