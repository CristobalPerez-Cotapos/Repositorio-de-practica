from PyQt5.QtWidgets import (QLabel, QWidget, QLineEdit, QVBoxLayout,
                             QPushButton)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap



class VentanaInicio(QWidget):
    senal_enviar_nombre = pyqtSignal(str)
    senal_ver_mejores = pyqtSignal()

    def __init__(self, ancho, alto, ruta_logo):
        super().__init__()
        self.size = (ancho, alto)
        self.resize(ancho, alto)
        self.setWindowTitle("Ventana de inicio")
        self.init_gui(ruta_logo)

    def init_gui(self, ruta_logo):
        self.imagen = QLabel(self)
        pixeles = QPixmap(ruta_logo)
        pixeles2 = pixeles.scaled(600, 600 , Qt.KeepAspectRatio)
        self.imagen.setPixmap(pixeles2)
        self.imagen.setScaledContents(True)

        self.escribe_nombre = QLabel("Escribe tu nombre de usuario:", self)
        self.line = QLineEdit("", self)

        self.boton_nueva_partida = QPushButton("Iniciar nueva partida", self)
        self.boton_nueva_partida.clicked.connect(self.enviar_nombre)
        self.boton_ver_mejores = QPushButton("Ver mejores puntuaciones", self)
        self.boton_ver_mejores.clicked.connect(self.ver_mejores)

        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.imagen)
        layout.addWidget(self.escribe_nombre)
        layout.addWidget(self.line)
        layout.addWidget(self.boton_nueva_partida)
        layout.addWidget(self.boton_ver_mejores)
        layout.addStretch(1)

        self.setLayout(layout)

    def enviar_nombre(self):
        if "," in self.line.text():
            self.line.clear()
            self.line.setPlaceholderText("Nombre invalido")
        else:
            self.senal_enviar_nombre.emit(self.line.text())

    def ver_mejores(self):
        self.senal_ver_mejores.emit()
