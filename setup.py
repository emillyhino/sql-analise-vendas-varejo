import sqlite3
import random
from datetime import date, timedelta

random.seed(42)

conn = sqlite3.connect("varejo.db")
cur = conn.cursor()

with open("schema.sql") as f:
    cur.executescript(f.read())

# ── CLIENTES ──────────────────────────────────────────────────────
cidades = [("São Paulo","SP"),("Rio de Janeiro","RJ"),("Fortaleza","CE"),
           ("Recife","PE"),("Salvador","BA"),("Manaus","AM"),
           ("João Pessoa","PB"),("Natal","RN"),("Curitiba","PR"),("Belém","PA")]
nomes_clientes = [
    "Ana Lima","Bruno Souza","Carla Mendes","Diego Ferreira","Elaine Costa",
    "Felipe Rocha","Gabriela Nunes","Henrique Alves","Isabela Martins","João Silva",
    "Karina Oliveira","Lucas Pereira","Marina Santos","Nicolas Gomes","Olivia Ramos",
    "Paulo Ribeiro","Queila Moura","Rafael Torres","Sabrina Castro","Tiago Azevedo",
    "Ursula Lima","Vitor Correia","Wanda Freitas","Xavier Lopes","Yasmin Pinto",
    "Zeca Monteiro","Alice Barros","Bernardo Farias","Cecília Moreira","Daniel Cunha"
]
clientes = []
for i, nome in enumerate(nomes_clientes, 1):
    cidade, estado = random.choice(cidades)
    dias = random.randint(0, 730)
    data = date(2023, 1, 1) + timedelta(days=dias)
    clientes.append((i, nome, cidade, estado, data.isoformat()))
cur.executemany("INSERT INTO clientes VALUES (?,?,?,?,?)", clientes)

# ── VENDEDORES ────────────────────────────────────────────────────
vendedores = [
    (1,"Marcos Venda","Norte"),(2,"Patrícia Sell","Nordeste"),
    (3,"Roberto Sales","Sudeste"),(4,"Fernanda Shop","Sul"),
    (5,"André Comercial","Centro-Oeste")
]
cur.executemany("INSERT INTO vendedores VALUES (?,?,?)", vendedores)

# ── PRODUTOS ──────────────────────────────────────────────────────
produtos = [
    (1,"Notebook Pro 15","Eletrônicos",4599.90),
    (2,"Mouse Sem Fio","Periféricos",89.90),
    (3,"Teclado Mecânico","Periféricos",299.90),
    (4,"Monitor 24\"","Eletrônicos",1299.90),
    (5,"Cadeira Gamer","Móveis",899.90),
    (6,"Headset USB","Periféricos",199.90),
    (7,"Webcam HD","Periféricos",249.90),
    (8,"SSD 1TB","Armazenamento",399.90),
    (9,"Memória RAM 16GB","Armazenamento",249.90),
    (10,"Impressora Laser","Eletrônicos",1099.90),
    (11,"Roteador Wi-Fi 6","Redes",399.90),
    (12,"Hub USB-C","Periféricos",149.90),
    (13,"Suporte Monitor","Móveis",199.90),
    (14,"Mousepad XL","Periféricos",79.90),
    (15,"Nobreak 1200VA","Eletrônicos",599.90),
]
cur.executemany("INSERT INTO produtos VALUES (?,?,?,?)", produtos)

# ── ESTOQUE ───────────────────────────────────────────────────────
estoque = [(i, random.randint(0, 100), random.randint(5, 20)) for i in range(1, 16)]
cur.executemany("INSERT INTO estoque VALUES (?,?,?)", estoque)

# ── PEDIDOS E ITENS ───────────────────────────────────────────────
pedidos = []
itens = []
id_item = 1
status_opcoes = ["Entregue","Entregue","Entregue","Cancelado","Pendente"]

for id_pedido in range(1, 501):
    id_cliente  = random.randint(1, 30)
    id_vendedor = random.randint(1, 5)
    dias        = random.randint(0, 729)
    data        = date(2023, 1, 1) + timedelta(days=dias)
    status      = random.choice(status_opcoes)
    pedidos.append((id_pedido, id_cliente, id_vendedor, data.isoformat(), status))

    n_itens = random.randint(1, 4)
    produtos_pedido = random.sample(range(1, 16), n_itens)
    for id_prod in produtos_pedido:
        preco = next(p[3] for p in produtos if p[0] == id_prod)
        qtd   = random.randint(1, 5)
        itens.append((id_item, id_pedido, id_prod, qtd, preco))
        id_item += 1

cur.executemany("INSERT INTO pedidos VALUES (?,?,?,?,?)", pedidos)
cur.executemany("INSERT INTO itens_pedido VALUES (?,?,?,?,?)", itens)

conn.commit()
conn.close()
print("Banco varejo.db criado com sucesso!")
print(f"  {len(clientes)} clientes")
print(f"  {len(vendedores)} vendedores")
print(f"  {len(produtos)} produtos")
print(f"  {len(pedidos)} pedidos")
print(f"  {len(itens)} itens de pedido")