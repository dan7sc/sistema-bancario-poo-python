def menu():
    menu = "\n\n[d] Depositar" \
    "\n[s] Sacar" \
    "\n[e] Extrato" \
    "\n[u] Criar usuario" \
    "\n[c] Criar conta" \
    "\n[lu] Listar usuarios" \
    "\n[lc] Listar contas" \
    "\n[q] Sair\n\n=> "
    return menu

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação inválida: valor inválido.")

    return (saldo, extrato)

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_saques >= limite_saques:
        print("Operação inválida: Limite diário de saques atingido.")
    elif valor > limite:
        print("Operação inválida: Limite máximo de R$ 500.00 por saque.")
    elif valor > saldo:
        print("Operação inválida: Saldo insuficiente.")
    elif valor > 0:
        saldo -= valor
        numero_saques += 1
        extrato += f"Saque: R$ {valor:.2f}\n"
    else:
        print("Operação inválida: valor inválido.")

    return (saldo, extrato, numero_saques)

def visualizar_extrato(saldo, /, *, extrato):
    if extrato == "":
        print("Não foram realizadas movimentações.")
    else:
        mensagem = f"{extrato}Saldo: R$ {saldo:.2f}"
        print(mensagem)

def busca_usuario(usuarios, cpf):
    usuario = None

    for u in usuarios:
        if u['cpf'] == cpf:
            usuario = u

    return usuario

def criar_usuario(usuarios):
    cpf = input("Digite o cpf: ")

    if busca_usuario(usuarios, cpf):
        print("Usuario já cadastrado.")
        return None

    nome = input("Digite o nome: ")
    data_nascimento = input("Digite a data de nascimento [dd-mm-yyyy]: ")
    logradouro = input("Digite o logradouro: ")
    numero_do_logradouro = input("Digite o numero do logradouro: ")
    bairro = input("Digite o bairro: ")
    cidade = input("Digite a cidade: ")
    estado = input("Digite a sigla do estado: ")

    endereco = f"{logradouro}, {numero_do_logradouro} - {bairro} - {cidade}/{estado}"

    usuario = {
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    }
    usuarios.append(usuario)
    print(f"Usuario {usuario} criado.")

def criar_conta(contas, usuarios):
    cpf = input("Digite o cpf do usuario: ")

    usuario = busca_usuario(usuarios, cpf)
    if  usuario == None:
        print("Usuario não cadastrado.")
        return None

    agencia = "0001"
    numero_da_conta = f"{len(contas)+1}"

    conta = {
        "agencia": agencia,
        "numero": numero_da_conta,
        "usuario": usuario
    }

    contas.append(conta)
    print(f"Conta {conta} criada.")

def listar_usuarios(usuarios):
    if len(usuarios) == 0:
        print("Não há nenhum usuário cadastrado.")
    for usuario in usuarios:
        print("------------------------------")
        print(f"nome: {usuario['nome']}")
        print(f"cpf: {usuario['cpf']}")
        print(f"data de nascimento: {usuario['data_nascimento']}")
        print(f"endereco: {usuario['endereco']}")

def listar_contas(contas):
    if len(contas) == 0:
        print("Não há nenhuma conta cadastrada.")
    for conta in contas:
        print("------------------------------")
        print(f"agencia: {conta['agencia']}")
        print(f"numero da conta: {conta['numero']}")
        print(f"cpf do usuario: {conta['usuario']['cpf']}")
        print(f"nome do usuario: {conta['usuario']['nome']}")


def main():
    saldo = 0
    LIMITE = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []

    while True:

        opcao = input(menu())

        if opcao == "d":
            try:
                valor = float(input("Digite o valor do depósito: "))
                saldo, extrato = depositar(saldo, valor, extrato)
            except ValueError:
                print("Operação inválida: valor inválido.")

        elif opcao == "s":
            try:
                valor = float(input("Digite o valor do saque: "))
                saldo, extrato, numero_saques = sacar(saldo=saldo,
                                                      valor=valor,
                                                      extrato=extrato,
                                                      limite=LIMITE,
                                                      numero_saques=numero_saques,
                                                      limite_saques=LIMITE_SAQUES)
            except ValueError:
                print("Operação inválida: valor inválido.")

        elif opcao == "e":
            visualizar_extrato(saldo, extrato=extrato)

        elif opcao == "u":
            criar_usuario(usuarios)

        elif opcao == "c":
            criar_conta(contas, usuarios)

        elif opcao == "lu":
            listar_usuarios(usuarios)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
