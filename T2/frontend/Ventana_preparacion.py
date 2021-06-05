from PyQt5.QtWidgets import (QLabel, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,
                             QPushButton, QGridLayout, QProgressBar, QComboBox)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
import parametros as p
from backend.logica_preparacion import Personaje_preparacion, Edificio_preparacion
from backend.logica_de_juego import Personaje


class VentanaPreparacion(QWidget):

    senal_eleccion = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setGeometry(p.x, p.y, p.LARGO, p.ANCHO)
        self.setWindowTitle("Ventana de preparación")
        self.nombre_jugador = ""
        self.personajes_creados = False
        self.vida_homero = 1
        self.vida_lisa = 1
        self.vida_moe = 1
        self.vida_krusty = 1
        self.puntaje = 0
        self.items_buenos = 0
        self.items_malos = 0
        self.ronda = 0
        self.vida_personaje = 0
        self.gui_instanciado = False


    def init_gui(self):
        grilla_personajes = QGridLayout()
        self.homero_preparacion = Personaje_preparacion(self.homero)
        self.homero_preparacion.vida = self.vida_homero
        self.lisa_preparacion = Personaje_preparacion(self.lisa)
        self.lisa_preparacion.vida = self.vida_lisa
        self.moe_preparacion = Personaje_preparacion(self.moe)
        self.moe_preparacion.vida = self.vida_moe
        self.krusty_preparacion = Personaje_preparacion(self.krusty)
        self.krusty_preparacion.vida = self.vida_krusty
        grilla_personajes.addWidget(self.homero_preparacion, 0, 0)
        grilla_personajes.addWidget(self.lisa_preparacion, 0, 1)
        grilla_personajes.addWidget(self.moe_preparacion, 1, 0)
        grilla_personajes.addWidget(self.krusty_preparacion, 1, 1)


        logo = QLabel(self)
        pixeles_logo = QPixmap(p.RUTA_LOGO)
        pixeles_logo = pixeles_logo.scaled(100, 100, Qt.IgnoreAspectRatio)
        logo.setPixmap(pixeles_logo)
        logo.setScaledContents(True)

        hbox_elecciones = QHBoxLayout()
        hbox_elecciones.addWidget(logo)
        vbox_elecciones_1 = QVBoxLayout()
        mensaje_arrastra_personaje = QLabel()
        mensaje_arrastra_personaje.setText("Arrastra un personaje hasta la calle")
        vbox_elecciones_1.addWidget(mensaje_arrastra_personaje)
        vbox_elecciones_1.addLayout(grilla_personajes)
        hbox_elecciones.addLayout(vbox_elecciones_1)

        vbox_elecciones_2 = QVBoxLayout()
        mensaje_selecciona_dificultad = QLabel()
        mensaje_selecciona_dificultad.setText("Selecciona la dificultad de la siguiente ronda")
        self.combo_box = MiComboBox(self)
        self.combo_box.addItems(["Intro", "Avanzada"])
        self.mensaje_numero_ronda = QLabel()
        self.mensaje_numero_ronda.setText(f"RONDA: {self.ronda}")
        vbox_elecciones_2.addWidget(mensaje_selecciona_dificultad)
        vbox_elecciones_2.addWidget(self.combo_box)
        vbox_elecciones_2.addWidget(self.mensaje_numero_ronda)
        hbox_elecciones.addLayout(vbox_elecciones_2)


        hbox_datos = QHBoxLayout()
        self.barra_vida = QProgressBar(self)
        self.barra_vida.setValue(self.vida_personaje * 100)
        self.label_puntos = QLabel(self)
        self.label_puntos.setText("PUNTOS: 0")
        self.label_items_buenos = QLabel(self)
        self.label_items_malos = QLabel(self)
        self.label_items_buenos.setText("ITEMS BUENOS: 0")
        self.label_items_malos.setText("ITEMS MALOS: 0")
        hbox_datos.addWidget(self.barra_vida)
        hbox_datos.addWidget(self.label_puntos)
        hbox_datos.addWidget(self.label_items_buenos)
        hbox_datos.addWidget(self.label_items_malos)

        self.zona = Fondo_con_edificios(self)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(hbox_elecciones)
        self.vbox.addLayout(hbox_datos)
        self.vbox.addWidget(self.zona)
        self.setLayout(self.vbox)

        self.homero_preparacion.senal_vida_personje.connect(self.actualizar_vida)
        self.lisa_preparacion.senal_vida_personje.connect(self.actualizar_vida)
        self.moe_preparacion.senal_vida_personje.connect(self.actualizar_vida)
        self.krusty_preparacion.senal_vida_personje.connect(self.actualizar_vida)


    def actualizar_vida(self, vida):
        self.barra_vida.setValue(vida * 100)

    def abrir_ventana(self, diccionario):
        if not self.gui_instanciado:
            self.crear_personajes(diccionario)
            self.init_gui()
            self.gui_instanciado = True
            self.show()
        else:
            self.label_items_buenos.setText("ITEMS BUENOS: 0")
            self.label_items_malos.setText("ITEMS MALOS: 0")
            self.label_puntos.setText("PUNTOS: 0")
            self.mensaje_numero_ronda.setText(f"RONDA: 0")
            self.puntaje = 0
            self.ronda = 0
            self.items_malos = 0
            self.items_buenos = 0
            self.homero_preparacion.vida = 1
            self.lisa_preparacion.vida = 1
            self.moe_preparacion.vida = 1
            self.krusty_preparacion.vida = 1
            self.zona.hide()
            self.zona = Fondo_con_edificios(self)
            self.vbox.addWidget(self.zona)
            self.show()


    def crear_personajes(self, diccionario):
        if not self.personajes_creados:
            self.nombre_jugador = diccionario["nombre_jugador"]
            self.homero = diccionario["homero"]
            self.lisa = diccionario["lisa"]
            self.moe = diccionario["moe"]
            self.krusty = diccionario["krusty"]


    def enviar_senal_eleccion(self, eleccion):
        eleccion["dificultad"] = self.combo_box.currentText()
        eleccion["vida"] = self.personaje_preparacion_en_el_fondo().vida
        eleccion["ronda"] = self.ronda
        eleccion["items malos"] = self.items_malos
        eleccion["items buenos"] = self.items_buenos
        eleccion["puntaje"] = self.puntaje
        eleccion["jugador"] = self.nombre_jugador
        self.senal_eleccion.emit(eleccion)
        self.hide()

    def keyPressEvent(self, evento):
        if self.zona.hay_personaje:
            if not self.zona.personaje.anim.isRunning():
                if evento.text() == "w":
                    pos = self.zona.personaje.y
                    if pos == 0:
                        local = "Primaria"
                    elif pos == 1:
                        local = "Bar"
                    elif pos == 2:
                        local = "Planta nuclear"
                    elif pos == 3:
                        local = "Krustyland"
                    eleccion = {"personaje": self.zona.personaje.personaje, "mapa": local}
                    self.enviar_senal_eleccion(eleccion)

                elif evento.text() == "a":
                    self.zona.personaje.moverse_preparacion("izquierda")
                elif evento.text() == "d":
                    self.zona.personaje.moverse_preparacion("derecha")
                elif evento.text() == "s":
                    pass

    def continuar_jugando(self, diccionario):
        if diccionario["personaje usado"].personaje == "Homero":
            self.vida_homero = diccionario["vida"]
            self.homero_preparacion.vida = diccionario["vida"]
            self.actualizar_vida(self.homero_preparacion.vida)
        elif diccionario["personaje usado"].personaje == "Lisa":
            self.vida_lisa = diccionario["vida"]
            self.lisa_preparacion.vida = diccionario["vida"]
            self.actualizar_vida(self.lisa_preparacion.vida)
        elif diccionario["personaje usado"].personaje == "Moe":
            self.vida_moe = diccionario["vida"]
            self.moe_preparacion.vida = diccionario["vida"]
            self.actualizar_vida(self.moe_preparacion.vida)
        elif diccionario["personaje usado"].personaje == "Krusty":
            self.vida_krusty = diccionario["vida"]
            self.krusty_preparacion.vida = diccionario["vida"]
            self.actualizar_vida(self.krusty_preparacion.vida)


        self.ronda = diccionario["ronda"]
        self.mensaje_numero_ronda.setText(f"RONDA: {self.ronda}")
        self.items_malos = diccionario["items malos"]
        self.label_items_malos.setText(f"ITEMS MALOS: {self.items_malos}")
        self.items_buenos = diccionario["items buenos"]
        self.label_items_buenos.setText(f"ITEMS BUENOS: {self.items_buenos}")
        self.puntaje = diccionario["puntaje"]
        self.label_puntos.setText(f"PUNTOS: {self.puntaje}")

        self.show()

    def personaje_preparacion_en_el_fondo(self):
        if self.zona.personaje.personaje == "Homero":
            return self.homero_preparacion
        elif self.zona.personaje.personaje == "Lisa":
            return self.lisa_preparacion
        elif self.zona.personaje.personaje == "Moe":
            return self.moe_preparacion
        elif self.zona.personaje.personaje == "Krusty":
            return self.krusty_preparacion


class Fondo_con_edificios(QLabel):


    def __init__(self, ventana_preparacion):
        super().__init__()
        self.init_gui()
        self.ventana_preparacion = ventana_preparacion
        self.hay_personaje = False


    def init_gui(self):
        pixeles_fondo = QPixmap(p.RUTA_FONDO)
        pixeles_fondo = pixeles_fondo.scaled(500, 200, Qt.KeepAspectRatio)
        self.setPixmap(pixeles_fondo)
        self.setScaledContents(True)

        primaria = Edificio_preparacion("Primaria", self)
        bar = Edificio_preparacion("Bar", self)
        planta = Edificio_preparacion("Planta nuclear", self)
        krustyland = Edificio_preparacion("Krustyland", self)

        casilla_1 = CasillaCalle(1, self)
        casilla_1.senal_drop_cassilla_calle.connect(self.drop_personaje)
        casilla_2 = CasillaCalle(2, self)
        casilla_2.senal_drop_cassilla_calle.connect(self.drop_personaje)
        casilla_3 = CasillaCalle(3, self)
        casilla_3.senal_drop_cassilla_calle.connect(self.drop_personaje)
        casilla_4 = CasillaCalle(4, self)
        casilla_4.senal_drop_cassilla_calle.connect(self.drop_personaje)


        self.grilla = QGridLayout()
        self.grilla.addWidget(primaria, 0, 0)
        self.grilla.addWidget(bar, 0, 1)
        self.grilla.addWidget(planta, 0, 2)
        self.grilla.addWidget(krustyland, 0, 3)
        self.grilla.addWidget(casilla_1, 1, 0)
        self.grilla.addWidget(casilla_2, 1, 1)
        self.grilla.addWidget(casilla_3, 1, 2)
        self.grilla.addWidget(casilla_4, 1, 3)
        self.grilla.addWidget(QLabel(self), 2, 0)
        self.grilla.addWidget(QLabel(self), 2, 1)
        self.grilla.addWidget(QLabel(self), 2, 2)
        self.grilla.addWidget(QLabel(self), 2, 3)

        self.setLayout(self.grilla)

    def drop_personaje(self, diccionario):
        nombre = diccionario["nombre"]
        if not self.hay_personaje:
            self.personaje = Personaje(nombre)
            self.hay_personaje = True
        else:
            self.personaje.hide()
            self.personaje = Personaje(nombre)
        self.personaje.definir_zona(self, self.grilla)
        self.grilla.addWidget(self.personaje, 1, diccionario["casilla"] - 1)
        self.personaje.definir_posicion(1, diccionario["casilla"] - 1)


class CasillaCalle(QLabel):

    senal_drop_cassilla_calle = pyqtSignal(dict)

    def __init__(self, numero, fondo):
        super().__init__()
        self.resize(150, 130)
        self.setScaledContents(True)
        self.numero = numero
        self.fondo = fondo
        self.setAcceptDrops(True)

    def dragEnterEvent(self, evento):
        if evento.mimeData().hasText():
            evento.acceptProposedAction()

    def dropEvent(self, evento):
        nombre_personaje = evento.mimeData().text()
        diccionario_a_enviar = {"nombre" : nombre_personaje, "casilla": self.numero}
        self.senal_drop_cassilla_calle.emit(diccionario_a_enviar)
        evento.acceptProposedAction()

class MiComboBox(QComboBox):
    def __init__(self, ventana):
        super().__init__()
        self.ventana = ventana
    def keyPressEvent(self, evento):
        self.ventana.keyPressEvent(evento)
