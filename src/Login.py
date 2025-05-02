import Menu
from Data import conexao

def verify_register(cpf, password):
    conexao_db = conexao()
    cursor = conexao_db.cursor()

    cursor.execute("SELECT EXISTS(SELECT 1 FROM usuarios WHERE cpf = ? AND senha = ?)", (cpf, password))
    resultado = cursor.fetchone()[0]

    conexao_db.close()

    if resultado == 1:
        print("Entrando...")
        Menu.menu(cpf)  # Chama o menu após login bem-sucedido
    else:
        print("Dados incorretos")

def login():
    print("Seja bem-vindo de volta!")
    cpf = input("Digite seu CPF: ")
    password = input("Digite a senha: ")

    verify_register(cpf, password)
