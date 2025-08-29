#primeiro desafio bootcamp DIO de python
#criar um sistema bancário com as operações: saque, deposito e extrato
##somente um usuario 
##deposito só pode receber valores positivos
##operações de saque devem ficar registradas
##apenas 3 saques diarios e no máximo R$500 por saque
##não pode negativar o saldo

menu = """

[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "1":
        dinheiro = float(input("Informe o valor do depósito: "))

        if dinheiro > 0:
            saldo += dinheiro
            extrato += f"Depósito: R$ {dinheiro:.2f}\n"
        else:
            print("Operação inválida: o valor deve ser positivo.")

    elif opcao == "2":
        dinheiro = float(input("Informe o valor do saque: "))

        excedeu_saldo = dinheiro > (saldo + limite)
        excedeu_limite = dinheiro > limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou: saldo e limite insuficientes.")
        elif excedeu_limite:
            print("Operação falhou: valor excede o limite por saque.")
        elif excedeu_saques:
            print("Operação falhou: número máximo de saques diários atingido.")
        elif dinheiro > 0:
            # Lógica de desconto: primeiro do saldo, depois do limite
            if dinheiro <= saldo:
                saldo -= dinheiro
            else:
                limite_utilizado = dinheiro - saldo
                saldo = 0
                limite -= limite_utilizado
            
            extrato += f"Saque: R$ {dinheiro:.2f}\n"
            numero_saques += 1
            print("Saque realizado com sucesso!")
        else:
            print("Operação falhou: valor inválido.")

    elif opcao == "3":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print(f"Limite disponível: R$ {limite:.2f}")
        print("==========================================")

    elif opcao == "0":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")