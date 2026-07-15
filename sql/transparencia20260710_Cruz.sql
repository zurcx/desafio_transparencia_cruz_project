

DROP DATABASE IF EXISTS transparencia;
CREATE DATABASE transparencia
  CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;
USE transparencia;

DROP table raw_viagem;
CREATE TABLE raw_viagem (
    id_viagem VARCHAR(50),
    num_proposta VARCHAR(50),
    situacao VARCHAR(100),
    viagem_urgente VARCHAR(10),
    justificativa_urgencia_viagem VARCHAR(4000),
    cod_orgao_superior VARCHAR(50),
    nome_orgao_superior VARCHAR(255),
    codigo_orgao_solicitante VARCHAR(50),
    nome_orgao_solicitante VARCHAR(255),
    cpf_viajante VARCHAR(20),
    nome_viajante VARCHAR(255),
    cargo VARCHAR(255),
    funcao VARCHAR(255),
    descricao_funcao VARCHAR(255),
    data_inicio VARCHAR(50),
    data_fim VARCHAR(50),
    destinos VARCHAR(4000),
    motivo VARCHAR(4000),
    valor_diarias VARCHAR(50),
    valor_passagens VARCHAR(50),
    valor_devolucao VARCHAR(50),
    valor_outros_gastos VARCHAR(50)
);


drop table raw_passagem;
CREATE TABLE raw_passagem (
    id_viagem VARCHAR(50),
    num_proposta VARCHAR(50),
    meio_transporte VARCHAR(100),
    pais_origem_ida VARCHAR(100),
    uf_origem_ida VARCHAR(100),
    cidade_origem_ida VARCHAR(150),
    pais_destino_ida VARCHAR(100),
    uf_destino_ida VARCHAR(100),
    cidade_destino_ida VARCHAR(150),
    pais_origem_volta VARCHAR(100),
    uf_origem_volta VARCHAR(100),
    cidade_origem_volta VARCHAR(150),
    pais_destino_volta VARCHAR(100),
    uf_destino_volta VARCHAR(100),
    cidade_destino_volta VARCHAR(150),
    valor_passagem VARCHAR(50),
    taxa_servico VARCHAR(50),
    data_emissao VARCHAR(50),
    hora_emissao VARCHAR(50)
);


DROP table raw_trecho;
CREATE TABLE raw_trecho (
    id_viagem VARCHAR(50),
    num_proposta VARCHAR(50),
    sequencia_trecho VARCHAR(50),
    origem_data VARCHAR(50),
    origem_pais VARCHAR(100),
    origem_uf VARCHAR(100),
    origem_cidade VARCHAR(150),
    destino_data VARCHAR(50),
    destino_pais VARCHAR(100),
    destino_uf VARCHAR(100),
    destino_cidade VARCHAR(150),
    meio_transporte VARCHAR(100),
    numero_diarias VARCHAR(50),
    missao VARCHAR(100)
);

CREATE TABLE raw_pagamento (
    id_viagem VARCHAR(50),
    num_proposta VARCHAR(50),
    cod_orgao_superior VARCHAR(50),
    nome_orgao_superior VARCHAR(255),
    codigo_orgao_pagador VARCHAR(50),
    nome_orgao_pagador VARCHAR(255),
    codigo_unidade_gestora_pagadora VARCHAR(50),
    nome_unidade_gestora_pagadora VARCHAR(255),
    tipo_pagamento VARCHAR(100),
    valor VARCHAR(50)
);

CREATE TABLE silver_viagem (
    id_viagem VARCHAR(50) NOT NULL,
    num_proposta VARCHAR(50),
    situacao VARCHAR(100),
    viagem_urgente VARCHAR(10),
    justificativa_urgencia_viagem VARCHAR(4000),
    cod_orgao_superior VARCHAR(50),
    nome_orgao_superior VARCHAR(255) NOT NULL,
    codigo_orgao_solicitante VARCHAR(50),
    nome_orgao_solicitante VARCHAR(255),
    cpf_viajante VARCHAR(20),
    nome_viajante VARCHAR(255),
    cargo VARCHAR(255),
    funcao VARCHAR(255),
    descricao_funcao VARCHAR(255),
    data_inicio DATE,
    data_fim DATE,
    destinos VARCHAR(4000),
    motivo VARCHAR(4000),
    valor_diarias DECIMAL(10,2),
    valor_passagens DECIMAL(10,2),
    valor_devolucao DECIMAL(10,2),
    valor_outros_gastos DECIMAL(10,2),
    valor_total DECIMAL(12,2),
    duracao_dias INT,
    CONSTRAINT pk_silver_viagem PRIMARY KEY (id_viagem),
    CONSTRAINT chk_valor_diarias CHECK (valor_diarias >= 0)
);

CREATE TABLE silver_passagem (
    id_passagem INT NOT NULL AUTO_INCREMENT,
    id_viagem VARCHAR(50) NOT NULL,
    num_proposta VARCHAR(50),
    meio_transporte VARCHAR(100),
    pais_origem_ida VARCHAR(100),
    uf_origem_ida VARCHAR(100),
    cidade_origem_ida VARCHAR(150),
    pais_destino_ida VARCHAR(100),
    uf_destino_ida VARCHAR(100),
    cidade_destino_ida VARCHAR(150),
    pais_origem_volta VARCHAR(100),
    uf_origem_volta VARCHAR(100),
    cidade_origem_volta VARCHAR(150),
    pais_destino_volta VARCHAR(100),
    uf_destino_volta VARCHAR(100),
    cidade_destino_volta VARCHAR(150),
    valor_passagem DECIMAL(10,2),
    taxa_servico DECIMAL(10,2),
    data_emissao DATE,
    hora_emissao VARCHAR(50),
    CONSTRAINT pk_silver_passagem PRIMARY KEY (id_passagem),
    CONSTRAINT fk_passagem_viagem FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem),
    CONSTRAINT chk_valor_passagem CHECK (valor_passagem >= 0),
    CONSTRAINT chk_taxa_servico CHECK (taxa_servico >= 0)
);

CREATE TABLE silver_pagamento (
    id_pagamento INT NOT NULL AUTO_INCREMENT,
    id_viagem VARCHAR(50) NOT NULL,
    num_proposta VARCHAR(50),
    cod_orgao_superior VARCHAR(50),
    nome_orgao_superior VARCHAR(255),
    codigo_orgao_pagador VARCHAR(50),
    nome_orgao_pagador VARCHAR(255),
    codigo_unidade_gestora_pagadora VARCHAR(50),
    nome_unidade_gestora_pagadora VARCHAR(255),
    tipo_pagamento VARCHAR(100) NOT NULL,
    valor DECIMAL(10,2),
    CONSTRAINT pk_silver_pagamento PRIMARY KEY (id_pagamento),
    CONSTRAINT fk_pagamento_viagem FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem),
    CONSTRAINT chk_valor_pagamento CHECK (valor >= 0)
);

CREATE TABLE silver_trecho (
    id_trecho INT NOT NULL AUTO_INCREMENT,
    id_viagem VARCHAR(50) NOT NULL,
    num_proposta VARCHAR(50),
    sequencia_trecho INT,
    origem_data DATE,
    origem_pais VARCHAR(100),
    origem_uf VARCHAR(100),
    origem_cidade VARCHAR(150),
    destino_data DATE,
    destino_pais VARCHAR(100),
    destino_uf VARCHAR(100),
    destino_cidade VARCHAR(150),
    meio_transporte VARCHAR(100),
    numero_diarias DECIMAL(10,2),
    missao VARCHAR(100),
    CONSTRAINT pk_silver_trecho PRIMARY KEY (id_trecho),
    CONSTRAINT fk_trecho_viagem FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem),
    CONSTRAINT chk_numero_diarias CHECK (numero_diarias >= 0)
);

show tables;