from PyQt5 import uic,QtWidgets
import pyodbc

server = 'localhost\\SQLEXPRESS'  # Nome do servidor (inclui o nome da instância)
database = 'cadastro'             # Nome do banco de dados
username = 'gustavo'                 # Usuário (ex: sa, se estiver usando autenticação do SQL Server)
password = '000gustavo'                      # Senha

def salvar_dados():

    # Lê o texto dentro dos campos e armazena nas variaveis
    textoCampoCodigo = formulario.campoCodigo.text()
    textoCampoDescricao = formulario.campoDescricao.text()
    textoCampoPreco = formulario.campoPreco.text()
    textoCampoPreco =  float(textoCampoPreco.replace(",", '.'))
    categoria = ""
    
    if formulario.opcaoInformatica.isChecked():
        categoria = "Informática"
    elif formulario.opcaoAlimentos.isChecked():
        categoria = "Alimentos"
    elif formulario.opcaoLimpeza.isChecked():
        categoria = "Limpeza"
    
    
    # Insere as informações no banco de dados
    try:
        comando_SQL = "exec SP_adicionar_produtos ?, ?, ?, ?"
        dados = (int(textoCampoCodigo), textoCampoDescricao, float(textoCampoPreco), categoria)
        cursor.execute(comando_SQL, dados)
        conn.commit()
        
    except pyodbc.Error as e:
        print("Erro ao inserir produto:", e)
        
    formulario.campoCodigo.setText("")
    formulario.campoDescricao.setText("")
    formulario.campoPreco.setText("")

def listar_dados():
    lista_de_dados.show()
    formulario.close()
    
    
    #Lendo os dados da tabela
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    
    lista_de_dados.tabela.setRowCount(len(dados_lidos))
    lista_de_dados.tabela.setColumnCount(5)
    lista_de_dados.tabela.setEditTriggers(lista_de_dados.tabela.NoEditTriggers)
    
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            lista_de_dados.tabela.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
    
    
    lista_de_dados.botaoVoltar.clicked.connect(voltar_telaCadastro)
        
    
def voltar_telaCadastro():
        formulario.show()
        lista_de_dados.close()
        
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
    lista_de_dados = uic.loadUi("listar_dados.ui")
    formulario.botaoSalvar.clicked.connect(salvar_dados)
    formulario.botaoListar.clicked.connect(listar_dados)
    formulario.show()
    
    app.exec()

except pyodbc.Error as e:
    print("Erro ao conectar:", e)
finally:
    if 'conn' in locals() and conn:
        conn.close()  # Certifique-se de fechar a conexão





    

