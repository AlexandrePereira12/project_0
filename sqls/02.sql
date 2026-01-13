CREATE TABLE movimentacoes_estoque (
    id SERIAL PRIMARY KEY,
    produto_id INT NOT NULL REFERENCES produtos(id),
    tipo VARCHAR(20) NOT NULL, -- 'ENTRADA', 'SAIDA', 'AJUSTE'
    quantidade NUMERIC(10,2) NOT NULL,
    estoque_antes NUMERIC(10,2) NOT NULL,
    estoque_depois NUMERIC(10,2) NOT NULL,
    motivo TEXT,
    criado_em TIMESTAMP DEFAULT NOW()
);