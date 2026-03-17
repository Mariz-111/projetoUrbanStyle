from dataclasses import dataclass
from datetime import datetime

# ================== MODELOS ==================

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
    nome: str
    cnpj: str

@dataclass
class Funcionario:
    id: int
    nome: str
    cargo: str

@dataclass
class Administrador:
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
    data_cadastro: str
    marca: str

@dataclass
class Estoque:
    id: int
    produto_id: int
    quantidade: int

@dataclass
class MovimentoEstoque:
    id: int
    produto_id: int
    tipo: str
    quantidade: int
    data: str
    funcionario_id: int

@dataclass
class Compra:
    id: int
    usuario_id: int
    produto_id: int
    metodo_pagamento: str
    status_pagamento: str
    data_pagamento: str
    endereco_entrega: str
    status_entrega: str
    frete: float
    cupom_id: int
    quantidade: int
    valor_total: float

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
    quantidade: int
    preco: float


# ================== "BANCO" ==================

clientes = []
categorias = []
fornecedores = []
funcionarios = []
administradores = []
produtos = []
estoques = []
movimentos_estoque = []
compras = []
pedidos = []
itens_pedido = []
carrinho = []


# ================== AUX ==================

def agora():
    return datetime.now().strftime("%d/%m/%Y %H:%M")

def proximo_id(lista):
    return len(lista) + 1

def buscar_produto(pid):
    return next((p for p in produtos if p.id == pid), None)

def buscar_estoque(pid):
    return next((e for e in estoques if e.produto_id == pid), None)


# ================== CADASTROS ==================

def cadastrar_cliente():
    email = input("Email: ")
    numero = input("Telefone: ")
    clientes.append(Cliente(proximo_id(clientes), email, numero))
    print("Cliente cadastrado!")

def cadastrar_categoria():
    nome = input("Nome categoria: ")
    categorias.append(Categoria(proximo_id(categorias), nome))
    print("Categoria cadastrada!")

def cadastrar_fornecedor():
    nome = input("Nome fornecedor: ")
    cnpj = input("CNPJ: ")
    fornecedores.append(Fornecedor(proximo_id(fornecedores), nome, cnpj))
    print("Fornecedor cadastrado!")

def cadastrar_funcionario():
    nome = input("Nome funcionário: ")
    cargo = input("Cargo: ")
    funcionarios.append(Funcionario(proximo_id(funcionarios), nome, cargo))
    print("Funcionário cadastrado!")

def cadastrar_admin():
    nome = input("Nome admin: ")
    senha = input("Senha: ")
    administradores.append(Administrador(proximo_id(administradores), nome, senha))
    print("Administrador cadastrado!")

def cadastrar_produto():
    if not categorias:
        print("Cadastre categoria primeiro")
        return

    nome = input("Nome: ")
    tamanho = input("Tamanho: ")

    print("\nCategorias:")
    for c in categorias:
        print(c.id, c.nome)

    categoria_id = int(input("ID categoria: "))
    cor = input("Cor: ")
    preco = float(input("Preço: "))
    descricao = input("Descrição: ")
    marca = input("Marca: ")

    p = Produto(
        proximo_id(produtos),
        nome,
        tamanho,
        categoria_id,
        cor,
        preco,
        descricao,
        agora(),
        marca
    )

    produtos.append(p)
    estoques.append(Estoque(proximo_id(estoques), p.id, 0))

    print("Produto cadastrado!")


# ================== ESTOQUE ==================

def entrada_estoque():
    listar_produtos()

    pid = int(input("ID produto: "))
    qtd = int(input("Quantidade: "))
    fid = int(input("ID funcionário: "))

    estoque = buscar_estoque(pid)

    if estoque:
        estoque.quantidade += qtd

        movimentos_estoque.append(MovimentoEstoque(
            proximo_id(movimentos_estoque),
            pid,
            "ENTRADA",
            qtd,
            agora(),
            fid
        ))

        print("Entrada registrada!")
    else:
        print("Produto não encontrado")


# ================== VENDAS ==================

def comprar_direto():
    listar_produtos()

    cliente_id = int(input("ID cliente: "))
    pid = int(input("ID produto: "))
    qtd = int(input("Quantidade: "))
    pagamento = input("Pagamento: ")

    produto = buscar_produto(pid)
    estoque = buscar_estoque(pid)

    if not produto or not estoque or qtd > estoque.quantidade:
        print("Erro na compra")
        return

    total = produto.preco * qtd
    estoque.quantidade -= qtd

    movimentos_estoque.append(MovimentoEstoque(
        proximo_id(movimentos_estoque),
        pid,
        "SAIDA",
        qtd,
        agora(),
        0
    ))

    compras.append(Compra(
        proximo_id(compras),
        cliente_id,
        pid,
        pagamento,
        "Pago",
        agora(),
        "Endereço padrão",
        "Processando",
        20.0,
        None,
        qtd,
        total
    ))

    print(f"Compra feita! Total R$ {total:.2f}")


# ================== CARRINHO ==================

def adicionar_carrinho():
    listar_produtos()

    pid = int(input("ID produto: "))
    qtd = int(input("Qtd: "))

    produto = buscar_produto(pid)
    estoque = buscar_estoque(pid)

    if not produto or not estoque or qtd > estoque.quantidade:
        print("Erro")
        return

    carrinho.append({
        "produto_id": pid,
        "nome": produto.nome,
        "quantidade": qtd,
        "valor": produto.preco
    })

    print("Adicionado ao carrinho")

def finalizar_carrinho():
    if not carrinho:
        print("Carrinho vazio")
        return

    cliente_id = int(input("ID cliente: "))
    pagamento_id = int(input("ID pagamento: "))

    subtotal = 0

    pedido = Pedido(
        proximo_id(pedidos),
        cliente_id,
        pagamento_id,
        0,
        20.0
    )

    pedidos.append(pedido)

    for item in carrinho:
        produto = buscar_produto(item["produto_id"])
        estoque = buscar_estoque(item["produto_id"])

        estoque.quantidade -= item["quantidade"]

        movimentos_estoque.append(MovimentoEstoque(
            proximo_id(movimentos_estoque),
            produto.id,
            "SAIDA",
            item["quantidade"],
            agora(),
            0
        ))

        subtotal += item["quantidade"] * item["valor"]

        itens_pedido.append(ItemPedido(
            proximo_id(itens_pedido),
            pedido.id,
            produto.id,
            item["quantidade"],
            produto.preco
        ))

    pedido.subtotal = subtotal
    carrinho.clear()

    print("Pedido finalizado!")


# ================== LISTAGENS ==================

def listar_produtos():
    print("\n--- PRODUTOS ---")
    for p in produtos:
        estoque = buscar_estoque(p.id)
        print(p.id, p.nome, "| R$", p.preco, "| Estoque:", estoque.quantidade if estoque else 0)

def listar_compras():
    for c in compras:
        print(c)

def listar_movimentos():
    print("\n--- MOVIMENTOS ---")
    for m in movimentos_estoque:
        print(m)


# ================== MENU ==================

def menu():
    while True:
        print("\n==== URBAN STYLE ====")
        print("1 Cliente")
        print("2 Categoria")
        print("3 Produto")
        print("4 Entrada estoque")
        print("5 Comprar direto")
        print("6 Carrinho")
        print("7 Finalizar carrinho")
        print("8 Compras")
        print("9 Fornecedor")
        print("10 Funcionário")
        print("11 Administrador")
        print("12 Movimentos estoque")
        print("0 Sair")

        op = input("> ")

        if op == "1":
            cadastrar_cliente()
        elif op == "2":
            cadastrar_categoria()
        elif op == "3":
            cadastrar_produto()
        elif op == "4":
            entrada_estoque()
        elif op == "5":
            comprar_direto()
        elif op == "6":
            adicionar_carrinho()
        elif op == "7":
            finalizar_carrinho()
        elif op == "8":
            listar_compras()
        elif op == "9":
            cadastrar_fornecedor()
        elif op == "10":
            cadastrar_funcionario()
        elif op == "11":
            cadastrar_admin()
        elif op == "12":
            listar_movimentos()
        else:
            break


menu()
