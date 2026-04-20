# 🛒 SQL — Análise de Vendas no Varejo

Projeto de análise de dados de vendas no varejo utilizando SQL, com foco em geração de insights de negócio a partir de consultas estruturadas.

## 📌 O que o projeto faz

- Criação de banco de dados SQLite com dados simulados de vendas
- Execução de queries SQL para análise de desempenho
- Identificação de produtos mais vendidos
- Análise de faturamento por período
- Ranking de clientes e categorias
- Cálculo de métricas de negócio (ticket médio, receita total, etc.)

## 📈 Resultados

- Identificação dos produtos com maior volume de vendas
- Descoberta das categorias mais lucrativas
- Análise de sazonalidade nas vendas
- Ranking de clientes com maior faturamento
- Insights para tomada de decisão em negócios de varejo

## 📊 Análises realizadas

| Query | Descrição |
|------|----------|
| `faturamento_total.sql` | Receita total do período |
| `vendas_por_categoria.sql` | Total de vendas por categoria |
| `top_produtos.sql` | Produtos mais vendidos |
| `top_clientes.sql` | Clientes com maior volume de compras |
| `ticket_medio.sql` | Cálculo do ticket médio |

## 🛠️ Tecnologias

- Python 3  
- SQLite  
- Pandas  
- SQL  

## ▶️ Como executar

```bash
git clone https://github.com/emillyhino/sql-analise-vendas-varejo.git
cd sql-analise-vendas-varejo

pip install pandas

python setup.py             # cria o banco varejo.db
python executar_queries.py  # roda todas as análises
```

## 🗄️ Estrutura do banco

O banco `varejo.db` contém tabelas como:

- `clientes`
- `produtos`
- `categorias`
- `vendas`
- `itens_venda`

## 📂 Saídas geradas

- Resultados das queries exibidos no terminal
- Possibilidade de exportação para CSV (adaptável no código)

## 🎯 Objetivo

Demonstrar habilidades em:

- Modelagem de dados
- Escrita de queries SQL eficientes
- Análise de dados para negócios
- Integração entre Python e banco de dados

## 👩‍💻 Autora

**Emilly Hino**  
Bacharela em Ciência de Dados 
[LinkedIn](https://linkedin.com/in/emillyhino)  
[GitHub](https://github.com/emillyhino)
