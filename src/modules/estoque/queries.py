from sqlalchemy import text

get_produtos = text("""
    SELECT
        id,
        nome,
        valor_compra,
        valor_venda,
        quantidade_estoque,
        criado_em,
        ultima_compra,
        ultima_venda
    FROM produtos
    ORDER BY id;
""")

insert_produto = text("""
    INSERT INTO produtos (
        nome,
        valor_compra,
        valor_venda,
        quantidade_estoque
    )
    VALUES (
        :nome,
        :valor_compra,
        :valor_venda,
        :quantidade_estoque
    )
    RETURNING id;
""")

update_produto = text("""
    UPDATE produtos
    SET
        nome = COALESCE(:nome, nome),
        valor_compra = COALESCE(:valor_compra, valor_compra),
        valor_venda = COALESCE(:valor_venda, valor_venda),
        quantidade_estoque = COALESCE(:quantidade_estoque, quantidade_estoque)
    WHERE id = :id
    RETURNING id;
""")

delete_produto = text("""
    DELETE FROM produtos
    WHERE id = :produto_id
      AND quantidade_estoque = 0
    RETURNING id
""")

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