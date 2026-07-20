USE transparencia;

-- ============================================================================
-- 1. MODELAGEM DIMENSIONAL (STAR SCHEMA)
-- ============================================================================

-- Dimensão Órgão
DROP TABLE IF EXISTS dim_orgao;
CREATE TABLE dim_orgao (
    sk_orgao INT AUTO_INCREMENT PRIMARY KEY,
    cod_orgao_superior VARCHAR(50),
    nome_orgao_superior VARCHAR(255) NOT NULL,
    codigo_orgao_solicitante VARCHAR(50),
    nome_orgao_solicitante VARCHAR(255),
    CONSTRAINT uk_orgao UNIQUE (cod_orgao_superior, codigo_orgao_solicitante)
);

INSERT IGNORE INTO dim_orgao (cod_orgao_superior, nome_orgao_superior, codigo_orgao_solicitante, nome_orgao_solicitante)
SELECT DISTINCT 
    cod_orgao_superior, 
    nome_orgao_superior, 
    codigo_orgao_solicitante, 
    nome_orgao_solicitante
FROM silver_viagem
WHERE nome_orgao_superior IS NOT NULL;

-- Tabela Fato Viagens
DROP TABLE IF EXISTS fato_viagem;
CREATE TABLE fato_viagem (
    id_viagem VARCHAR(50) PRIMARY KEY,
    sk_orgao INT,
    data_inicio DATE,
    data_fim DATE,
    duracao_dias INT,
    situacao VARCHAR(100),
    valor_diarias DECIMAL(10,2),
    valor_passagens DECIMAL(10,2),
    valor_devolucao DECIMAL(10,2),
    valor_outros_gastos DECIMAL(10,2),
    valor_total DECIMAL(12,2),
    CONSTRAINT fk_fato_orgao FOREIGN KEY (sk_orgao) REFERENCES dim_orgao(sk_orgao)
);

INSERT INTO fato_viagem (
    id_viagem, sk_orgao, data_inicio, data_fim, duracao_dias, 
    situacao, valor_diarias, valor_passagens, valor_devolucao, valor_outros_gastos, valor_total
)
SELECT 
    v.id_viagem,
    o.sk_orgao,
    v.data_inicio,
    v.data_fim,
    v.duracao_dias,
    v.situacao,
    v.valor_diarias,
    v.valor_passagens,
    v.valor_devolucao,
    v.valor_outros_gastos,
    COALESCE(v.valor_total, (v.valor_diarias + v.valor_passagens + v.valor_outros_gastos - v.valor_devolucao)) AS valor_total
FROM silver_viagem v
LEFT JOIN dim_orgao o 
    ON COALESCE(v.cod_orgao_superior, '') = COALESCE(o.cod_orgao_superior, '')
   AND COALESCE(v.codigo_orgao_solicitante, '') = COALESCE(o.codigo_orgao_solicitante, '');


-- ============================================================================
-- 2. VIEWS ANALÍTICAS GOLD (PARA RESPONDER ÀS PERGUNTAS DE NEGÓCIO)
-- ============================================================================

-- Q1: Os 5 órgãos com maior custo total
CREATE OR REPLACE VIEW gold_q1_top5_orgaos_custo AS
SELECT 
    o.nome_orgao_superior,
    SUM(f.valor_total) AS custo_total
FROM fato_viagem f
JOIN dim_orgao o ON f.sk_orgao = o.sk_orgao
GROUP BY o.nome_orgao_superior
ORDER BY custo_total DESC
LIMIT 5;

-- Q2: Os 3 destinos com maior custo médio por viagem
CREATE OR REPLACE VIEW gold_q2_top3_destinos_custo_medio AS
SELECT 
    t.destino_cidade,
    t.destino_uf,
    AVG(f.valor_total) AS custo_medio_por_viagem,
    COUNT(DISTINCT f.id_viagem) AS quantidade_viagens
FROM silver_trecho t
JOIN fato_viagem f ON t.id_viagem = f.id_viagem
WHERE t.destino_cidade IS NOT NULL AND t.destino_cidade != ''
GROUP BY t.destino_cidade, t.destino_uf
HAVING quantidade_viagens >= 3  
ORDER BY custo_medio_por_viagem DESC
LIMIT 3;

-- Q3: A viagem de maior duração e seu custo total
CREATE OR REPLACE VIEW gold_q3_viagem_maior_duracao AS
SELECT 
    f.id_viagem,
    o.nome_orgao_superior,
    f.duracao_dias,
    f.valor_total AS custo_total,
    f.data_inicio,
    f.data_fim
FROM fato_viagem f
JOIN dim_orgao o ON f.sk_orgao = o.sk_orgao
WHERE f.duracao_dias IS NOT NULL
ORDER BY f.duracao_dias DESC, f.valor_total DESC
LIMIT 1;

-- Q4: Qual o tipo de pagamento com maior valor médio?
CREATE OR REPLACE VIEW gold_q4_tipo_pagamento_maior_medio AS
SELECT 
    tipo_pagamento,
    AVG(valor) AS valor_medio_pagamento,
    COUNT(*) AS total_transacoes
FROM silver_pagamento
WHERE tipo_pagamento IS NOT NULL AND tipo_pagamento != ''
GROUP BY tipo_pagamento
ORDER BY valor_medio_pagamento DESC
LIMIT 1;

-- Q5: Qual o meio de transporte mais usado nos trechos?
CREATE OR REPLACE VIEW gold_q5_meio_transporte_mais_usado AS
SELECT 
    meio_transporte,
    COUNT(*) AS total_trechos
FROM silver_trecho
WHERE meio_transporte IS NOT NULL AND meio_transporte != ''
GROUP BY meio_transporte
ORDER BY total_trechos DESC
LIMIT 1;

-- Q6: Qual UF de destino aparece em mais trechos?
CREATE OR REPLACE VIEW gold_q6_uf_destino_mais_frequente AS
SELECT 
    destino_uf AS uf_destino,
    COUNT(*) AS total_trechos
FROM silver_trecho
WHERE destino_uf IS NOT NULL AND destino_uf != ''
GROUP BY destino_uf
ORDER BY total_trechos DESC
LIMIT 1;

-- Q7: Qual órgão pagou mais no total?
CREATE OR REPLACE VIEW gold_q7_orgao_pagou_mais_total AS
SELECT 
    nome_orgao_pagador,
    SUM(valor) AS valor_total_pago
FROM silver_pagamento
WHERE nome_orgao_pagador IS NOT NULL AND nome_orgao_pagador != ''
GROUP BY nome_orgao_pagador
ORDER BY valor_total_pago DESC
LIMIT 1;