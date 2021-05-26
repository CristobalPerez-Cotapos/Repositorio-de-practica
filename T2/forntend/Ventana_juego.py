from PyQt5.QtWidgets import (QLabel, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from random import randint
from backend.logica_de_juego import Personaje, Objeto


class Ventana_juego(QWidget):

    def __init__(self, ruta_mapa, ruta_personaje, ancho, alto):
        super().__init__()
        self.size = (ancho, alto)
        self.setWindowTitle("Ventana de juego")
        self.resize(ancho, alto)
        self.ruta_mapa = ruta_mapa
        self.ruta_personaje = ruta_personaje
        self.init_gui(ruta_mapa, ruta_personaje)
        self.setGeometry(200,25, ancho, alto)

    def init_gui(self, ruta_mapa, ruta_personaje):
        vbox = QVBoxLayout()
        ruta_baldosa = ruta_mapa+"/Baldosa.png"
        ruta_fondo = ruta_mapa + "/Fondo.png"
        fondo = QLabel("", self)
        pixles_fondo = QPixmap(ruta_fondo)
        fondo.setPixmap(pixles_fondo)
        fondo.setScaledContents(True)
        hbox = QHBoxLayout()
        hbox.addWidget(fondo)
        self.zona = Zona_de_juego(ruta_mapa)
        vbox.addLayout(hbox)
        vbox.addWidget(self.zona)
        self.setLayout(vbox)

    def keyPressEvent(self, evento):
        if evento.text() == "w":
            self.zona.personaje.moverse("arriba")
        elif evento.text() == "a":
            self.zona.personaje.moverse("izquierda")
        elif evento.text() == "d":
            self.zona.personaje.moverse("derecha")
        elif evento.text() == "s":
            self.zona.personaje.moverse("abajo")


class Zona_de_juego(QLabel):

    def __init__(self, ruta_mapa):
        super().__init__()
        self.ruta_mapa = ruta_mapa
        self.grilla = QGridLayout()
        self.dic_objetos = {}
        self.init_gui(ruta_mapa)
        self.personaje = Personaje("Homero", self.grilla, self)
        self.agregar_personaje()


    def init_gui(self,ruta_mapa):
        ruta_baldosas = "forntend/assets/sprites/Mapa/Planta_nuclear/Baldosa.png"
        self.setPixmap(QPixmap(ruta_baldosas))
        self.setScaledContents(True)
        for i in range(8):
            for j in range(12):
                a = randint(1,100)
                if a < 5:
                    label = Objeto(ruta_mapa + "/Obstaculo1.png", "obstaculo")
                elif 5 < a < 8:
                    label = Objeto("forntend/assets/sprites/Objetos/Cerveza.png", "item")
                else:
                    label = QLabel(self)
                self.dic_objetos[(i,j)] = label
                self.grilla.addWidget(label, i, j)
        self.setLayout(self.grilla)

    def agregar_personaje(self):
        self.grilla.addWidget(self.personaje, 0, 0)







