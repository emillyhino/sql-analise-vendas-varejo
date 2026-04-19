-- ================================================================
-- BANCO DE DADOS: Loja de Varejo
-- Tabelas: clientes, produtos, vendedores, pedidos, itens_pedido, estoque
-- ================================================================

CREATE TABLE clientes (
    id_cliente    INTEGER PRIMARY KEY,
    nome          TEXT NOT NULL,
    cidade        TEXT,
    estado        TEXT,
    data_cadastro DATE
);

CREATE TABLE vendedores (
    id_vendedor INTEGER PRIMARY KEY,
    nome        TEXT NOT NULL,
    regiao      TEXT
);

CREATE TABLE produtos (
    id_produto  INTEGER PRIMARY KEY,
    nome        TEXT NOT NULL,
    categoria   TEXT,
    preco_unit  REAL
);

CREATE TABLE estoque (
    id_produto       INTEGER PRIMARY KEY,
    quantidade       INTEGER,
    estoque_minimo   INTEGER,
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
);

CREATE TABLE pedidos (
    id_pedido   INTEGER PRIMARY KEY,
    id_cliente  INTEGER,
    id_vendedor INTEGER,
    data_pedido DATE,
    status      TEXT,
    FOREIGN KEY (id_cliente)  REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_vendedor) REFERENCES vendedores(id_vendedor)
);

CREATE TABLE itens_pedido (
    id_item     INTEGER PRIMARY KEY,
    id_pedido   INTEGER,
    id_produto  INTEGER,
    quantidade  INTEGER,
    preco_unit  REAL,
    FOREIGN KEY (id_pedido)  REFERENCES pedidos(id_pedido),
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
);