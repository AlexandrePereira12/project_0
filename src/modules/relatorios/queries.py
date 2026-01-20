from sqlalchemy import text


relatorio_vendas_periodo = text("""
    SELECT
        p.id AS produto_id,
        p.nome,
        SUM(m.quantidade) AS quantidade_vendida,
        COUNT(m.id) AS total_operacoes,
        SUM(m.quantidade * p.valor_venda) AS faturamento
    FROM movimentacoes_estoque m
    JOIN produtos p ON p.id = m.produto_id
    WHERE m.tipo = 'SAIDA'
      AND (
            (m.criado_em AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo')
            BETWEEN :data_inicio AND :data_fim
          )
      AND (
            CAST(:produto_id AS INTEGER) IS NULL
            OR p.id = :produto_id
          )
    GROUP BY p.id, p.nome
    ORDER BY faturamento DESC
""")
