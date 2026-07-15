"""
2_transformar.py  -  FASE 2: Transformacao e Camada SILVER
----------------------------------------------------------
Pega os dados "sujos" da camada RAW (tudo texto) e preenche as tabelas SILVER
(ja criadas, com PK/FK, pelo 0_criar_banco.txt) com os dados limpos e tipados.

A receita e simples: rodamos alguns comandos SQL, em ordem.
  1. Esvaziamos as tabelas SILVER (para nao duplicar se rodar de novo).
  2. Copiamos da RAW para a SILVER, convertendo os tipos.
  3. Calculamos as colunas derivadas (valor_total, prazo_dias, subtotal).

------------------------------------------------------------------------------
COMO CONVERTEMOS O TEXTO DA CAMADA RAW (esse padrao se repete no SQL abaixo):

  - Dinheiro: "1.234,50" (texto)  ->  1234.50 (numero DECIMAL)
      tira o ponto de milhar, troca a virgula por ponto e faz CAST:
      CAST(REPLACE(REPLACE(NULLIF(TRIM(coluna), ''), '.', ''), ',', '.') AS DECIMAL(10,2))

  - Data: "30/06/2025" (texto)  ->  2025-06-30 (tipo DATE)
      STR_TO_DATE(NULLIF(TRIM(coluna), ''), '%d/%m/%Y')

  Obs.: NULLIF(coluna, '') transforma um campo vazio em NULL (vazio no banco).
------------------------------------------------------------------------------
"""

import banco


# 1) Esvaziar as tabelas SILVER (idempotencia).
#    A ordem importa por causa da FK: apagamos a filha (itens) antes da principal.


LIMPAR_SILVER = [
    "DELETE FROM silver_pagamento",
    "DELETE FROM silver_passagem",
    "DELETE FROM silver_trecho",
    "DELETE FROM silver_viagem",
]

# 2) Copiar RAW -> SILVER convertendo os tipos
SQL_VIAGEM = """
INSERT INTO silver_viagem (
    id_viagem, num_proposta, situacao, viagem_urgente, justificativa_urgencia_viagem,
    cod_orgao_superior, nome_orgao_superior, codigo_orgao_solicitante, nome_orgao_solicitante,
    cpf_viajante, nome_viajante, cargo, funcao, descricao_funcao, data_inicio, data_fim,
    destinos, motivo, valor_diarias, valor_passagens, valor_devolucao, valor_outros_gastos,
    valor_total, duracao_dias
)
SELECT 
    NULLIF(TRIM(id_viagem), ''), 
    NULLIF(TRIM(num_proposta), ''), 
    NULLIF(TRIM(situacao), ''), 
    NULLIF(TRIM(viagem_urgente), ''), 
    NULLIF(TRIM(justificativa_urgencia_viagem), ''),
    NULLIF(TRIM(cod_orgao_superior), ''), 
    COALESCE(NULLIF(TRIM(nome_orgao_superior), ''), 'NÃO INFORMADO'), 
    NULLIF(TRIM(codigo_orgao_solicitante), ''), 
    NULLIF(TRIM(nome_orgao_solicitante), ''),
    NULLIF(TRIM(cpf_viajante), ''), 
    NULLIF(TRIM(nome_viajante), ''), 
    NULLIF(TRIM(cargo), ''), 
    NULLIF(TRIM(funcao), ''), 
    NULLIF(TRIM(descricao_funcao), ''),
    CASE WHEN TRIM(data_inicio) = '' OR data_inicio IS NULL THEN NULL ELSE STR_TO_DATE(TRIM(data_inicio), '%d/%m/%Y') END, 
    CASE WHEN TRIM(data_fim) = '' OR data_fim IS NULL THEN NULL ELSE STR_TO_DATE(TRIM(data_fim), '%d/%m/%Y') END,
    NULLIF(TRIM(destinos), ''), 
    NULLIF(TRIM(motivo), ''),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_diarias), ''), '.', ''), ',', '.') AS DECIMAL(10,2)),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_passagens), ''), '.', ''), ',', '.') AS DECIMAL(10,2)),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_devolucao), ''), '.', ''), ',', '.') AS DECIMAL(10,2)),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_outros_gastos), ''), '.', ''), ',', '.') AS DECIMAL(10,2)),
    0.00,  
    0      
FROM raw_viagem;
"""

SQL_PASSAGEM = """
INSERT INTO silver_passagem (
    id_viagem, num_proposta, meio_transporte, pais_origem_ida, uf_origem_ida, cidade_origem_ida,
    pais_destino_ida, uf_destino_ida, cidade_destino_ida, pais_origem_volta, uf_origem_volta,
    cidade_origem_volta, pais_destino_volta, uf_destino_volta, cidade_destino_volta,
    valor_passagem, taxa_servico, data_emissao, hora_emissao
)
SELECT 
    NULLIF(TRIM(id_viagem), ''), 
    NULLIF(TRIM(num_proposta), ''), 
    NULLIF(TRIM(meio_transporte), ''), 
    NULLIF(TRIM(pais_origem_ida), ''), 
    NULLIF(TRIM(uf_origem_ida), ''), 
    NULLIF(TRIM(cidade_origem_ida), ''),
    NULLIF(TRIM(pais_destino_ida), ''), 
    NULLIF(TRIM(uf_destino_ida), ''), 
    NULLIF(TRIM(cidade_destino_ida), ''), 
    NULLIF(TRIM(pais_origem_volta), ''), 
    NULLIF(TRIM(uf_origem_volta), ''),
    NULLIF(TRIM(cidade_origem_volta), ''), 
    NULLIF(TRIM(pais_destino_volta), ''), 
    NULLIF(TRIM(uf_destino_volta), ''), 
    NULLIF(TRIM(cidade_destino_volta), ''),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_passagem), ''), '.', ''), ',', '.') AS DECIMAL(10,2)),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(taxa_servico), ''), '.', ''), ',', '.') AS DECIMAL(10,2)),
    CASE WHEN TRIM(data_emissao) = '' OR data_emissao IS NULL THEN NULL ELSE STR_TO_DATE(TRIM(data_emissao), '%d/%m/%Y') END,
    NULLIF(TRIM(hora_emissao), '')
FROM raw_passagem;
"""

SQL_PAGAMENTO = """
INSERT INTO silver_pagamento (
    id_viagem, num_proposta, cod_orgao_superior, nome_orgao_superior, codigo_orgao_pagador,
    nome_orgao_pagador, codigo_unidade_gestora_pagadora, nome_unidade_gestora_pagadora,
    tipo_pagamento, valor
)
SELECT 
    NULLIF(TRIM(id_viagem), ''), 
    NULLIF(TRIM(num_proposta), ''), 
    NULLIF(TRIM(cod_orgao_superior), ''), 
    NULLIF(TRIM(nome_orgao_superior), ''), 
    NULLIF(TRIM(codigo_orgao_pagador), ''),
    NULLIF(TRIM(nome_orgao_pagador), ''), 
    NULLIF(TRIM(codigo_unidade_gestora_pagadora), ''), 
    NULLIF(TRIM(nome_unidade_gestora_pagadora), ''),
    COALESCE(NULLIF(TRIM(tipo_pagamento), ''), 'NÃO INFORMADO'),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor), ''), '.', ''), ',', '.') AS DECIMAL(10,2))
FROM raw_pagamento;
"""

SQL_TRECHO = """
INSERT INTO silver_trecho (
    id_viagem, num_proposta, sequencia_trecho, origem_data, origem_pais, origem_uf,
    origem_cidade, destino_data, destino_pais, destino_uf, destino_cidade,
    meio_transporte, numero_diarias, missao
)
SELECT 
    NULLIF(TRIM(id_viagem), ''), 
    NULLIF(TRIM(num_proposta), ''), 
    CAST(NULLIF(TRIM(sequencia_trecho), '') AS UNSIGNED),
    CASE WHEN TRIM(origem_data) = '' OR origem_data IS NULL THEN NULL ELSE STR_TO_DATE(TRIM(origem_data), '%d/%m/%Y') END,
    NULLIF(TRIM(origem_pais), ''), 
    NULLIF(TRIM(origem_uf), ''), 
    NULLIF(TRIM(origem_cidade), ''),
    CASE WHEN TRIM(destino_data) = '' OR destino_data IS NULL THEN NULL ELSE STR_TO_DATE(TRIM(destino_data), '%d/%m/%Y') END,
    NULLIF(TRIM(destino_pais), ''), 
    NULLIF(TRIM(destino_uf), ''), 
    NULLIF(TRIM(destino_cidade), ''),
    NULLIF(TRIM(meio_transporte), ''),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(numero_diarias), ''), '.', ''), ',', '.') AS DECIMAL(10,2)),
    NULLIF(TRIM(missao), '')
FROM raw_trecho;
"""

# 3) Calcular as colunas derivadas via UPDATE
SQL_CALC_VIAGEM = """
UPDATE silver_viagem
SET valor_total = COALESCE(valor_diarias, 0) + COALESCE(valor_passagens, 0) + COALESCE(valor_outros_gastos, 0) - COALESCE(valor_devolucao, 0),
    duracao_dias = CASE WHEN data_fim IS NOT NULL AND data_inicio IS NOT NULL THEN DATEDIFF(data_fim, data_inicio) ELSE 0 END
"""


def main():
    print("=== FASE 2: TRANSFORMACAO + CAMADA SILVER ===")
    try:
        conexao = banco.conectar()

        print("[1/3] Esvaziando as tabelas SILVER...")
        for comando in LIMPAR_SILVER:
            banco.executar(conexao, comando)

        print("[2/3] Copiando e convertendo RAW -> SILVER...")
        banco.executar(conexao, SQL_VIAGEM)
        print("      silver_viagem    OK")
        banco.executar(conexao, SQL_PASSAGEM)
        print("      silver_passagem  OK")
        banco.executar(conexao, SQL_PAGAMENTO)
        print("      silver_pagamento OK")
        banco.executar(conexao, SQL_TRECHO)
        print("      silver_trecho    OK")

        print("[3/3] Calculando colunas valor_total e duracao_dias via UPDATE...")
        banco.executar(conexao, SQL_CALC_VIAGEM)
        print("      Campos calculados atualizados!")

        conexao.close()
        print("=== Camada SILVER concluida com sucesso! ===")
    except Exception as erro:
        print("[ERRO] Algo deu errado:", erro)
        raise


if __name__ == "__main__":
    main()
