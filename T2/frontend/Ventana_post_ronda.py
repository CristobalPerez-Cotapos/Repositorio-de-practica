from PyQt5.QtWidgets import (QLabel, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,
                             QPushButton, QGridLayout, QProgressBar, QComboBox)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
import parametros as p
from backend.logica_preparacion import Personaje_preparacion, Edificio_preparacion
from backend.logica_de_juego import Personaje


class VentanaPostRonda(QWidget):

    senal_continuar_post_ronda = pyqtSignal(dict)
    senal_salir_post_ronda = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.gui_instanciado = False
        self.jugador = ""
        pass

    def abrir_ventana(self, diccionario):
        if not self.gui_instanciado:
            self.diccionario = diccionario
            if self.diccionario["vida"] > 1:
                self.diccionario.vida = 1
            self.init_gui()
            self.show()
            self.gui_instanciado = True
            self.jugador = diccionario["jugador"]
        else:
            self.diccionario = diccionario
            if self.diccionario["vida"] > 1:
                self.diccionario.vida = 1
            self.num_puntaje.setText(str(diccionario["puntaje"]))
            vida = self.diccionario["vida"]
            if vida <= 0:
                vida = 0
            self.definir_mensaje()
            self.num_vida.setText(str(vida * 100) + "%")
            self.num_items_malos.setText(str(diccionario["items malos"]))
            self.num_items_buenos.setText(str(diccionario["items buenos"]))
            self.jugador = diccionario["jugador"]
            self.show()

    def init_gui(self):
        vbox = QVBoxLayout()

        hbox_titulo = QHBoxLayout()
        titulo = QLabel(self)
        titulo.setText("RESUMEN DE LA RONDA")
        titulo.setScaledContents(True)
        logo = QLabel(self)
        pixeles_logo = QPixmap(p.RUTA_LOGO)
        pixeles_logo = pixeles_logo.scaled(100, 100, Qt.IgnoreAspectRatio)
        logo.setPixmap(pixeles_logo)
        logo.setScaledContents(True)
        hbox_titulo.addWidget(titulo)
        hbox_titulo.addWidget(logo)

        grilla_datos = QGridLayout()

        txt_puntaje = QLabel()
        txt_puntaje.setText("Puntaje total:")
        txt_vida = QLabel()
        txt_vida.setText("Vida:")
        txt_items_buenos = QLabel()
        txt_items_buenos.setText("Cantidad de ítems buenos")
        txt_items_malos = QLabel()
        txt_items_malos.setText("Cantidad de ítems malos")

        self.num_puntaje = QLabel()
        self.num_puntaje.setText(str(self.diccionario["puntaje"]))
        self.num_vida = QLabel()
        vida = self.diccionario["vida"]
        if vida <= 0:
            vida = 0
        self.num_vida.setText(f"{vida * 100}%")
        self.num_items_buenos = QLabel()
        self.num_items_buenos.setText(str(self.diccionario["items buenos"]))
        self.num_items_malos = QLabel()
        self.num_items_malos.setText(str(self.diccionario["items malos"]))
        grilla_datos.addWidget(txt_puntaje, 0, 0)
        grilla_datos.addWidget(self.num_puntaje, 0, 1)
        grilla_datos.addWidget(txt_vida, 1, 0)
        grilla_datos.addWidget(self.num_vida, 1, 1)
        grilla_datos.addWidget(txt_items_buenos, 2, 0)
        grilla_datos.addWidget(self.num_items_buenos, 2, 1)
        grilla_datos.addWidget(txt_items_malos, 3, 0)
        grilla_datos.addWidget(self.num_items_malos, 3, 1)



        hbox_botones = QHBoxLayout()
        self.boton_continuar = QPushButton(self)
        self.boton_continuar.setText("Continuar juego")
        self.boton_continuar.clicked.connect(self.boton_continuar_clickeado)
        boton_salir = QPushButton(self)
        boton_salir.setText("Salir")
        hbox_botones.addWidget(self.boton_continuar)
        boton_salir.clicked.connect(self.boton_salir_clickeado)
        hbox_botones.addWidget(boton_salir)

        self.mensaje_indicador = QLabel(self)
        self.definir_mensaje()

        vbox.addLayout(hbox_titulo)
        vbox.addLayout(grilla_datos)
        vbox.addWidget(self.mensaje_indicador)
        vbox.addLayout(hbox_botones)

        self.setLayout(vbox)

    def definir_mensaje(self):
        if self.diccionario["vida"] > 0:
            self.mensaje_indicador.setText("Puedes seguir jugando")
            self.mensaje_indicador.setStyleSheet("background-color: green")
            self.boton_continuar.setDisabled(False)
        else:
            self.mensaje_indicador.setText("Te has quedado sin vida, no puedes continuar :(")
            self.mensaje_indicador.setStyleSheet("background-color: red")
            self.boton_continuar.setDisabled(True)

    def boton_continuar_clickeado(self):
        if self.diccionario["vida"] > 0:
            self.senal_continuar_post_ronda.emit(self.diccionario)
            self.hide()

    def boton_salir_clickeado(self):
        self.senal_salir_post_ronda.emit(self.diccionario)
        self.hide()

