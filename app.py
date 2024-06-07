from abc import abstractmethod
from datetime import date

class Cliente:
    def __init__(self,
                 endereco: str,
                 contas: list):
        self._endereco = endereco
        self._contas = contas

    def realizar_transacao(self,
                           conta,
                           transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self,
                 cpf: str,
                 nome: str,
                 data_nascimento: date,
                 *args,
                 **kwargs):
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"

class Conta:
    def __init__(self,
                 saldo: float,
                 numero: int,
                 agencia: str,
                 cliente: Cliente,
                 historico):
        self._saldo = saldo
        self._numero = len(cliente._contas)+1
        self._agencia = agencia
        self._cliente = cliente
        self._historico = historico

    def saldo(self) -> float:
        return self._saldo

    def nova_conta(self,
                   cliente: Cliente,
                   numero: int):
        pass

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            transacao = Deposito(valor)
            self._historico.adicionar_transacao(transacao)
            print("Depósito realizado.")
        else:
            print("Operação inválida: valor inválido.")

    def sacar(self, valor: float) -> bool:
        pass

class ContaCorrente(Conta):

    def __init__(self,
                 limite: float,
                 limite_saques: int,
                 *args,
                 **kwargs):
        self._limite = limite
        self._limite_saques = limite_saques
        self._numero_saques = 0
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}:{valor}' for chave, valor in self.__dict__.items()])}"

    def nova_conta(self,
                   cliente: Cliente,
                   numero: int):
        return ContaCorrente(saldo=0,
                             numero=numero,
                             agencia=self._agencia,
                             cliente=cliente,
                             historico=Historico(),
                             limite=self._limite,
                             limite_saques=self._limite_saques)

    def sacar(self, valor: float) -> bool:
        if self._numero_saques >= self._limite_saques:
            print("Operação inválida: Limite diário de saques atingido.")
        elif valor > self._limite:
            print("Operação inválida: Limite máximo de R$ 500.00 por saque.")
        elif valor > self._saldo:
            print("Operação inválida: Saldo insuficiente.")
        elif valor > 0:
            self._saldo -= valor
            self._numero_saques += 1
            transacao = Saque(valor)
            self._historico.adicionar_transacao(transacao)
            print("Saque realizado.")
        else:
            print("Operação inválida: valor inválido.")


class Transacao:
    @abstractmethod
    def registrar(self, conta: Conta):
        pass

class Deposito(Transacao):

    def __init__(self, valor: float):
        self._valor = valor

    def __str__(self):
        return f"{self.__class__.__name__}: {self._valor: .2f}"

    def registrar(self, conta: Conta):
        conta.historico.adicionar_transacao(f"Depósito: {valor: .2f}")

class Saque(Transacao):

    def __init__(self, valor: float):
        self._valor = valor

    def __str__(self):
        return f"{self.__class__.__name__}: {self._valor: .2f}"

    def registrar(self, conta: Conta):
        conta.historico.adicionar_transacao(f"Saque: {valor: .2f}")

class Historico:

    def __init__(self):
        self._log = []

    def adicionar_transacao(self, transacao):
        self._log.append(f"{transacao}")


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

def busca_usuario(usuarios, cpf):
    for usuario in usuarios:
        if usuario._cpf == cpf:
            return usuario
    return None

def criar_usuario(usuarios):
    cpf = input("Digite o cpf: ")

    if busca_usuario(usuarios, cpf):
        print("Usuario já cadastrado.")
        return None

    #nome = input("Digite o nome: ")
    #data_nascimento = input("Digite a data de nascimento [dd-mm-yyyy]: ")
    #logradouro = input("Digite o logradouro: ")
    #numero_do_logradouro = input("Digite o numero do logradouro: ")
    #bairro = input("Digite o bairro: ")
    #cidade = input("Digite a cidade: ")
    #estado = input("Digite a sigla do estado: ")
    #endereco = f"{logradouro}, {numero_do_logradouro} - {bairro} - {cidade}/{estado}"

    nome = "dan"
    data_nascimento = "01-01-2023"
    endereco = "rua tal, 8 - Barro - City/ES"

    usuario = PessoaFisica(cpf=cpf,
                           nome=nome,
                           data_nascimento=data_nascimento,
                           endereco=endereco,
                           contas=[])

    usuarios.append(usuario)
    print(f"Usuario criado.\n{usuario}")

def criar_conta(usuarios, saldo, limite, limite_saques):
    cpf = input("Digite o cpf do usuario: ")

    usuario = busca_usuario(usuarios, cpf)
    if  usuario == None:
        print("Usuario não cadastrado.")
        return None

    agencia = "0001"

    if len(usuario._contas) == 0:
        conta = ContaCorrente(saldo=saldo,
                      numero=len(usuario._contas)+1,
                      agencia=agencia,
                      cliente=usuario,
                      historico=Historico(),
                      limite=limite,
                      limite_saques=limite_saques)
        usuario.adicionar_conta(conta)
    else:
        conta = usuario._contas[0].nova_conta(usuario, len(usuario._contas)+1)
        usuario.adicionar_conta(conta)
    print(f"Conta criada.\n{conta}")

def listar_usuarios(usuarios):
    if len(usuarios) == 0:
        print("Não há nenhum usuário cadastrado.")
        return
    for usuario in usuarios:
        print("------------------------------")
        print(usuario)
        #print(f"nome: {usuario.nome}")
        #print(f"cpf: {usuario.cpf}")
        #print(f"data de nascimento: {usuario.data_nascimento}")
        #print(f"endereco: {usuario.endereco}")

def listar_contas(usuarios):
  # if len(usuarios) == 0:
   #     print("Não há nenhuma conta cadastrada.")
   #     return
    for usuario in usuarios:
        for conta in usuario._contas:
            print("------------------------------")
            print(conta)
            #print(f"agencia: {conta._agencia}")
            #print(f"numero da conta: {conta._numero}")
            #print(f"cpf do usuario: {conta._cliente._cpf}")
            #print(f"nome do usuario: {conta._cliente._nome}")


def main():
    saldo = 0
    LIMITE = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    usuarios = []

    while True:

        opcao = input(menu())

        if opcao == "d":
            try:
                valor = float(input("Digite o valor do depósito: "))
                usuarios[0]._contas[0].depositar(valor)
            except ValueError:
                print("Operação inválida: valor inválido.")

        elif opcao == "s":
            try:
                valor = float(input("Digite o valor do saque: "))
                usuarios[0]._contas[0].sacar(valor)
            except ValueError:
                print("Operação inválida: valor inválido.")

        elif opcao == "e":
            print(usuarios[0]._contas[0]._historico._log)

        elif opcao == "u":
            criar_usuario(usuarios)

        elif opcao == "c":
            criar_conta(usuarios, saldo, LIMITE, LIMITE_SAQUES)

        elif opcao == "lu":
            listar_usuarios(usuarios)

        elif opcao == "lc":
            listar_contas(usuarios)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
