from PyQt5.QtWidgets import (QLabel, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,
                             QPushButton)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
import parametros as p


class Ventana_puntajes(QWidget):
    senal_vovler_puntajes = pyqtSignal()

    def __init__(self, ancho, alto):
        super().__init__()
        self.size = (ancho, alto)
        self.resize(ancho, alto)
        self.setWindowTitle("Ventana de puntajes")
        self.init_gui()

    def init_gui(self):
        self.setStyleSheet("background-color: yellow;")
        hbox = QHBoxLayout()
        self.imagen = QLabel(self)
        pixeles = QPixmap(p.RUTA_LOGO)
        pixeles2 = pixeles.scaled(100, 100, Qt.KeepAspectRatio)
        self.imagen.setPixmap(pixeles2)
        self.imagen.setScaledContents(True)
        self.texto = QLabel(self)
        self.texto.setText("Mejores puntajes")

        hbox.addWidget(self.texto)
        hbox.addWidget(self.imagen)

        self.puntajes = VboxPuntajes()

        self.boton_volver = QPushButton(self)
        self.boton_volver.setText("Volver")
        self.boton_volver.clicked.connect(self.boton_vovler_clikeado)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(hbox)
        self.vbox.addWidget(self.puntajes)
        self.vbox.addWidget(self.boton_volver)
        self.setLayout(self.vbox)

    def boton_vovler_clikeado(self):
        self.hide()
        self.senal_vovler_puntajes.emit()

    def actualzar_archivo(self, diccionario):
        archivo = open(p.RUTA_PUNTAJES, "r")
        antiguas_lineas = archivo.readlines()
        nueva_linea = diccionario["jugador"] + "," + str(diccionario["puntaje"])
        archivo.close()
        archivo = open(p.RUTA_PUNTAJES, "w")
        string_a_escribir = ""
        for i in antiguas_lineas:
            string_a_escribir += i
        string_a_escribir += "\n"
        string_a_escribir += nueva_linea
        archivo.write(string_a_escribir)
        archivo.close()

    def abrir_ventana(self):
        self.show()
        self.puntajes.hide()
        self.boton_volver.hide()
        self.puntajes = VboxPuntajes()

        self.boton_volver = QPushButton(self)
        self.boton_volver.setText("Volver")
        self.boton_volver.clicked.connect(self.boton_vovler_clikeado)

        self.vbox.addWidget(self.puntajes)
        self.vbox.addWidget(self.boton_volver)


class VboxPuntajes(QLabel):

    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        archivo = open(p.RUTA_PUNTAJES, "r")
        lineas = archivo.readlines()
        nuevas_lineas = []
        for i in lineas:
            i = i.strip("\n")
            i = i.split(",")
            nuevas_lineas.append(i)

        print(nuevas_lineas)

        nuevas_lineas = sorted(nuevas_lineas, key=lambda x: int(x[1]), reverse=True)

        print(nuevas_lineas)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        for i in range(len(nuevas_lineas)):
            if i < 5:
                hbox = QHBoxLayout()
                nombre = QLabel(f"{str(i + 1)}. {nuevas_lineas[i][0]}", self)
                puntaje = QLabel(f"{nuevas_lineas[i][1]} ptos", self)
                hbox.addStretch(1)
                hbox.addWidget(nombre)
                hbox.addWidget(puntaje)
                hbox.addStretch(1)
                vbox.addLayout(hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)

