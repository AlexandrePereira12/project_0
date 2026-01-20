from sqlalchemy import text

check_quantidade_produto = text("""
    SELECT quantidade_estoque
    FROM produtos
    WHERE id = :produto_id
""")

saida_produto = text("""
    UPDATE produtos
    SET
        quantidade_estoque = :quantidade_estoque,
        ultima_venda = NOW()
    WHERE id = :id
    RETURNING id, quantidade_estoque, ultima_venda
""")

entrada_produto = text("""
    UPDATE produtos
    SET
        quantidade_estoque = :quantidade_estoque,
        ultima_compra = NOW()
    WHERE id = :id 
    RETURNING id, quantidade_estoque, ultima_compra
""")

insert_movimentacao = text("""
    INSERT INTO movimentacoes_estoque
    (
        produto_id,
        tipo,
        quantidade,
        estoque_antes,
        estoque_depois,
        motivo,
        forma_pagamento
    )
    VALUES
    (
        :produto_id,
        :tipo,
        :quantidade,
        :estoque_antes,
        :estoque_depois,
        :motivo,
        :forma_pagamento
    )
""")

get_movimentacoes = text("""
    SELECT
        me.id,
        p.nome AS produto_nome,
        me.quantidade,
        p.valor_venda AS valor_unitario,
        (p.valor_venda * me.quantidade) AS valor_total,
        me.forma_pagamento,
        (me.criado_em AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo') AS data
    FROM movimentacoes_estoque me
    JOIN produtos p ON p.id = me.produto_id
    WHERE me.tipo = 'SAIDA'
    AND me.motivo = 'VENDA'
    ORDER BY me.criado_em DESC
    LIMIT :limit
""")