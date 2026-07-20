# Análise Governamental: Gastos e Logística de Viagens Corporativas

Uma solução de Business Intelligence desenvolvida em Python e SQL para analisar a eficiência orçamentária, modais de transporte e comportamento de custos em viagens corporativas governamentais. 

Este repositório consolida dados brutos em uma camada refinada (Silver) para responder a perguntas críticas de auditoria e fornecer dashboards de alto nível para a tomada de decisão da diretoria.

---

## Perguntas de Negócio Respondidas

O projeto foi estruturado para resolver 7 frentes analíticas essenciais divididas em três pilares estratégicos:

### 1. Gestão Orçamentária e Maiores Custos
* **Concentração de Gastos por Órgão:** Identificação do Top 5 órgãos com maior custo total acumulado em viagens corporativas, isolando o órgão campeão absoluto de despesas e sua respectiva participação (%) no orçamento global.
* **Análise de Meios de Pagamento:** Avaliação de qual modalidade de pagamento apresenta o maior ticket médio por viagem para identificar gargalos ou preferências de faturamento.

### 2. Eficiência Logística e Destinos
* **Principais Polos de Destino:** Mapeamento do fluxo de viagens por Unidade da Federação (Top 10 UFs mais frequentadas) para entender a capilaridade das missões corporativas.
* **Matriz de Transporte:** Análise do market share dos meios de transporte mais utilizados nos trechos para avaliar a eficiência logística dos deslocamentos.

### 3. Casos Extremos e Ticket Médio
* **Destinos Mais Caros:** Identificação dos 3 destinos com os maiores custos médios por viagem, permitindo auditar trechos com valores fora da curva.
* **Auditoria de Anomalias (Recordes):** Isolamento e análise do caso extremo de maior duração em dias e seu respectivo impacto orçamentário.

# Análise de Custos e Deslocamentos de Viagens a Serviço

Este projeto realiza a extração, visualização e análise de dados sobre viagens a serviço e trechos percorridos a partir do banco de dados MySQL (`silver_viagem` e `silver_trecho`). O objetivo principal é gerar *insights* sobre o uso de recursos públicos e facilitar a tomada de decisão por meio de relatórios visuais limpos e legíveis.

---

## Técnicas e Tecnologias Utilizadas

### Tecnologias
* **Python 3.x:** Linguagem base do projeto.
* **Pandas:** Manipulação, estruturação e agregação de dados em DataFrames.
* **Plotly Express & Plotly I/O:** Construção dos gráficos interativos e aplicação de temas customizados.
* **Kaleido:** Engine para exportação de gráficos estáticos em formato PNG de alta definição.
* **MySQL:** Banco de dados relacional para armazenamento e consulta dos dados (`silver_viagem` e `silver_trecho`).

## Análises e Resultados (Camada Gold)

Abaixo estão apresentadas as respostas para as perguntas de negócio com base no processamento da camada Gold, acompanhadas das respetivas visualizações geradas.

---

### 1. Top 5 Órgãos por Custo Total
Quais órgãos públicos acumularam o maior valor total em gastos com viagens e diárias?

- Resposta: O Ministério da Educação lidera o volume de gastos, seguido pelo Ministério da Justiça e Segurança Pública e pelo Ministério da Defesa. Os valores consolidados refletem a grande escala operacional e o deslocamento contínuo de pessoal dessas pastas.

![Top 5 Órgãos por Custo Total](graficos_png/1_maior_custo_total_orgao.png)

---

### 2. Top 3 Destinos com Maior Custo Médio por Viagem
Quais destinos possuem a maior média de custo por ocorrência individual de viagem?

- Resposta: Destinos internacionais e missões diplomáticas no exterior apresentam os maiores custos médios por viagem, impulsionados pelos valores de passagens internacionais e conversão de diárias em moeda estrangeira (Dólar/Euro).

![Top 3 Destinos com Maior Custo Médio](graficos_png/2_custo_medio_destino.png)

---

### 3. Viagem de Maior Duração
Qual foi o registro de viagem corporativa com o maior número de dias contínuos e o seu custo total?

- Resposta: A viagem de maior duração registrada estendeu-se por um período contínuo voltado a missão oficial prolongada de assistência técnica/treinamento, totalizando um custo proporcional à duração das diárias concedidas.

*(Dado apresentado em tabela detalhada diretamente no notebook 3_analise.ipynb)*

---

### 4. Ticket Médio por Tipo de Pagamento
Qual a modalidade financeira ou tipo de pagamento que apresenta o maior valor médio transacionado?

- Resposta: Os pagamentos efetuados via Ordem de Bancária de Pagamento Direto e Concessão de Diárias possuem os maiores tickets médios por transação quando comparados ao ressarcimento individual de despesas menores.

![Valor Médio por Tipo de Pagamento](graficos_png/4_valor_medio_pagamento.png)

---

### 5. Distribuição dos Meios de Transporte
Qual é a proporção do uso dos meios de transporte nos trechos realizados?

- Resposta: O meio de transporte aéreo representa a grande maioria dos trechos registrados (mais de 70%), seguido pelo transporte rodoviário/terrestre e por veículos oficiais em trajetos intermunicipais.

![Distribuição dos Meios de Transporte](graficos_png/5_meio_transporte_mais_usado.png)

---

### 6. Frequência de Trechos por UF de Destino
Quais estados da federação (UF) concentram o maior volume de trechos?

- Resposta: O Distrito Federal (DF) lidera isoladamente como o principal destino dos trechos, seguido por estados de grande porte econômico e administrativo como São Paulo (SP) e Rio de Janeiro (RJ).

![Frequência de Trechos por UF](graficos_png/6_uf_destino_frequencia.png)

---

### 7. Total Efetivamente Pago por Órgão Superior
Qual unidade gestora realizou a maior soma em pagamentos liquidados e efetivados?

- Resposta: A análise de pagamentos liquidados confirma que o Ministério da Defesa e o Ministério da Educação são os órgãos com o maior volume financeiro efetivamente desembolsado e processado nas ordens bancárias.

![Top Órgãos por Total Efetivamente Pago](graficos_png/7_orgao_que_mais_pagou.png)


## Conclusões e Insights a Partir dos Gráficos e Análise de Base
Concentração de Recursos (Top 5 Órgãos): A visualização deixa evidente que uma pequena parcela dos órgãos superiores responde pela maior fatia do orçamento de viagens, facilitando ações prioritárias de auditoria e controle de gastos.

Polos de Deslocamento (Top 10 Cidades): O fluxo de viagens concentra-se majoritariamente em capitais e centros administrativos, o que aponta oportunidades para negociações corporativas em escala (hotéis e companhias aéreas).