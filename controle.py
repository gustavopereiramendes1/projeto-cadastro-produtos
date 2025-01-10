from PyQt5 import uic,QtWidgets, QtGui
import pyodbc
from reportlab.pdfgen import canvas
from lib.janela_dialogos import *
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

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
        categoria = formulario.campoCategoria.text()
        
        """
        categoria = ""
        
         if formulario.opcaoInformatica.isChecked():
            categoria = "Informática"
        elif formulario.opcaoAlimentos.isChecked():
            categoria = "Alimentos"
        elif formulario.opcaoLimpeza.isChecked():
            categoria = "Limpeza" """      #Codigo antigo quando utilizava RADIO BUTTON
            
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
    formulario.campoCategoria.setText("")

def gerar_pdf(dados):
    largura, altura = A4
    espacamento_linha = 20 
    largura_colunas = [50, 100, 200, 100, 100]
    margem = 50
    colunas = ["ID", "Código", "Descrição", "Preço", "Categoria"]
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
    
    pdf = canvas.Canvas(file_path, pagesize=A4)
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Produtos cadastrados: ")
    
    def desenhar_cabecalho(y):
        x = margem
        for i, nome_coluna in enumerate(colunas):
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(x, y, nome_coluna)
            x += largura_colunas[i]
    def desenhar_linhas(y, dados_pagina):
        for linha in dados_pagina:
            x = margem
            for i, dado in enumerate(linha):
                pdf.setFont("Helvetica", 9)
                pdf.drawString(x, y, str(dado))
                x += largura_colunas[i]
            y -= espacamento_linha
        return y
    y = altura - 100  # Posição inicial da primeira linha
    dados_por_pagina = int((altura - 150) // espacamento_linha)
    paginas = [dados[i:i + dados_por_pagina] for i in range(0, len(dados), dados_por_pagina)]

    for pagina in paginas:
        desenhar_cabecalho(y)
        y -= espacamento_linha
        y = desenhar_linhas(y, pagina)
        pdf.showPage()  # Nova página
        y = altura - 100  # Resetando o início da próxima página

    pdf.save()
    exibir_sucesso(lista_de_dados, "Salvo com Sucesso!")

def atualizar_lista(dados_lidos):
    
    
    #Criando a tabela de dados
    lista_de_dados.tabela.setRowCount(len(dados_lidos))
    lista_de_dados.tabela.setColumnCount(5)
    lista_de_dados.tabela.setEditTriggers(lista_de_dados.tabela.NoEditTriggers)
    
    #Inserindo os dados na tabela da janela
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            lista_de_dados.tabela.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    
def excluir_dados(dados_tabela = []):
    linha = None
    try:
        linha = lista_de_dados.tabela.currentRow()
        
        if linha == -1:
            exibir_erro(listar_dados, "Nenhuma linha selecionada")
            return
        valor_id = lista_de_dados.tabela.item(linha, 0).text()
        lista_de_dados.tabela.removeRow(linha)
        comando_SQL = "DELETE FROM produtos WHERE id=" + str(valor_id)
        cursor.execute(comando_SQL)
        conn.commit()
        
    except IndexError as i:
        exibir_erro(listar_dados, "Nenhuma linha selecionada")

def menu_editar_dados(dados_tabela=[]):
    
    try:
        linha = lista_de_dados.tabela.currentRow()
        if linha == -1:
            exibir_erro(listar_dados, "Nenhuma linha selecionada")
            return
        #valor_id = dados_tabela[linha][0]
        valor_id = lista_de_dados.tabela.item(linha, 0).text()
        
        comando_SQL = "SELECT codigo, descricao, preco, categoria FROM produtos where id=" + str(valor_id)
        cursor.execute(comando_SQL)
        dados = cursor.fetchall()
        
        menu_editar.campoCodigo.setText(str(dados[0][0]))
        menu_editar.campoDescricao.setText(dados[0][1])
        menu_editar.campoPreco.setText(str(dados[0][2]))
        menu_editar.campoCategoria.setText(dados[0][3])
        
    except IndexError:
        exibir_erro(listar_dados, "Nenhuma linha selecionada")
        return

    menu_editar.show()
    try:
        menu_editar.botaoSalvar.clicked.disconnect()
    except TypeError:
        pass
    menu_editar.botaoSalvar.clicked.connect(lambda: editar_dados(valor_id))

def editar_dados(valor_id_dado=-1):
    if valor_id_dado == -1:
        exibir_erro(menu_editar, "Nenhuma linha selecionada")
        return

    
    
    try:
        textoCampoCodigo = int(menu_editar.campoCodigo.text())
        textoCampoDescricao = menu_editar.campoDescricao.text()
        textoCampoPreco = menu_editar.campoPreco.text()
        textoCampoCategoria = menu_editar.campoCategoria.text()

        # Convertendo o preço
        textoCampoPreco = float(textoCampoPreco.replace(",", "."))

        # Alterando os dados no BD
        comando_SQL = "UPDATE produtos SET codigo = ?, descricao = ?, preco = ?, categoria = ? WHERE id = ?"
        dados = (textoCampoCodigo, textoCampoDescricao, textoCampoPreco, textoCampoCategoria, valor_id_dado)
        cursor.execute(comando_SQL, dados)
        conn.commit()

        exibir_sucesso(menu_editar, "Dados alterados com sucesso.")
        menu_editar.close()
        
        comando_SQL = "SELECT * FROM produtos"
        cursor.execute(comando_SQL)
        dados_lidos = cursor.fetchall()
        atualizar_lista(dados_lidos)
        
        return
    except ValueError:
        exibir_erro(menu_editar, "Os campos devem estar preenchidos corretamente.")
    except Exception as e:
        exibir_erro(menu_editar, f"Erro ao editar dados: {str(e)}")
        
def filtrar_dados(dados_lidos = []):
    texto = lista_de_dados.campoPesquisar.text().lower()
    dados_filtrados = [
        linha for linha in dados_lidos
        if any(texto in str(celula).lower() for celula in linha)
    ]
    atualizar_lista(dados_filtrados)
    

def listar_dados():
    
    #Mostrando a janela com a lista dos dados
    lista_de_dados.move(formulario.pos().x(),formulario.pos().y())
    lista_de_dados.show()
    formulario.hide()
    
    
    #Lendo os dados da tabela
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    atualizar_lista(dados_lidos)
    
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
    
    try:
        lista_de_dados.botaoEditar.clicked.disconnect()
    except TypeError:
        pass
    lista_de_dados.botaoEditar.clicked.connect(lambda: menu_editar_dados(dados_lidos))
    
    try:
        lista_de_dados.campoPesquisar.textChanged.disconnect()
    except TypeError:
        pass
    lista_de_dados.campoPesquisar.textChanged.connect(lambda: filtrar_dados(dados_lidos))
        
    
def voltar_telaCadastro():
        formulario.show()
        lista_de_dados.hide()
      
#Conectando no BD e adicionando as janelas        
try:
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"TrustServerCertificate=yes;"
        f"Trusted_Connection=yes;"
        )
    cursor = conn.cursor()
    cursor.execute("IF NOT EXISTS(SELECT * from sys.databases where name = 'cadastro') BEGIN CREATE DATABASE cadastro END")
    
    cursor.execute("IF NOT EXISTS(SELECT * from sysobjects where name = 'produtos' AND xtype = 'U') BEGIN CREATE TABLE produtos (id INT IDENTITY(1,1) PRIMARY KEY,codigo INT NOT NULL,descricao TEXT NOT NULL,preco DECIMAL(10,2) NOT NULL,categoria VARCHAR(20) NOT NULL)END")
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon("icons/icon_main.png"))
    
    formulario = uic.loadUi("formulario.ui")
    lista_de_dados = uic.loadUi("listar_dados.ui")
    menu_editar = uic.loadUi("edita_dados.ui")
    formulario.setWindowTitle("Cadastrar Produtos")
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





    

