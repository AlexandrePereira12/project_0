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