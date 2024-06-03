menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
LIMITE = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        deposito = -1 
        try:
            deposito = float(input("Digite o valor do depósito: "))
        except ValueError:
            pass

        if deposito > 0:
            saldo += deposito
            extrato += f"Depósito: R$ {deposito:.2f}\n"
        else:
            print("Operação inválida: valor inválido.")

    elif opcao == "s":
        saque = -1
        try:
            saque = float(input("Digite o valor do saque: "))
        except ValueError:
            pass

        if numero_saques >= LIMITE_SAQUES:
            print("Operação inválida: Limite diário de saques atingido.")
        elif saque > LIMITE:
            print("Operação inválida: Limite máximo de R$ 500.00 por saque.")
        elif saque > saldo:
            print("Operação inválida: Saldo insuficiente.")
        elif saque > 0:
            saldo -= saque
            numero_saques += 1
            extrato += f"Saque: R$ {saque:.2f}\n"
        else:
            print("Operação inválida: valor inválido.")

    elif opcao == "e":
        if extrato == "":
            print("Não foram realizadas movimentações.")
        else:
            mensagem = f"{extrato}Saldo: R$ {saldo:.2f}"
            print(mensagem)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
