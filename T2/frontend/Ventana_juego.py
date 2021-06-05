from PyQt5.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QProgressBar)
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QPixmap
from backend.logica_de_juego import Objeto
from backend.logica_zona_de_juego import ZonaDeJuego
import parametros as p
from backend.logica_musica import Musica


class VentanaJuego(QWidget):

    senal_fin_ronda = pyqtSignal(dict)
    senal_boton_salir = pyqtSignal(dict)

    def __init__(self, ancho, alto):
        super().__init__()
        self.setWindowTitle("Ventana de juego")
        self.ancho = ancho
        self.alto = alto
        self.tiempo = 0
        self.ronda = 0
        self.puntaje = 0
        self.items_buenos = 0
        self.items_malos = 0
        self.vida = 0
        self.gui_instanciado = False
        self.movimientos_realizados = []
        self.pausa = False
        self.jugador = ""
        self.lista_cheat_code = []
        self.cheat_activo = False

    def init_gui(self, ruta_carpeta_mapa):
        logo = QLabel(self)
        pixeles_logo = QPixmap(p.RUTA_LOGO)
        pixeles_logo = pixeles_logo.scaled(100, 100, Qt.IgnoreAspectRatio)
        logo.setPixmap(pixeles_logo)
        logo.setScaledContents(True)

        vbox_datos_1 = QVBoxLayout()
        label_tiempo = QLabel()
        label_tiempo.setText("Tiempo:")
        self.barra_tiempo = QProgressBar(self)
        label_vida = QLabel()
        label_vida.setText("Vida:")
        self.barra_tiempo.setValue(0)
        self.barra_vida = QProgressBar(self)
        self.barra_vida.setValue(self.vida * 100)
        vbox_datos_1.addWidget(label_vida)
        vbox_datos_1.addWidget(self.barra_vida)
        vbox_datos_1.addWidget(label_tiempo)
        vbox_datos_1.addWidget(self.barra_tiempo)

        vbox_datos_2 = QVBoxLayout()
        self.label_items_buenos = QLabel(self)
        self.label_items_buenos.setText("ITEMS BUENOS: 0")
        self.label_items_malos = QLabel(self)
        self.label_items_malos.setText("ITEMS MALOS: 0")
        vbox_datos_2.addWidget(self.label_items_buenos)
        vbox_datos_2.addWidget(self.label_items_malos)

        vbox_datos_3 = QVBoxLayout()
        self.label_ronda = QLabel(self)
        self.label_ronda.setText(f"RONDA: {self.ronda}")
        self.label_puntaje = QLabel(self)
        self.label_puntaje.setText("PUNTAJE: 0")
        vbox_datos_3.addWidget(self.label_ronda)
        vbox_datos_3.addWidget(self.label_puntaje)

        vbox_datos_4 = QVBoxLayout()
        self.boton_pausa = QPushButton(self)
        self.boton_pausa.setText("Pausar")
        self.boton_pausa.clicked.connect(self.pausar)

        boton_salir = QPushButton(self)
        boton_salir.setText("Salir")
        vbox_datos_4.addWidget(self.boton_pausa)
        vbox_datos_4.addWidget(boton_salir)
        boton_salir.clicked.connect(self.presion_boton_salir)

        hbox_datos = QHBoxLayout()
        hbox_datos.addWidget(logo)
        hbox_datos.addLayout(vbox_datos_1)
        hbox_datos.addLayout(vbox_datos_2)
        hbox_datos.addLayout(vbox_datos_3)
        hbox_datos.addLayout(vbox_datos_4)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(hbox_datos)
        ruta_fondo = ruta_carpeta_mapa + "/Fondo.png"
        self.fondo = QLabel("", self)
        pixles_fondo = QPixmap(ruta_fondo)
        pixles_fondo = pixles_fondo.scaled(256, 96, Qt.IgnoreAspectRatio)
        self.fondo.setPixmap(pixles_fondo)
        self.fondo.setScaledContents(True)
        hbox = QHBoxLayout()
        hbox.addWidget(self.fondo)
        self.vbox.addLayout(hbox)
        self.vbox.addWidget(self.zona)
        self.setGeometry(200, 25, self.ancho, self.alto)
        self.setLayout(self.vbox)

        self.musica = Musica()
        self.musica.comenzar()

        self.zona.personaje.senal_item_recogido.connect(self.procesar_item)
        self.zona.personaje.senal_movimieto.connect(self.movimientos_gorgory)

    def pausar(self):
        if self.pausa:
            self.timer_duracion_partida.start()
            self.timer_aparicion.start()
            self.pausa = False
            self.musica.cancion.play()
            for i in self.zona.dic_objetos:
                if isinstance(self.zona.dic_objetos[i], Objeto):
                    if self.zona.dic_objetos[i].tipo == "item":
                        self.zona.dic_objetos[i].timer.start()
        else:
            self.timer_duracion_partida.stop()
            self.timer_aparicion.stop()
            self.pausa = True
            self.musica.cancion.stop()
            for i in self.zona.dic_objetos:
                if isinstance(self.zona.dic_objetos[i], Objeto):
                    if self.zona.dic_objetos[i].tipo == "item":
                        self.zona.dic_objetos[i].timer.stop()

    def procesar_item(self, diccionario):
        objeto = diccionario["objeto"]
        if self.zona.personaje.personaje == "Homero":
            self.zona.personaje.habilidad_especial()
        if objeto.bueno and objeto.corazon:
            self.vida += p.PONDERADOR_CORAZON
            if self.vida > 1:
                self.vida = 1
            self.vida = round(self.vida, 2)
            self.barra_vida.setValue(self.vida * 100)
            self.items_buenos += 1
            self.label_items_buenos.setText(f"ITEMS BUENOS: {self.items_buenos}")
        elif objeto.bueno and not objeto.corazon:

            self.puntaje += (p.PUNTOS_OBJETO_NORMAL * 2)
            self.items_buenos += 1
            self.label_puntaje.setText(f"PUNTAJE: {self.puntaje}")
            self.label_items_buenos.setText(f"ITEMS BUENOS: {self.items_buenos}")
        elif objeto.malo:
            self.vida -= p.PONDERADOR_VENENO
            self.vida = round(self.vida, 2)
            self.items_malos += 1
            self.label_items_malos.setText(f"ITEMS MALOS: {self.items_malos}")
            self.barra_vida.setValue(self.vida * 100)
            if self.vida <= 0:
                self.terminar_ronda()
        else:
            self.puntaje += p.PUNTOS_OBJETO_NORMAL
            self.label_puntaje.setText(f"PUNTAJE: {self.puntaje}")
        self.vida = round(self.vida, 2)

    def keyPressEvent(self, evento):
        letra = evento.text()
        if evento.text() == "p":
            self.pausar()
        elif letra == "v" or letra == "n" or self.cheat_activo:
            self.cheat_activo = True
            if letra not in "vidniv":
                self.cheat_activo = False
                self.lista_cheat_code = []
            elif (letra in self.lista_cheat_code and (letra == "v" or letra == "n"))\
                    and not (self.lista_cheat_code == ["n", "i"] and letra == "v"):
                self.lista_cheat_code = []
                self.lista_cheat_code.append(letra)
            elif letra in self.lista_cheat_code and not (letra == "v" or letra == "n"):
                self.cheat_activo = False
                self.lista_cheat_code = []
            else:
                self.lista_cheat_code.append(letra)
                if len(self.lista_cheat_code) >= 4:
                    self.lista_cheat_code = []
                    self.cheat_activo = False
                else:
                    if self.lista_cheat_code == ["v", "i", "d"]:
                        self.vida += 0.5
                        if self.vida > 1:
                            self.vida = 1
                        self.barra_vida.setValue(self.vida * 100)
                        self.cheat_activo = False
                    elif self.lista_cheat_code == ["n", "i", "v"]:
                        self.terminar_ronda()
                        self.cheat_activo = False

        if not self.zona.personaje.anim.isRunning() and not self.pausa:
            if evento.text() == "w":
                self.zona.personaje.moverse("arriba")
            elif evento.text() == "a":
                self.zona.personaje.moverse("izquierda")
            elif evento.text() == "d":
                self.zona.personaje.moverse("derecha")
            elif evento.text() == "s":
                self.zona.personaje.moverse("abajo")

    def crear_zona(self, eleccion):
        if not self.gui_instanciado:
            carpeta_mapa = self.ruta_carpeta_mapa(eleccion["mapa"])
            self.dificultad = eleccion["dificultad"]
            self.zona = ZonaDeJuego(carpeta_mapa, eleccion["personaje"], self)
            self.vida = eleccion["vida"]
            self.init_gui(carpeta_mapa)
            self.comenzar_partida()
            self.show()
            self.gui_instanciado = True
            self.jugador = eleccion["jugador"]
        else:
            self.jugador = eleccion["jugador"]
            self.fondo.hide()
            carpeta_mapa = self.ruta_carpeta_mapa(eleccion["mapa"])
            self.dificultad = eleccion["dificultad"]
            self.zona = ZonaDeJuego(carpeta_mapa, eleccion["personaje"], self)
            self.vida = eleccion["vida"]
            self.barra_vida.setValue(self.vida * 100)
            ruta_fondo = carpeta_mapa + "/Fondo.png"
            self.fondo = QLabel("", self)
            self.comenzar_partida()
            pixles_fondo = QPixmap(ruta_fondo)
            pixles_fondo = pixles_fondo.scaled(256, 96, Qt.IgnoreAspectRatio)
            self.fondo.setPixmap(pixles_fondo)
            self.fondo.setScaledContents(True)
            hbox = QHBoxLayout()
            hbox.addWidget(self.fondo)
            self.vbox.addLayout(hbox)
            self.vbox.addWidget(self.zona)
            self.setGeometry(200, 25, self.ancho, self.alto)
            self.setLayout(self.vbox)
            self.movimientos_realizados = []
            self.zona.personaje.senal_item_recogido.connect(self.procesar_item)
            self.zona.personaje.senal_movimieto.connect(self.movimientos_gorgory)
            if eleccion["items malos"] == 0 and eleccion["items buenos"] == 0 \
                    and eleccion["puntaje"] == 0 and eleccion["ronda"] == 0:
                self.reiniciar_puntajes()
            self.musica = Musica()
            self.musica.comenzar()
            self.show()

    def reiniciar_puntajes(self):
        self.puntaje = 0
        self.items_buenos = 0
        self.items_malos = 0
        self.label_puntaje.setText(f"PUNTAJE: {self.puntaje}")
        self.label_items_buenos.setText(f"ITEMS BUENOS: {self.items_buenos}")
        self.label_items_malos.setText(f"ITEMS MALOS: {self.items_malos}")
        self.ronda = 0
        self.label_ronda.setText(f"RONDA: 0")

    def ruta_carpeta_mapa(self, mapa):
        if mapa == "Primaria":
            return p.CARPETA_PRIMARIA
        elif mapa == "Planta nuclear":
            return p.CARPETA_PLANTA_NUCLEAR
        elif mapa == "Bar":
            return p.CARPETA_BAR
        elif mapa == "Krustyland":
            return p.CARPETA_KRUSTYLAND

    def comenzar_partida(self):
        self.ronda += 1
        self.timer_aparicion = QTimer(self)
        self.tiempo_aparicion()
        if self.zona.personaje.personaje == "Moe":
            self.zona.personaje.habilidad_especial()
        self.timer_aparicion.setInterval(self.tiempo_aparicion_objeto * 1000)
        self.timer_aparicion.timeout.connect(self.zona.aparicion_objeto)
        self.timer_aparicion.start()
        self.timer_duracion_partida = QTimer()
        self.timer_duracion_partida.setInterval(1000)
        self.timer_duracion_partida.timeout.connect(self.avanzar_segundo)
        self.timer_duracion_partida.start()
        self.tiempo_delay()

    def avanzar_segundo(self):
        self.tiempo += 1
        self.duracion()
        porcentaje = self.tiempo/self.tiempo_druacion_partida
        self.barra_tiempo.setValue(porcentaje * 100)
        if self.tiempo == self.tiempo_druacion_partida:
            self.terminar_ronda()
            self.tiempo = 0
        if self.tiempo == self.tiempo_delay_gorgory:
            self.zona.agrgar_gorgory()
            self.zona.gorgory.senal_personaje_atrapado.connect(self.personaje_atrapado)

    def personaje_atrapado(self):
        self.vida = 0
        self.terminar_ronda()

    def terminar_ronda(self):
        self.hide()
        self.zona.hide()
        personaje_usado = self.zona.personaje
        dicionario_a_enviar = {
            "puntaje": self.puntaje,
            "items buenos": self.items_buenos,
            "items malos": self.items_malos,
            "ronda": self.ronda,
            "personaje usado": personaje_usado,
            "vida": self.vida,
            "jugador": self.jugador
        }
        self.senal_fin_ronda.emit(dicionario_a_enviar)
        self.timer_duracion_partida.stop()
        self.tiempo = 0
        self.barra_tiempo.setValue(0)
        self.musica.cancion.stop()
        if self.zona.hay_gorogry:
            self.zona.gorgory.timer_atrapar.stop()

    def duracion(self):
        if self.dificultad == "Avanzada":
            self.tiempo_druacion_partida = p.DURACION_AVANZADA
        elif self.dificultad == "Intro":
            self.tiempo_druacion_partida = p.DURACION_INTRO

    def tiempo_aparicion(self):
        if self.dificultad == "Avanzada":
            self.tiempo_aparicion_objeto = p.APARICION_AVANZADA
        elif self.dificultad == "Intro":
            self.tiempo_aparicion_objeto = p.APARICION_INTRO

    def tiempo_objeto(self):
        if self.dificultad == "Avanzada":
            self.tiempo_duracion_objeto = p.TIEMPO_OBJETO_AVANZADA
        elif self.dificultad == "Intro":
            self.tiempo_duracion_objeto = p.TIEMPO_OBJETO_INTRO

    def tiempo_delay(self):
        if self.dificultad == "Avanzada":
            self.tiempo_delay_gorgory = p.TIEMPO_DELAY_AVANZADA
        elif self.dificultad == "Intro":
            self.tiempo_delay_gorgory = p.TIEMPO_DEALY_INTRO
        if self.zona.personaje.personaje == "Krusty":
            self.zona.personaje.habilidad_especial()

    def movimientos_gorgory(self, direccion):
        if self.zona.hay_gorogry:
            self.zona.gorgory.anadir_movimiento(direccion)
        else:
            self.movimientos_realizados.append(direccion)

    def presion_boton_salir(self):
        self.hide()
        self.zona.hide()
        personaje_usado = self.zona.personaje
        dicionario_a_enviar = {
            "puntaje": self.puntaje,
            "items buenos": self.items_buenos,
            "items malos": self.items_malos,
            "ronda": self.ronda,
            "personaje usado": personaje_usado,
            "vida": self.vida,
            "jugador": self.jugador
        }
        self.senal_boton_salir.emit(dicionario_a_enviar)
        self.timer_duracion_partida.stop()
        self.tiempo = 0
        self.barra_tiempo.setValue(0)
        self.musica.cancion.stop()
        if self.zona.hay_gorogry:
            self.zona.gorgory.timer_atrapar.stop()
