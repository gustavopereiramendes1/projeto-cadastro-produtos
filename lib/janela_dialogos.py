from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import sys
import winsound 


class SuccessDialog(QDialog):
    def __init__(self, mensagem):
        super().__init__()
        self.setWindowTitle("Salvo")
        self.setFixedSize(200, 150)  # Tamanho fixo da janela
        self.setWindowIcon(QIcon("icons/icon_Sucesso.png")) 

        # Reproduzir o som de sucesso do sistema
        winsound.MessageBeep(winsound.MB_ICONASTERISK)

        # Layout principal
        main_layout = QVBoxLayout()

        # Layout horizontal para o ícone e o texto
        h_layout = QHBoxLayout()
        h_layout.setSpacing(10)  # Define o espaçamento entre o ícone e o texto

        # Adicionando o ícone de sucesso
        icon_label = QLabel()
        icon_pixmap = QPixmap("icons/icon_Sucesso.png").scaled(48, 48)  # Ícone escalado
        icon_label.setPixmap(icon_pixmap)
        h_layout.addWidget(icon_label)

        # Adicionando a mensagem de sucesso
        mensagem_label = QLabel(mensagem)
        mensagem_label.setStyleSheet("font-size: 14px; color: #333;")
        mensagem_label.setWordWrap(True)
        mensagem_label.setAlignment(Qt.AlignVCenter)  # Centralizar verticalmente no layout horizontal
        h_layout.addWidget(mensagem_label)

        # Adiciona o layout horizontal ao layout principal
        main_layout.addLayout(h_layout)

        # Botão de fechar
        fechar_botao = QPushButton("Fechar")
        fechar_botao.setStyleSheet("""
            QPushButton {
                background-color: #5bc0de;
                color: white;
                font-size: 14px;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #31b0d5;
            }
        """)
        fechar_botao.clicked.connect(self.close)
        main_layout.addWidget(fechar_botao, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)


class ErrorDialog(QDialog):
    def __init__(self, mensagem):
        super().__init__()
        self.setWindowTitle("Erro")
        #self.setFixedSize(400, 200)  # Tamanho fixo da janela
        self.setWindowIcon(QIcon("icons/icon_Erro.png"))  # Ícone da janela

        # Reproduzir o som de erro do sistema
        winsound.MessageBeep(winsound.MB_ICONHAND)

        # Layout principal
        main_layout = QVBoxLayout()

        # Layout horizontal para o ícone e o texto
        h_layout = QHBoxLayout()
        h_layout.setSpacing(10)  # Define o espaçamento entre o ícone e o texto

        # Adicionando o ícone de erro
        icon_label = QLabel()
        icon_pixmap = QPixmap("icons/icon_Erro.png").scaled(32, 32)  # Ícone escalado
        icon_label.setPixmap(icon_pixmap)
        h_layout.addWidget(icon_label)

        # Adicionando a mensagem de erro
        mensagem_label = QLabel(mensagem)
        mensagem_label.setStyleSheet("font-size: 14px; color: #333;")
        mensagem_label.setWordWrap(True)
        mensagem_label.setAlignment(Qt.AlignVCenter)  # Centralizar verticalmente no layout horizontal
        h_layout.addWidget(mensagem_label)

        # Adiciona o layout horizontal ao layout principal
        main_layout.addLayout(h_layout)

        # Botão de fechar
        fechar_botao = QPushButton("Fechar")
        fechar_botao.setStyleSheet("""
            QPushButton {
                background-color: #d9534f;
                color: white;
                font-size: 14px;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
        """)
        fechar_botao.clicked.connect(self.close)
        main_layout.addWidget(fechar_botao, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

def exibir_sucesso(parent, mensagem):
    sucesso = SuccessDialog(mensagem)
    sucesso.exec_() #Mostra a janela de sucesso

def exibir_erro(parent, mensagem):
    erro = ErrorDialog(mensagem)
    erro.exec_()  # Mostra a janela como modal
