from Data import conexao
from datetime import datetime
import Menu

# Função para ver o saldo
def ver_saldo(cpf):
    # Cria conexão com o banco e configura o cursor para executar os comando SQL
    conexao_db = conexao()
    cursor = conexao_db.cursor()

    # Puxa o saldo atual pelo cpf que esta sendo passado no parêmetro da função
    print("=== Visualizar saldo ===")
    cursor.execute("SELECT saldo FROM usuarios WHERE cpf = ?", (cpf,))
    resultado = cursor.fetchone()

    # Print do saldo Atual
    if resultado:
        print(10 * "=")
        print(f"Saldo atual: R$ {resultado[0]:.2f}")
        print(10 * "=")
    else:
        print("CPF não encontrado.")

    # Fecha a conexão com o banco de dados e volta para o menu
    conexao_db.close()
    Menu.menu(cpf)

# Função para depositar dinheiro
def depositar(cpf):
    # Cria conexão com o banco e configura o cursor para executar os comando SQL
    conexao_db = conexao()
    cursor = conexao_db.cursor()

    print("=== Depositar ===")
    valor = float(input("Insira o valor: "))
    descricao = input("Adicionar descrição: ")

    # Puxa o saldo atual do CPF passado no parâmetro da função
    cursor.execute("SELECT saldo FROM usuarios WHERE cpf = ?", (cpf,))
    resultado = cursor.fetchone()

    # Atribui o saldo puxado do banco de dados a variavel
    saldo_atual = resultado[0]

    # Soma o saldo atual ao valor depositado
    novo_saldo = saldo_atual + valor

    # Define o tipo da transação
    tipo = "Depósito"

    # Define a data da operação
    data_operacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Executa o comando em SQL para guardar o novo valor no banco de dados através do cpf passado por parâmetro na função
    cursor.execute("UPDATE usuarios SET saldo = ? WHERE cpf = ?", (novo_saldo, cpf))
    conexao_db.commit()

    # Executa o comando em SQL que insere uma nova transação a tabela de transações que será usado para ver o extrato
    cursor.execute("INSERT INTO transacoes (cpf, tipo, valor, data_hora, descricao) VALUES (?, ?, ?, ?, ?)", (cpf, tipo, valor, data_operacao, descricao))
    conexao_db.commit()

    # Printa a mensagem de sucesso e mostra o saldo atual
    print("Depósito realizado com sucesso.")
    print(f'Saldo Atual: R$ {novo_saldo:.2f}\n')

    # Fecha a conexão com o banco de dados e retorna ao menu
    conexao_db.close()
    Menu.menu(cpf)

def sacar(cpf):
    # Cria conexão com o banco e configura o cursor para executar os comando SQL
    conexao_db = conexao()
    cursor = conexao_db.cursor()

    print("=== Sacar ===")
    valor = float(input("Insira o valor: "))

    # Puxa o saldo atual do CPF passado no parâmetro da função
    cursor.execute("SELECT saldo FROM usuarios WHERE cpf = ?", (cpf,))
    resultado = cursor.fetchone()

    # Atribui o resultado da busca a uma variavel
    saldo_atual = resultado[0]

    # Define a data da operação
    data_operacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Faz a verificação se há saldo suficiente
    if valor > saldo_atual:
        print("Saldo insuficiente")
    else:
        # Seta o novo saldo como o saldo atual menos o saque
        novo_saldo = saldo_atual - valor

        # Executa o comando que atualiza o saldo no banco de dados
        cursor.execute("UPDATE usuarios SET saldo = ? WHERE cpf = ?", (novo_saldo, cpf))
        conexao_db.commit()

        print("Saque realizado com sucesso.")
        print(f'Saldo Atual: R$ {novo_saldo:.2f}\n')

        # Define o tipo da transação
        tipo = "Saque"

        # Executa o comando em SQL que insere uma nova transação a tabela de transações que será usado para ver o extrato
        cursor.execute("INSERT INTO transacoes (cpf, tipo, valor, data_hora) VALUES (?, ?, ?, ?)",(cpf, tipo, valor, data_operacao))
        conexao_db.commit()


    # Fecha a conexão com o banco de dados e retorna ao menu
    conexao_db.close()
    Menu.menu(cpf)

def extrato(cpf):
    # Cria conexão com o banco e configura o cursor para executar os comando SQL
    conexao_db = conexao()
    cursor = conexao_db.cursor()

    # Puxa as informações que tem no banco de dados atribuiadas ao CPF passado no parâmetro da função
    cursor.execute("SELECT tipo, valor, data_hora, descricao FROM transacoes WHERE cpf = ?", (cpf,))
    resultado = cursor.fetchall()

    # Se tiver saldo vai entrar em um laço de repetição para mostrar todas as trnasações
    print("=== Extrato ===")
    if resultado:
        for linha in resultado:
            tipo, valor, data_hora, descricao = linha
            print(f'Tipo: {tipo}')
            print(f'Valor: R$ {valor:.2f}')
            print(f'Data: {data_hora}')
            print(f'Descrição: {descricao}')
            print("-" * 30)
    else:
        print("Nenhuma transação encontrada.")

    # Fecha a conexão com o banco de dados e retorna ao menu
    conexao_db.close()
    Menu.menu(cpf)

def transferir(cpf):
    # Cria conexão com o banco e configura o cursor para executar os comando SQL
    conexao_db = conexao()
    cursor = conexao_db.cursor()

    # Insere o valor a ser transferido e para quem será transferido
    print("=== Transferir ===")
    valor = float(input("Insira o valor: "))
    receptor = input("Digite o CPF da qual deseja enviar: ")

    # Busca no banco de dados o saldo atual da pessoa que esta enviando o dinheiro
    cursor.execute("SELECT saldo FROM usuarios WHERE cpf = ?", (cpf,))
    resultado = cursor.fetchone()

    # Atribui o resultado da busca a uma variavel
    saldo_atual = resultado[0]

    # Define a data da operação
    data_operacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Verificação se possui dinheiro suficiente para a transação
    if valor > saldo_atual:
        print("Dinheiro insuficiente\n")
        return
    else:
        # Seta o novo saldo de quem esta enviando, sendo seu saldo atual menos o valor que esta tranferindo
        novo_saldo = saldo_atual - valor

        # Atualizando o saldo ao banco de dados
        cursor.execute("UPDATE usuarios SET saldo = ? WHERE cpf = ?", (novo_saldo, cpf))
        conexao_db.commit()

        # Busca no banco de dados o saldo atual da pessoa que esta recebendo o dinheiro
        cursor.execute("SELECT saldo FROM usuarios WHERE cpf = ?", (receptor,))
        resultado = cursor.fetchone()

        # Atribuindo o resultado da busca a uma variavel
        saldo_atual = resultado[0]

        # Setando o novo saldo, sendo saldo atual mais o valor que esta recendo
        novo_valor = saldo_atual + valor

        # Atualizando no banco de dados o saldo atual de quem esta recebendo o dinheiro
        cursor.execute("UPDATE usuarios SET saldo = ? WHERE cpf = ?", (novo_valor, receptor))
        conexao_db.commit()

        tipo_envio = "Transferência enviada"
        tipo_recebido = "Transferência recebida"

        # Executa o comando em SQL que insere uma nova transação a tabela de transações de quem enviou
        cursor.execute("INSERT INTO transacoes (cpf, tipo, valor, data_hora) VALUES (?, ?, ?, ?)",(cpf, tipo_envio, valor, data_operacao))
        conexao_db.commit()

        # Executa o comando em SQL que insere uma nova transação a tabela de transações de quem recebeu
        cursor.execute("INSERT INTO transacoes (cpf, tipo, valor, data_hora) VALUES (?, ?, ?, ?)",(cpf, tipo_recebido, valor, data_operacao))
        conexao_db.commit()

        print("Transferência executada com sucesso!\n")

        # Fecha a conexão com o banco de dados e retorna ao menu
        conexao_db.close()
        Menu.menu(cpf)