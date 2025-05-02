import sqlite3

# Função que faz a conexão com o banco de dados e será utilizado nas outras páginas
def conexao():
    return sqlite3.connect('Banco.db')

# Função para criar as tabelas do banco de dados
def criar_tabelas():
    # Cria conexão com o banco e configura o cursor para executar os comando SQL
    conexao_db = conexao()
    cursor = conexao_db.cursor()

    # Comando para criar a tabela de usuários
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios ( 
            id INTEGER PRIMARY KEY, 
            nome_usuario TEXT NOT NULL, 
            senha TEXT NOT NULL,
            rg TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            data_criacao TEXT NOT NULL,
            saldo REAL
        )
        """
    )

    # Comando para criar a tabela de histórico de transações
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY, 
            cpf TEXT NOT NULL,
            tipo TEXT NOT NULL, 
            valor REAL NOT NULL,
            data_hora TEXT NOT NULL,
            descricao TEXT,
            FOREIGN KEY (cpf) REFERENCES usuarios(cpf)
        )
        """
    )

    conexao_db.commit()
    conexao_db.close()

criar_tabelas()
