CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,

    nome VARCHAR(255) NOT NULL,

    valor_compra NUMERIC(10,2) NOT NULL,
    valor_venda  NUMERIC(10,2) NOT NULL,

    quantidade_estoque INTEGER NOT NULL DEFAULT 0,

    criado_em TIMESTAMP NOT NULL DEFAULT NOW(),
    ultima_compra TIMESTAMP,
    ultima_venda  TIMESTAMP
);