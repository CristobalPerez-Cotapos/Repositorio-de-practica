from PyQt5.QtWidgets import (QLabel, QWidget, QLineEdit, QVBoxLayout,
                             QPushButton)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
import parametros as p
from backend.logica_de_juego import Personaje
from backend.logica_musica import Musica


class VentanaInicio(QWidget):
    senal_enviar_nombre = pyqtSignal(dict)
    senal_ver_mejores = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.size = (p.ANCHO, p.LARGO)
        self.resize(p.ANCHO, p.LARGO)
        self.setGeometry(p.x, p.y, p.LARGO, p.ANCHO)
        self.setWindowTitle("Ventana de inicio")
        self.init_gui(p.RUTA_LOGO)

    def init_gui(self, ruta_logo):
        self.imagen = QLabel(self)
        pixeles = QPixmap(ruta_logo)
        pixeles2 = pixeles.scaled(600, 600, Qt.KeepAspectRatio)
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
        self.musica = Musica()
        self.musica.comenzar()
        self.setLayout(layout)

    def enviar_nombre(self):
        if "," in self.line.text() or len(self.line.text()) == 0:
            self.line.clear()
            self.line.setPlaceholderText("Nombre invalido")
        else:
            self.musica.cancion.stop()
            self.hide()
            homero = Personaje("Homero")
            lisa = Personaje("Lisa")
            moe = Personaje("Moe")
            krusty = Personaje("Krusty")
            dicionario_preparacion = {
                "nombre_jugador": self.line.text(),
                "homero": homero,
                "lisa": lisa,
                "moe": moe,
                "krusty": krusty
            }
            self.senal_enviar_nombre.emit(dicionario_preparacion)

    def ver_mejores(self):
        self.hide()
        self.musica.cancion.stop()
        self.senal_ver_mejores.emit()

    def mostrarse(self):
        self.show()
        self.musica = Musica()
        self.musica.comenzar()
