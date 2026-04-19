import sqlite3
import pandas as pd

conn = sqlite3.connect("varejo.db")

queries = {
    "1. Ranking de vendedores por receita": """
        SELECT v.nome AS vendedor, v.regiao,
            COUNT(DISTINCT p.id_pedido) AS total_pedidos,
            ROUND(SUM(i.quantidade * i.preco_unit), 2) AS receita_total,
            ROUND(SUM(i.quantidade * i.preco_unit) * 100.0 /
                SUM(SUM(i.quantidade * i.preco_unit)) OVER (), 2) AS pct_receita
        FROM vendedores v
        JOIN pedidos p      ON v.id_vendedor = p.id_vendedor
        JOIN itens_pedido i ON p.id_pedido   = i.id_pedido
        WHERE p.status = 'Entregue'
        GROUP BY v.id_vendedor, v.nome, v.regiao
        ORDER BY receita_total DESC
    """,
    "2. Top produtos por categoria": """
        WITH vendas_produto AS (
            SELECT pr.categoria, pr.nome AS produto,
                SUM(i.quantidade) AS total_vendido,
                ROUND(SUM(i.quantidade * i.preco_unit), 2) AS receita
            FROM itens_pedido i
            JOIN pedidos p   ON i.id_pedido  = p.id_pedido
            JOIN produtos pr ON i.id_produto = pr.id_produto
            WHERE p.status = 'Entregue'
            GROUP BY pr.id_produto, pr.categoria, pr.nome
        ),
        ranking AS (
            SELECT *, RANK() OVER (PARTITION BY categoria ORDER BY total_vendido DESC) AS rank_categoria
            FROM vendas_produto
        )
        SELECT categoria, rank_categoria, produto, total_vendido, receita
        FROM ranking WHERE rank_categoria <= 3
        ORDER BY categoria, rank_categoria
    """,
    "3. Segmentação de clientes RFM": """
        WITH rfm AS (
            SELECT c.id_cliente, c.nome, c.cidade, c.estado,
                MAX(p.data_pedido) AS ultimo_pedido,
                COUNT(DISTINCT p.id_pedido) AS frequencia,
                ROUND(SUM(i.quantidade * i.preco_unit), 2) AS valor_total
            FROM clientes c
            JOIN pedidos p      ON c.id_cliente = p.id_cliente
            JOIN itens_pedido i ON p.id_pedido  = i.id_pedido
            WHERE p.status = 'Entregue'
            GROUP BY c.id_cliente, c.nome, c.cidade, c.estado
        )
        SELECT *, CASE
            WHEN frequencia >= 25 AND valor_total >= 10000 THEN 'VIP'
            WHEN frequencia >= 15 THEN 'Fiel'
            WHEN frequencia >= 5  THEN 'Regular'
            ELSE 'Ocasional'
        END AS segmento
        FROM rfm ORDER BY valor_total DESC
    """,
    "4. Estoque crítico": """
        SELECT pr.nome AS produto, pr.categoria,
            e.quantidade AS estoque_atual, e.estoque_minimo,
            e.estoque_minimo - e.quantidade AS deficit,
            ROUND(e.quantidade * 1.0 / e.estoque_minimo * 100, 1) AS pct_estoque
        FROM estoque e
        JOIN produtos pr ON e.id_produto = pr.id_produto
        WHERE e.quantidade < e.estoque_minimo
        ORDER BY deficit DESC
    """,
    "5. Receita mensal com variação": """
        WITH receita_mensal AS (
            SELECT strftime('%Y-%m', p.data_pedido) AS mes,
                ROUND(SUM(i.quantidade * i.preco_unit), 2) AS receita
            FROM pedidos p
            JOIN itens_pedido i ON p.id_pedido = i.id_pedido
            WHERE p.status = 'Entregue'
            GROUP BY mes
        )
        SELECT mes, receita,
            LAG(receita) OVER (ORDER BY mes) AS receita_mes_anterior,
            ROUND((receita - LAG(receita) OVER (ORDER BY mes)) * 100.0 /
                LAG(receita) OVER (ORDER BY mes), 1) AS variacao_pct
        FROM receita_mensal ORDER BY mes
    """,
    "6. Taxa de cancelamento por vendedor": """
        SELECT v.nome AS vendedor, COUNT(*) AS total_pedidos,
            SUM(CASE WHEN p.status = 'Cancelado' THEN 1 ELSE 0 END) AS cancelados,
            ROUND(SUM(CASE WHEN p.status = 'Cancelado' THEN 1.0 ELSE 0 END)
                / COUNT(*) * 100, 1) AS taxa_cancelamento_pct
        FROM vendedores v
        JOIN pedidos p ON v.id_vendedor = p.id_vendedor
        GROUP BY v.id_vendedor, v.nome
        ORDER BY taxa_cancelamento_pct DESC
    """,
    "7. Ticket médio por estado": """
        SELECT c.estado, COUNT(DISTINCT p.id_pedido) AS total_pedidos,
            ROUND(SUM(i.quantidade * i.preco_unit), 2) AS receita_total,
            ROUND(SUM(i.quantidade * i.preco_unit) / COUNT(DISTINCT p.id_pedido), 2) AS ticket_medio
        FROM clientes c
        JOIN pedidos p      ON c.id_cliente = p.id_cliente
        JOIN itens_pedido i ON p.id_pedido  = i.id_pedido
        WHERE p.status = 'Entregue'
        GROUP BY c.estado ORDER BY ticket_medio DESC
    """,
    "8. Produtos nunca vendidos": """
        SELECT pr.nome AS produto, pr.categoria, pr.preco_unit, e.quantidade AS estoque_atual
        FROM produtos pr
        LEFT JOIN itens_pedido i ON pr.id_produto = i.id_produto
        JOIN estoque e           ON pr.id_produto = e.id_produto
        WHERE i.id_produto IS NULL
    """,
    "9. Clientes inativos (churn)": """
        WITH ultimo_pedido AS (
            SELECT id_cliente, MAX(data_pedido) AS ultimo_pedido
            FROM pedidos WHERE status = 'Entregue'
            GROUP BY id_cliente
        )
        SELECT c.nome, c.cidade, c.estado, u.ultimo_pedido,
            CAST(julianday('2024-12-31') - julianday(u.ultimo_pedido) AS INTEGER) AS dias_inativo
        FROM clientes c
        JOIN ultimo_pedido u ON c.id_cliente = u.id_cliente
        WHERE CAST(julianday('2024-12-31') - julianday(u.ultimo_pedido) AS INTEGER) > 180
        ORDER BY dias_inativo DESC
    """,
    "10. Receita acumulada no ano": """
        WITH receita_mensal AS (
            SELECT strftime('%Y-%m', p.data_pedido) AS mes,
                ROUND(SUM(i.quantidade * i.preco_unit), 2) AS receita
            FROM pedidos p
            JOIN itens_pedido i ON p.id_pedido = i.id_pedido
            WHERE p.status = 'Entregue'
            GROUP BY mes
        )
        SELECT mes, receita,
            ROUND(SUM(receita) OVER (ORDER BY mes ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS receita_acumulada
        FROM receita_mensal ORDER BY mes
    """
}

for titulo, query in queries.items():
    print(f"\n{'='*60}")
    print(f" {titulo}")
    print('='*60)
    df = pd.read_sql_query(query, conn)
    print(df.to_string(index=False))

conn.close()
print("\n✅ Todas as queries executadas com sucesso!")