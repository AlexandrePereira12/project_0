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
