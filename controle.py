from PyQt5 import uic,QtWidgets
import pyodbc

server = 'localhost\\SQLEXPRESS'  # Nome do servidor (inclui o nome da instância)
database = 'cadastro'             # Nome do banco de dados
username = 'cadastropublic'                 # Usuário (ex: sa, se estiver usando autenticação do SQL Server)
password = 'cadastro123'                      # Senha

def funcao_principal():

    # Lê o texto dentro dos campos e armazena nas variaveis
    textoCampoCodigo = formulario.campoCodigo.text()
    textoCampoDescricao = formulario.campoDescricao.text()
    textoCampoPreco = formulario.campoPreco.text()
    categoria = ""
    
    if formulario.opcaoInformatica.isChecked():
        categoria = "Informática"
    elif formulario.opcaoAlimentos.isChecked():
        categoria = "Alimentos"
    elif formulario.opcaoLimpeza.isChecked():
        categoria = "Limpeza"
    
    
    # Insere as informações no banco de dados
    try:
        comando_SQL = "INSERT INTO produtos (codigo, descricao, preco, categoria) VALUES (?, ?, ?, ?)"
        dados = (int(textoCampoCodigo), textoCampoDescricao, float(textoCampoPreco), categoria)
        cursor.execute(comando_SQL, dados)
        conn.commit()
    except pyodbc.Error as e:
        print("Erro ao inserir produto:", e)


try:
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=yes;"
        )
    cursor = conn.cursor()
    cursor.execute("IF NOT EXISTS(SELECT * from sys.databases where name = 'cadastro') BEGIN CREATE DATABASE cadastro END")
    
    cursor.execute("IF NOT EXISTS(SELECT * from sysobjects where name = 'produtos' AND xtype = 'U') BEGIN CREATE TABLE produtos (id INT IDENTITY(1,1) PRIMARY KEY,codigo INT NOT NULL,descricao TEXT NOT NULL,preco DECIMAL(10,2) NOT NULL,categoria VARCHAR(20) NOT NULL)END")
    app = QtWidgets.QApplication([])
    formulario = uic.loadUi("formulario.ui")
    formulario.botaoSalvar.clicked.connect(funcao_principal)

    formulario.show()
    app.exec()

except pyodbc.Error as e:
    print("Erro ao conectar:", e)
finally:
    if 'conn' in locals() and conn:
        conn.close()  # Certifique-se de fechar a conexão





    

