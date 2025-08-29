def depositar(saldo, extrato, valor, /):
    if valor <= 0:
        return {
            'saldo': saldo,
            'extrato': extrato,
            'sucesso': False,
            'mensagem': "Operação falhou: o valor deve ser positivo."
        }
    
    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"
    
    return {
        'saldo': saldo,
        'extrato': extrato,
        'sucesso': True,
        'mensagem': f"Depósito de R$ {valor:.2f} realizado com sucesso!"
    }

def sacar(*, saldo, limite, numero_saques, LIMITE_SAQUES, valor):
    if valor <= 0:
        return {
            'saldo': saldo,
            'limite': limite,
            'numero_saques': numero_saques,
            'sucesso': False,
            'mensagem': "Operação falhou: valor inválido."
        }
    
    limite_total = saldo + limite
    excedeu_saldo_limite = valor > limite_total
    excedeu_limite_por_saque = valor > 500
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo_limite:
        return {
            'saldo': saldo,
            'limite': limite,
            'numero_saques': numero_saques,
            'sucesso': False,
            'mensagem': f"Operação falhou: saldo e limite insuficientes. Disponível: R$ {limite_total:.2f}"
        }
    elif excedeu_limite_por_saque:
        return {
            'saldo': saldo,
            'limite': limite,
            'numero_saques': numero_saques,
            'sucesso': False,
            'mensagem': "Operação falhou: valor excede o limite por saque (R$ 500,00)."
        }
    elif excedeu_saques:
        return {
            'saldo': saldo,
            'limite': limite,
            'numero_saques': numero_saques,
            'sucesso': False,
            'mensagem': "Operação falhou: número máximo de saques diários atingido."
        }
    
    if valor <= saldo:
        saldo -= valor
    else:
        valor_restante = valor - saldo
        saldo = 0
        limite -= valor_restante
    
    return {
        'saldo': saldo,
        'limite': limite,
        'numero_saques': numero_saques + 1,
        'sucesso': True,
        'mensagem': f"Saque de R$ {valor:.2f} realizado com sucesso!"
    }

def exibir_extrato(saldo, /, *, limite, extrato):
    limite_total = saldo + limite
    
    extrato_formatado = "\n================ EXTRATO ================\n"
    extrato_formatado += "Não foram realizadas movimentações." if not extrato else extrato
    extrato_formatado += f"\n\nSaldo: R$ {saldo:.2f}"
    extrato_formatado += f"\nLimite disponível: R$ {limite:.2f}"
    extrato_formatado += f"\nLimite total para saque: R$ {limite_total:.2f}"
    extrato_formatado += "\n=========================================="
    
    return extrato_formatado

def cadastrar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ").strip()
    
    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print("Erro: Já existe usuário com esse CPF!")
        return usuarios, False
    
    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ").strip()
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/UF): ").strip()
    
    usuario = {
        'cpf': cpf,
        'nome': nome,
        'data_nascimento': data_nascimento,
        'endereco': endereco
    }
    
    usuarios.append(usuario)
    print("Usuário cadastrado com sucesso!")
    return usuarios, True

def cadastrar_conta_bancaria(contas, usuarios, numero_conta):
    cpf = input("Informe o CPF do usuário: ").strip()
    
    usuario = next((u for u in usuarios if u['cpf'] == cpf), None)
    
    if not usuario:
        print("Erro: Usuário não encontrado! Cadastre o usuario primeiro.")
        return contas, False
    
    conta = {
        'agencia': '0001',
        'numero_conta': numero_conta,
        'usuario': usuario,
        'saldo': 0,
        'limite': 500,
        'extrato': "",
        'numero_saques': 0
    }
    
    contas.append(conta)
    print(f"Conta criada com sucesso! Número: {numero_conta}")
    return contas, True

def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    
    print("\n=== CONTAS CADASTRADAS ===")
    for conta in contas:
        print(f"Agência: {conta['agencia']}")
        print(f"C/C: {conta['numero_conta']}")
        print(f"Titular: {conta['usuario']['nome']}")
        print(f"CPF: {conta['usuario']['cpf']}")
        print("------------------------")

def selecionar_conta(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return None
    
    listar_contas(contas)
    
    try:
        numero = int(input("\nInforme o número da conta: "))
        conta = next((c for c in contas if c['numero_conta'] == numero), None)
        
        if conta:
            return conta
        else:
            print("Conta não encontrada.")
            return None
    except ValueError:
        print("Número de conta inválido.")
        return None

def main():
    menu_principal = """
    [1] Cadastrar Usuário
    [2] Cadastrar Conta Bancária
    [3] Listar Contas
    [4] Acessar Conta
    [0] Sair

    => """
    
    menu_conta = """
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Voltar ao Menu Principal

    => """
    
    usuarios = []
    contas = []
    numero_conta = 1
    LIMITE_SAQUES = 3

    while True:
        opcao = input(menu_principal).strip()

        if opcao == "1":
            usuarios, sucesso = cadastrar_usuario(usuarios)
            
        elif opcao == "2":
            if not usuarios:
                print("Cadastre pelo menos um usuário primeiro!")
            else:
                contas, sucesso = cadastrar_conta_bancaria(contas, usuarios, numero_conta)
                if sucesso:
                    numero_conta += 1
            
        elif opcao == "3":
            listar_contas(contas)
            
        elif opcao == "4":
            conta = selecionar_conta(contas)
            if conta:
                while True:
                    opcao_conta = input(menu_conta).strip()
                    
                    if opcao_conta == "1":
                        try:
                            valor = float(input("Informe o valor do depósito: "))
                            resultado = depositar(conta['saldo'], conta['extrato'], valor)
                            conta['saldo'] = resultado['saldo']
                            conta['extrato'] = resultado['extrato']
                            print(resultado['mensagem'])
                        except ValueError:
                            print("Operação falhou: valor informado não é numérico.")
                    
                    elif opcao_conta == "2":
                        try:
                            valor = float(input("Informe o valor do saque: "))
                            resultado = sacar(
                                saldo=conta['saldo'],
                                limite=conta['limite'],
                                numero_saques=conta['numero_saques'],
                                LIMITE_SAQUES=LIMITE_SAQUES,
                                valor=valor
                            )
                            conta['saldo'] = resultado['saldo']
                            conta['limite'] = resultado['limite']
                            conta['numero_saques'] = resultado['numero_saques']
                            print(resultado['mensagem'])
                            if resultado['sucesso']:
                                conta['extrato'] += f"Saque: R$ {valor:.2f}\n"
                        except ValueError:
                            print("Operação falhou: valor informado não é numérico.")
                    
                    elif opcao_conta == "3":
                        print(exibir_extrato(
                            conta['saldo'],
                            limite=conta['limite'],
                            extrato=conta['extrato']
                        ))
                    
                    elif opcao_conta == "4":
                        break
                    
                    else:
                        print("Operação inválida!")
            
        elif opcao == "0":
            print("Obrigado por usar nosso sistema bancário!")
            break
        
        else:
            print("Operação inválida!")

if __name__ == "__main__":
    main()