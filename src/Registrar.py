from datetime import datetime
import Login
from Data import conexao
import re


# Função para verificar se as duas senhas cadastradas estão iguais
def verify_password(password, confirm_password):
    if password != confirm_password:
        print("Senhas diferentes")
        return False
    return True


# Função para verificar se o CPF está no formato correto e válido
def verify_cpf(cpf):
    padrao = r"^\d{3}[.]\d{3}[.]\d{3}[-]\d{2}$"
    if not re.match(padrao, cpf):
        print("CPF não foi escrito corretamente")
        return False

    # Remove pontos e traço
    cpf_numerico = re.sub(r'\D', '', cpf)

    # Verifica se todos os dígitos são iguais (caso clássico de CPF inválido)
    if cpf_numerico == cpf_numerico[0] * 11:
        print("CPF inválido")
        return False

    # Cálculo do primeiro dígito verificador
    soma = sum(int(cpf_numerico[i]) * (10 - i) for i in range(9))
    digito1 = 11 - (soma % 11)
    digito1 = digito1 if digito1 < 10 else 0

    # Cálculo do segundo dígito verificador
    soma = sum(int(cpf_numerico[i]) * (11 - i) for i in range(10))
    digito2 = 11 - (soma % 11)
    digito2 = digito2 if digito2 < 10 else 0

    if int(cpf_numerico[9]) == digito1 and int(cpf_numerico[10]) == digito2:
        print("CPF válido")
        return True
    else:
        print("CPF inválido")
        return False


# Função para calcular o dígito verificador do RG
def calcular_digito_rg(rg_numeros):
    pesos = [2, 3, 4, 5, 6, 7, 8, 9]
    soma = sum(int(d) * p for d, p in zip(reversed(rg_numeros), pesos))
    resto = soma % 11
    if resto == 10:
        return 'X'
    else:
        return str(resto)


# Função para verificar se o RG está no formato correto e válido
def verify_rg(rg):
    # Remove caracteres não numéricos (exceto o dígito verificador)
    rg = rg.upper().replace(".", "").replace("-", "")

    if len(rg) != 9:
        print("RG inválido (formato incorreto)")
        return False

    rg_numeros = rg[:-1]
    verificador = rg[-1]

    if not rg_numeros.isdigit():
        print("RG inválido (formato incorreto)")
        return False

    digito_calculado = calcular_digito_rg(rg_numeros)

    if digito_calculado == verificador:
        print("RG válido")
        return True
    else:
        print("RG inválido (dígito verificador incorreto)")
        return False


# Função para criar um novo usuário
def registro():
    print("\nSeja bem-vindo!\n")
    print("Vamos criar a sua conta no melhor banco dos programadores!")
    print("Vamos precisar de algumas informações para começar!\n")

    user_name = input("Nome completo: ")

    # Laço que garante que o RG será inserido corretamente
    while True:
        rg = input("Insira seu RG (com dígito verificador): ")
        if verify_rg(rg):
            break

    # Laço que garante que o CPF será inserido corretamente
    while True:
        cpf = input("Digite seu CPF (formato xxx.xxx.xxx-xx): ")
        if verify_cpf(cpf):
            break

    # Cria conexão com o banco e configura o cursor para executar os comandos SQL
    conexao_db = conexao()
    cursor = conexao_db.cursor()

    # Verifica se o CPF já está cadastrado no banco
    cursor.execute("SELECT * FROM usuarios WHERE cpf = ?", (cpf,))
    if cursor.fetchone():
        print("\nErro: CPF já cadastrado.")
        print("Faça o login\n")
        Login.login()
        conexao_db.close()
        return

    # Não funciona enquanto as duas senhas não forem iguais
    while True:
        password = input("Insira uma senha: ")
        confirm_password = input("Confirme a senha: ")

        if verify_password(password, confirm_password):
            break
        else:
            print("Tente novamente\n")

    print("\nConta criada com sucesso.")
    print(f"Seja bem-vindo {user_name}\n")

    # Atribui a data de criação da conta e valor inicial
    data_criacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    saldo_inicial = 0.0

    # Comando que executa a criação do usuário no banco de dados
    cursor.execute(
        "INSERT INTO usuarios (nome_usuario, senha, rg, cpf, data_criacao, saldo) VALUES (?, ?, ?, ?, ?, ?)",
        (user_name, password, rg, cpf, data_criacao, saldo_inicial)
    )

    # Executa os comandos e fecha o menu
    conexao_db.commit()
    conexao_db.close()

    # Puxa a função Login (verifique se a importação está correta no seu script principal)
    Login.login()
