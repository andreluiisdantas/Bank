import Registrar
import Login

def inicio():
    print(
    r"""
                       Seja Bem-Vindo ao
 /$$$$$$$  /$$     /$$/$$$$$$$   /$$$$$$  /$$   /$$ /$$   /$$
| $$__  $$|  $$   /$$/ $$__  $$ /$$__  $$| $$$ | $$| $$  /$$/
| $$  \ $$ \  $$ /$$/| $$  \ $$| $$  \ $$| $$$$| $$| $$ /$$/ 
| $$$$$$$/  \  $$$$/ | $$$$$$$ | $$$$$$$$| $$ $$ $$| $$$$$/  
| $$____/    \  $$/  | $$__  $$| $$__  $$| $$  $$$$| $$  $$  
| $$          | $$   | $$  \ $$| $$  | $$| $$\  $$$| $$\  $$ 
| $$          | $$   | $$$$$$$/| $$  | $$| $$ \  $$| $$ \  $$
|__/          |__/   |_______/ |__/  |__/|__/  \__/|__/  \__/
    """)
    option = int(input("TELA INICIAL\n1. Entrar\n2. Criar Conta\n3. Sair\n\n"))
    return option

while True:
    option_chose = inicio()

    if option_chose == 3:
        print("Saindo...")
        print("Até a próxima!")
        break
    elif option_chose == 2:
        Registrar.registro()
    elif option_chose == 1:
        Login.login()

    else:
        print("Opção inválida! Tente novamente...\n\n")


