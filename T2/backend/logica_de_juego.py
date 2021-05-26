from PyQt5.QtWidgets import (QLabel, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from random import randint
import PyQt5
import parametros as p


class Personaje(QLabel):

    def __init__(self, personaje, grilla, zona):
        super().__init__()
        self.personaje = personaje
        self.init_gui()
        self.grilla = grilla
        self.x = 0
        self.y = 0
        self.zona = zona
        self.items = []

    def init_gui(self):
        pixles = QPixmap("forntend/assets/sprites/Personajes/Homero/down_1.png")
        pixeles2 = pixles.scaled(60, 60, Qt.KeepAspectRatio)
        self.setPixmap(pixeles2)

    def moverse(self, direccion):
        if direccion == "arriba":
            if 0 < self.x:
                if type(self.zona.dic_objetos[(self.x - 1, self.y)]) == Objeto:
                    self.colision(self.zona.dic_objetos[(self.x - 1, self.y)])
                    if self.zona.dic_objetos[(self.x - 1, self.y)].tipo == "item":
                        self.x -= 1
                        self.grilla.addWidget(self, self.x, self.y)
                else:
                    self.x -= 1
                    self.grilla.addWidget(self, self.x, self.y)

        elif direccion == "abajo":
            if 7 > self.x:
                if type(self.zona.dic_objetos[(self.x + 1, self.y)]) == Objeto:
                    self.colision(self.zona.dic_objetos[(self.x + 1, self.y)])
                    if self.zona.dic_objetos[(self.x + 1, self.y)].tipo == "item":
                        self.x += 1
                        self.grilla.addWidget(self, self.x, self.y)
                else:
                    self.x += 1
                    self.grilla.addWidget(self, self.x, self.y)

        elif direccion == "izquierda":
            if 0 < self.y:
                if type(self.zona.dic_objetos[(self.x, self.y - 1)]) == Objeto:
                    self.colision(self.zona.dic_objetos[(self.x, self.y - 1)])
                    if self.zona.dic_objetos[(self.x, self.y - 1)].tipo == "item":
                        self.y -= 1
                        self.grilla.addWidget(self, self.x, self.y)
                else:
                    self.y -= 1
                    self.grilla.addWidget(self, self.x, self.y)

        elif direccion == "derecha":
            if 11 > self.y:
                if type(self.zona.dic_objetos[(self.x, self.y + 1)]) == Objeto:
                    self.colision(self.zona.dic_objetos[(self.x, self.y + 1)])
                    if self.zona.dic_objetos[(self.x, self.y + 1)].tipo == "item":
                        self.y += 1
                        self.grilla.addWidget(self, self.x, self.y)
                else:
                    self.y += 1
                    self.grilla.addWidget(self, self.x, self.y)

    def colision(self, objeto):
        if objeto.tipo == "obstaculo":
            pass
        elif objeto.tipo == "item" and not objeto.recogido:
            self.items.append(objeto)
            objeto.recogido = True
            objeto.hide()
            print(self.items)
            label = QLabel("", self.zona)
            self.grilla.addWidget(label, self.x, self.y)
            self.grilla.addWidget(self, self.x, self.y)

    def animacion(self, direccion):
        if direccion == "arriba":
            pass
        if direccion == "arriba":
            pass
        if direccion == "arriba":
            pass
        if direccion == "arriba":
            pass

    @property
    def carpeta_personaje(self):
        if self.personaje == "Homero":
            return p.RUTA_SPRITES_HOMERO
        elif self.personaje == "Lisa":
            return p.RUTA_SPRITES_LISA
        elif self.personaje == "Moe":
            return p.RUTA_SPRITES_MOE
        elif self.personaje == "Krusty":
            return p.RUTA_SPRITES_KRUSTY
        elif self.personaje == "Gorgory":
            return p.RUTA_SPRITES_GORGORY

    @property
    def velocidad(self):
        if self.personaje == "Homero":
            return p.VELOCIDAD_HOMERO
        elif self.personaje == "Lisa":
            return p.VELOCIDAD_LISA
        elif self.personaje == "Moe":
            return p.VELOCIDAD_MOE
        elif self.personaje == "Krusty":
            return p.VELOCIDAD_KRUSTY
        elif self.personaje == "Gorgory":
            return p.VELOCIDAD_GORGORY

class Objeto(QLabel):

    def __init__(self, ruta, tipo):
        super().__init__()
        self.init_gui(ruta)
        self.tipo = tipo
        self.recogido = False

    def init_gui(self, ruta):
        pixles = QPixmap(ruta)
        pixeles2 = pixles.scaled(60, 60, Qt.KeepAspectRatio)
        self.setPixmap(pixeles2)
