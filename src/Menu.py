import Operacao

def menu(cpf):
    print("==== MENU ====")
    print("Escolha a opção:")
    opcao = input("1. Ver Saldo\n2. Depositar\n3. Sacar\n4. Extrato\n5. Fazer transferência\n6. Sair\n")

    if opcao == '1':
        Operacao.ver_saldo(cpf)
    elif opcao == '2':
        Operacao.depositar(cpf)
    elif opcao == '3':
        Operacao.sacar(cpf)
    elif opcao == '4':
        Operacao.extrato(cpf)
    elif opcao == '5':
        Operacao.transferir(cpf)
    elif opcao == '6':
        print("Saindo...")
        exit()  # Fecha o programa
    else:
        print("Opção inválida!")
        menu(cpf)  # Chama o menu novamente em caso de erro
