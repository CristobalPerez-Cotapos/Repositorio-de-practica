from PyQt5.QtWidgets import (QLabel, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QProgressBar)
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QPixmap
from random import randint, uniform
from backend.logica_de_juego import Personaje, Objeto, Gorgory
import parametros as p


class Zona_de_juego(QLabel):

    def __init__(self, ruta_carpeta_mapa, personaje, ventana_juego):
        super().__init__()
        self.ventana_juego = ventana_juego
        self.ruta_carpeta_mapa = ruta_carpeta_mapa
        self.grilla = QGridLayout()
        self.dic_objetos = {}
        self.init_gui(ruta_carpeta_mapa)
        self.personaje = Personaje(personaje)

        self.agregar_personaje()
        self.hay_gorogry = False

    def init_gui(self,ruta_mapa):
        ruta_baldosas = ruta_mapa + "/Baldosa.png"
        pixeles_fondo = QPixmap(ruta_baldosas)
        pixeles_fondo = pixeles_fondo.scaled(p.X_BALDOSAS, p.Y_BALDOSAS, Qt.IgnoreAspectRatio)
        self.setPixmap(pixeles_fondo)
        self.setScaledContents(True)
        for i in range(p.ALTO_GRAVA):
            for j in range(p.ANCHO_GRAVA):
                a = uniform(0, 1)
                if a < p.PROBABILIDAD_OBSTACULO_INICIAL and (i != 0 and j != 0):
                    if not (isinstance(self.dic_objetos[i-1,j], Objeto)) \
                            and not (isinstance(self.dic_objetos[i, j-1], Objeto))\
                            and not (isinstance(self.dic_objetos[i -1, j-1], Objeto)):
                        b = randint(1, 3)
                        ruta_objeto = f"{self.ruta_carpeta_mapa}/Obstaculo{str(b)}.png"
                        label = Objeto(ruta_objeto, "obstaculo", self, (i, j))
                    else:
                        label = QLabel(self)
                else:
                    label = QLabel(self)
                self.dic_objetos[(i, j)] = label
                label.setScaledContents(True)
                self.grilla.addWidget(label, i, j)
        self.setLayout(self.grilla)
        self.resize(640, 480)

    def agregar_personaje(self):
        self.personaje.definir_zona(self, self.grilla)
        self.grilla.addWidget(self.personaje, 0, 0)

    def objetos_personaje(self):
        ruta_objetos = {0: p.CARPETA_OBJETOS+"/Veneno.png",
                        2: p.CARPETA_OBJETOS+"/Corazon.png"}
        if self.personaje.personaje == "Homero":
            objeto = "Dona"
        elif self.personaje.personaje == "Lisa":
            objeto = "Saxofon"
        elif self.personaje.personaje == "Moe":
            objeto = "Cerveza"
        elif self.personaje.personaje == "Krusty":
            objeto = "Krusty"
        ruta_objetos[1] = p.CARPETA_OBJETOS + "/" + objeto + ".png"
        ruta_objetos[3] = p.CARPETA_OBJETOS + "/" + objeto + "X2.png"
        return ruta_objetos

    def aparicion_objeto(self):
        prob = uniform(0, 1)
        creado = False
        contador = 0
        while not creado and contador < 500:
            contador += 1
            rand_x = randint(0, p.ANCHO_GRAVA - 1)
            rand_y = randint(0, p.ALTO_GRAVA - 1)
            if not isinstance(self.dic_objetos[(rand_y, rand_x)], Objeto)\
                    and not (self.personaje.y == rand_x and self.personaje.x == rand_y):
                if prob <= p.PROB_BUENO:
                    rand_bueno = randint(2, 3)
                    objeto = Objeto(self.objetos_personaje()[rand_bueno], "item", self, (rand_y, rand_x))
                    if rand_bueno == 2:
                        objeto.corazon = True
                    objeto.bueno = True
                    self.grilla.addWidget(objeto, rand_y, rand_x)
                    creado = True
                    self.dic_objetos[rand_y, rand_x] = objeto
                elif prob <= p.PROB_BUENO + p.PROB_VENENO:
                    objeto = Objeto(self.objetos_personaje()[0], "item", self, (rand_y, rand_x))
                    objeto.malo = True
                    self.grilla.addWidget(objeto, rand_y, rand_x)
                    creado = True
                    self.dic_objetos[rand_y, rand_x] = objeto
                elif prob <= p.PROB_BUENO + p.PROB_VENENO + p.PROB_NORMAL:
                    objeto = Objeto(self.objetos_personaje()[1], "item", self, (rand_y, rand_x))
                    self.grilla.addWidget(objeto, rand_y, rand_x)
                    creado = True
                    self.dic_objetos[rand_y, rand_x] = objeto
        if self.personaje.personaje == "Lisa":
            self.personaje.habilidad_especial()
        if contador == 500:
            self.ventana_juego.timer_aparicion.stop()

    def agrgar_gorgory(self):
        self.gorgory = Gorgory("Gorgory", self.ventana_juego.movimientos_realizados, self, self.grilla)
        self.grilla.addWidget(self.gorgory, 0, 0)
        self.hay_gorogry = True
