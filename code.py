from dataclasses import dataclass
from datetime import datetime

@dataclass
class Cliente:
    id: int
    email: str
    numero: str

@dataclass
class Categoria:
    id: int
    nome: str

@dataclass
class Fornecedor:
    id: int
    nome_empresa: str
    cnpj: str

@dataclass
class Funcionario:
    id: int
    nome: str
    cargo: str

@dataclass
class Admin:
    id: int
    nome: str
    senha: str

@dataclass
class Produto:
    id: int
    nome: str
    tamanho: str
    categoria_id: int
    cor: str
    preco: float
    descricao: str
    data: str
    marca: str

@dataclass
class Estoque:
    id: int
    produto_id: int
    qtd: int

@dataclass
class Movimento:
    id: int
    produto_id: int
    tipo: str
    qtd: int
    data: str
    funcionario_id: int

@dataclass
class Compra:
    id: int
    cliente_id: int
    produto_id: int
    pagamento: str
    status: str
    data: str
    endereco: str
    entrega: str
    frete: float
    cupom: int
    qtd: int
    total: float

@dataclass
class Pedido:
    id: int
    cliente_id: int
    pagamento_id: int
    subtotal: float
    frete: float

@dataclass
class ItemPedido:
    id: int
    pedido_id: int
    produto_id: int
    qtd: int
    preco: float

clientes = []
categorias = []
fornecedores = []
funcionarios = []
admins = []
produtos = []
estoques = []
movs = []
compras = []
pedidos = []
itens = []
carrinho = []

def agora():
    return datetime.now().strftime("%d/%m %H:%M")

def novo_id(lista):
    return len(lista) + 1  

def get_prod(pid):
    for p in produtos:
        if p.id == pid:
            return p

def get_est(pid):
    for e in estoques:
        if e.produto_id == pid:
            return e

# CADASTRO

def add_cliente():
    email = input("email: ")
    num = input("telefone: ")
    clientes.append(Cliente(novo_id(clientes), email, num))
    print("cliente ok")

def add_categoria():
    nome = input("categoria: ")
    categorias.append(Categoria(novo_id(categorias), nome))
    print("categoria salva")

def add_fornecedor():
    nome = input("nome fornecedor: ")
    cnpj = input("cnpj: ")
    fornecedores.append(Fornecedor(novo_id(fornecedores), nome, cnpj))
    print("fornecedor ok")

def add_func():
    nome = input("nome: ")
    cargo = input("cargo: ")
    funcionarios.append(Funcionario(novo_id(funcionarios), nome, cargo))
    print("funcionario criado")

def add_admin():
    nome = input("admin: ")
    senha = input("senha: ")
    admins.append(Admin(novo_id(admins), nome, senha))
    print("admin pronto")

def add_prod():
    if not categorias:
        print("cria categoria antes")
        return

    nome = input("nome: ")
    tamanho = input("tamanho: ")

    print("categorias:")
    for c in categorias:
        print(c.id, c.nome)

    cat = int(input("id cat: "))
    cor = input("cor: ")
    preco = float(input("preço: "))
    desc = input("desc: ")
    marca = input("marca: ")

    p = Produto(novo_id(produtos), nome, tamanho, cat, cor, preco, desc, agora(), marca)
    produtos.append(p)

    estoques.append(Estoque(novo_id(estoques), p.id, 0))

    print("produto foi")

# ESTOQUE

def entrada():
    listar_prod()

    pid = int(input("produto: "))
    qtd = int(input("qtd: "))
    fid = int(input("funcionario: "))

    est = get_est(pid)

    if est:
        est.qtd += qtd
        movs.append(Movimento(novo_id(movs), pid, "entrada", qtd, agora(), fid))
        print("estoque atualizado")
    else:
        print("produto não achei")

#FORNECEDOR

def cadastrar_fornecedor():
    print("\n--- Cadastrar Fornecedor ---")
    nome = input("Nome da Empresa: ")
    cnpj = input("CNPJ: ")

    fornecedor = Fornecedor(
        proximo_id(fornecedores),
        nome,
        cnpj
    )

    fornecedores.append(fornecedor)
    print("Fornecedor cadastrado!")


def listar_fornecedores():
    print("\n--- Fornecedores ---")
    for f in fornecedores:
        print(f)

# VENDAS

def comprar():
    listar_prod()

    cliente = int(input("cliente id: "))
    pid = int(input("produto: "))
    qtd = int(input("qtd: "))
    pag = input("pagamento: ")

    p = get_prod(pid)
    est = get_est(pid)

    if not p or not est or est.qtd < qtd:
        print("erro compra")
        return

    total = p.preco * qtd
    est.qtd -= qtd

    movs.append(Movimento(novo_id(movs), pid, "saida", qtd, agora(), 0))

    compras.append(Compra(
        novo_id(compras),
        cliente,
        pid,
        pag,
        "pago",
        agora(),
        "endereco padrão",
        "processando",
        20.0,
        None,
        qtd,
        total
    ))

    print("comprou ->", total)

# CARRINHO

def add_cart():
    listar_prod()

    pid = int(input("produto: "))
    qtd = int(input("qtd: "))

    carrinho.append((pid, qtd)) 
    print("add no carrinho")

def fechar_cart():
    if not carrinho:
        print("vazio")
        return

    cliente = int(input("cliente: "))
    pag = int(input("pagamento id: "))

    ped = Pedido(novo_id(pedidos), cliente, pag, 0, 20.0)
    pedidos.append(ped)

    total = 0

    for item in carrinho:
        pid, qtd = item

        p = get_prod(pid)
        est = get_est(pid)

        if not p or not est:
            print("erro item")
            continue

        if est.qtd < qtd:
            print("sem estoque:", p.nome)
            continue

        est.qtd -= qtd
        total += p.preco * qtd

        movs.append(Movimento(novo_id(movs), pid, "saida", qtd, agora(), 0))

        itens.append(ItemPedido(novo_id(itens), ped.id, pid, qtd, p.preco))

    ped.subtotal = total
    carrinho.clear()

    print("pedido fechado:", total)

# LISTAS

def listar_prod():
    print("\nprodutos:")
    for p in produtos:
        est = get_est(p.id)
        q = est.qtd if est else 0
        print(p.id, p.nome, p.preco, "| estoque:", q)

def ver_compras():
    for c in compras:
        print(c)

def ver_movs():
    print("\nmov:")
    for m in movs:
        print(m)

# MENU

def menu():
    while True:
        print("\n--- URBAN STYLE ---")
        print("1 cliente")
        print("2 categoria")
        print("3 produto")
        print("4 entrada estoque")
        print("5 comprar")
        print("6 carrinho")
        print("7 fechar carrinho")
        print("8 compras")
        print("9 fornecedor")
        print("10 funcionario")
        print("11 admin")
        print("12 movimentos")
        print("0 sair")

        op = input(">> ")

        if op == "1":
            add_cliente()
        elif op == "2":
            add_categoria()
        elif op == "3":
            add_prod()
        elif op == "4":
            entrada()
        elif op == "5":
            comprar()
        elif op == "6":
            add_cart()
        elif op == "7":
            fechar_cart()
        elif op == "8":
            ver_compras()
        elif op == "9":
            add_fornecedor()
        elif op == "10":
            add_func()
        elif op == "11":
            add_admin()
        elif op == "12":
            ver_movs()
        else:
            break

menu()
