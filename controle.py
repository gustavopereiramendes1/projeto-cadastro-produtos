from PyQt5 import uic,QtWidgets, QtGui
import pyodbc
from reportlab.pdfgen import canvas
from lib.janela_dialogos import *

server = 'localhost\\SQLEXPRESS'  # Nome do servidor (inclui o nome da instância)
database = 'cadastro'             # Nome do banco de dados
username = 'gustavo'                 # Usuário (ex: sa, se estiver usando autenticação do SQL Server)
password = '000gustavo'                      # Senha

def salvar_dados():
    try:
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
            
        if not textoCampoCodigo.isdigit() or textoCampoDescricao == '' or textoCampoPreco == '':
            raise ValueError("O código deve conter apenas dígitos.")
        # Insere as informações no banco de dados
    
        comando_SQL = "exec SP_adicionar_produtos ?, ?, ?, ?"
        dados = (int(textoCampoCodigo), textoCampoDescricao, float(textoCampoPreco), categoria)
        cursor.execute(comando_SQL, dados)
        conn.commit()
        
    except pyodbc.Error as e:
        exibir_erro(formulario, "Erro ao inserir o produto")

    except ValueError as v:
        exibir_erro(formulario, "Campos Vazios ou Inválidos")
        
    formulario.campoCodigo.setText("")
    formulario.campoDescricao.setText("")
    formulario.campoPreco.setText("")

def gerar_pdf(dados_informacoes = []):

    file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            lista_de_dados,
            "Salvar PDF",  # Título da janela
            "Salvos",            # Diretório inicial
            "PDF Files (*.pdf)"  # Filtro de arquivo
        )
    
    if not file_path:  # Usuário cancelou a ação
            return

        # Certifique-se de que o arquivo tenha a extensão .pdf
    if not file_path.endswith(".pdf"):
        file_path += ".pdf"
    
    pdf = canvas.Canvas(file_path)
    
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Produtos cadastrados: ")
    pdf.setFont("Times-Bold", 15)
    pdf.drawString(10, 750, "ID")
    pdf.drawString(110, 750, "CÓDIGO")
    pdf.drawString(210, 750, "DESCRIÇÃO")
    pdf.drawString(310, 750, "PREÇO")
    pdf.drawString(410, 750, "CATEGORIA")
    y = 0
    x = 0
    for i in range(0, len(dados_informacoes)):
        x = 0
        y = y + 50
        for j in range(0, 5):
            pdf.drawString(10 + x, 750 - y, str(dados_informacoes[i][j]))
            x = x + 100
    pdf.save()
    exibir_sucesso(lista_de_dados, "Salvo com Sucesso!")
    
def excluir_dados(dados_tabela = []):
    linha = None
    try:
        linha = lista_de_dados.tabela.currentRow()
        
        if linha == -1:
            exibir_erro(listar_dados, "Nenhuma linha selecionada")
            return
        valor_id = dados_tabela[linha][0]
        lista_de_dados.tabela.removeRow(linha)
        comando_SQL = "DELETE FROM produtos WHERE id=" + str(valor_id)
        cursor.execute(comando_SQL)
        conn.commit()
        
    except IndexError as i:
        exibir_erro(listar_dados, "Nenhuma linha selecionada")

def listar_dados():
    
    #Mostrando a janela com a lista dos dados
    lista_de_dados.move(formulario.pos().x(),formulario.pos().y())
    lista_de_dados.show()
    formulario.hide()
    
    
    #Lendo os dados da tabela
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    
    #Criando a tabela de dados
    lista_de_dados.tabela.setRowCount(len(dados_lidos))
    lista_de_dados.tabela.setColumnCount(5)
    lista_de_dados.tabela.setEditTriggers(lista_de_dados.tabela.NoEditTriggers)
    
    #Inserindo os dados na tabela da janela
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            lista_de_dados.tabela.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
    
    #Evento para voltar para a tela de cadastro, clicando no botão "Voltar"
    
    try:
        lista_de_dados.botaoVoltar.clicked.disconnect()
    except TypeError:
        pass  # Ignorar erro se o botão não estiver conectado
    lista_de_dados.botaoVoltar.clicked.connect(voltar_telaCadastro)
    
    try:
        lista_de_dados.botaoPDF.clicked.disconnect()
    except TypeError:
        pass
    lista_de_dados.botaoPDF.clicked.connect(lambda: gerar_pdf(dados_lidos))
    
    try:
        lista_de_dados.botaoRemover.clicked.disconnect()
    except TypeError:
        pass
    lista_de_dados.botaoRemover.clicked.connect(lambda: excluir_dados(dados_lidos))
        
    
def voltar_telaCadastro():
        formulario.show()
        lista_de_dados.hide()
        
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
    app.setWindowIcon(QtGui.QIcon("icons/icon_main.png"))
    
    formulario = uic.loadUi("formulario.ui")
    formulario.setWindowTitle("Cadastrar Produtos")
    lista_de_dados = uic.loadUi("listar_dados.ui")
    lista_de_dados.setWindowTitle("Lista de Produtos")
    formulario.botaoSalvar.clicked.connect(salvar_dados)
    formulario.botaoListar.clicked.connect(listar_dados)
    formulario.show()
    
    app.exec()

except pyodbc.Error as e:
    print("Erro ao conectar:", e)
finally:
    if 'conn' in locals() and conn:
        conn.close()  # Certifique-se de fechar a conexão





    

