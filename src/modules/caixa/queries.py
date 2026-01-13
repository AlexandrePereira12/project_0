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
        motivo
    )
    VALUES
    (
        :produto_id,
        :tipo,
        :quantidade,
        :estoque_antes,
        :estoque_depois,
        :motivo
    )
""")