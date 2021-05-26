from PyQt5.QtWidgets import (QLabel, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,
                             QPushButton)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap


class Ventana_puntajes(QWidget):

    def __init__(self, ancho, alto, ruta_puntajes, ruta_imagen):
        super().__init__()
        self.size = (ancho, alto)
        self.resize(ancho, alto)
        self.setWindowTitle("Ventana de puntajes")
        self.init_gui(ruta_imagen, ruta_puntajes)

    def inint_gui(self, ruta_imagen, ruta_puntajes):
        pass

    def Vbox_puntajes(self,ruta_puntajes):
        archivo = open(ruta_puntajes, "r")
        lineas = archivo.readlines()
        nuevas_lineas = []
        for i in lineas:
            i.strip("\n")
            i.split(",")
            nuevas_lineas.append(i)

        vbox = QHBoxLayout
        vbox.addStretch(1)
        for i in range(len(nuevas_lineas)):
            if i < 5:
                hbox = QHBoxLayout
                nombre = QLabel(f"{str(i)}. {nuevas_lineas[i][0]}", self)
                putaje = QLabel(f"{nuevas_lineas[i][1]} ptos", self)
                hbox.addStretch(1)
                hbox.addWidget(nombre)
                hbox.addWidget(putaje)
                hbox.addStretch(1)
                vbox.addLayout(hbox)
        vbox.addStretch(1)
        return vbox