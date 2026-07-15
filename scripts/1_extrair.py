import zipfile
import gdown

import pandas as pd

import config
import banco

"""
1_extrair.py  -  FASE 1: Extracao e Camada RAW
----------------------------------------------
Passo a passo simples:
  1. Localiza o arquivo cafeteria.zip que foi baixado para a pasta data/.
  2. Le os 2 CSVs de dentro do .zip (vendas, itens).
  3. Insere os dados, SEM nenhuma alteracao, nas 2 tabelas RAW do MySQL.

ANTES DE RODAR: baixe o "cafeteria.zip" (link do Drive da escola) e coloque-o
dentro da pasta "data/" deste projeto:
    data/cafeteria.zip

A camada RAW e uma copia fiel do CSV: todas as colunas sao texto (VARCHAR).
DROP TABLE raw_viagem;
As tabelas ja foram criadas pelo script 0_criar_banco.txt.
"""


# ---------------------------------------------------------------------------
# Passo 1 - Localizar o arquivo .zip na pasta data/
# ---------------------------------------------------------------------------
def download_zip():
    """Aponta para o viagens.zip que voce colocou na pasta data/."""
    config.PASTA_DADOS.mkdir(exist_ok=True)
    destino = config.PASTA_DADOS / "viagens.zip"

    if destino.exists():
        print("[1/3] O arquivo ja foi criado antes - pulando o download")
    else:
        print("[1/3] Baixando o arquivo do Google Drive... ")
        gdown.download(id=config.DRIVE_FILE_ID, output=str(destino))
    return destino


def loading_csv(conexao, zip_aberto, nome_csv, tabela):
    banco.executar(conexao, f"TRUNCATE TABLE {tabela}")
    total = 0
    with zip_aberto.open(nome_csv) as arquivo:
        pedacos = pd.read_csv(
            arquivo,
            sep=";",
            encoding="latin-1",
            dtype=str,
            keep_default_na=False,
            chunksize=config.TAMANHO_BLOCO,
        )

        for pedaco in pedacos:
            linhas = pedaco.values.tolist()
            # um "%s" para cada coluna do CSV
            marcadores = ", ".join(["%s"] * len(pedaco.columns))
            comando = f"INSERT INTO {tabela} VALUES ({marcadores})"
            banco.inserir_em_lote(conexao, comando, linhas)
            total += len(linhas)

    print("      ->", total, "linhas em", tabela)


def main():
    print("=== FASE 1: EXTRACAO + CAMADA RAW ===JK")
    try:
        conexao = banco.conectar()

        caminho_zip = download_zip()
        print("[2/3] Abrindo o arquivo zip...")
        print("[3/3] Carregando as 2 tabelas RAW...")
        with zipfile.ZipFile(caminho_zip) as zip_aberto:
            for arquivo in config.ARQUIVOS.values():
                loading_csv(conexao, zip_aberto, arquivo["csv"], arquivo["tabela_raw"])

        conexao.close()
        print("=== Camada RAW concluida com sucesso! ===")
    except Exception as erro:
        print("[ERRO] Algo deu errado:", erro)
        raise


if __name__ == "__main__":
    main()
