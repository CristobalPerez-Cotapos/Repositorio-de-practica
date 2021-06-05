from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QPixmap
import parametros as p
from backend.logica_animacion import Animacion


class Personaje(QLabel):

    senal_item_recogido = pyqtSignal(dict)
    senal_movimieto = pyqtSignal(str)

    def __init__(self, personaje):
        super().__init__()
        self.personaje = personaje
        self.init_gui()
        self.grilla = None
        self.x = 0
        self.y = 0
        self.zona = None
        self.items = []
        self.anim = Animacion("", "", self)

    def init_gui(self):
        self.ruta_imagen_inicial = self.carpeta_personaje + "/down_1.png"
        pixles = QPixmap(self.ruta_imagen_inicial)
        pixeles2 = pixles.scaled(60, 60, Qt.KeepAspectRatio)
        self.setPixmap(pixeles2)
        self.setScaledContents(True)


    def moverse(self, direccion):
        if direccion == "arriba":
            if 0 < self.x:
                if type(self.zona.dic_objetos[(self.x - 1, self.y)]) == Objeto:
                    self.colision(self.zona.dic_objetos[(self.x - 1, self.y)])
                    if self.zona.dic_objetos[(self.x - 1, self.y)].tipo == "item":
                        self.anim = Animacion(self.carpeta_personaje, "arriba", self)
                        self.anim.start()
                        self.x -= 1
                        self.grilla.addWidget(self, self.x, self.y)
                        self.senal_movimieto.emit(direccion)
                else:
                    self.anim = Animacion(self.carpeta_personaje, "arriba", self)
                    self.anim.start()
                    self.x -= 1
                    self.grilla.addWidget(self, self.x, self.y)
                    self.senal_movimieto.emit(direccion)

        elif direccion == "abajo":
            if p.ALTO_GRAVA - 1 > self.x:
                if type(self.zona.dic_objetos[(self.x + 1, self.y)]) == Objeto:
                    self.colision(self.zona.dic_objetos[(self.x + 1, self.y)])
                    if self.zona.dic_objetos[(self.x + 1, self.y)].tipo == "item":
                        self.anim = Animacion(self.carpeta_personaje, "abajo", self)
                        self.anim.start()
                        self.x += 1
                        self.grilla.addWidget(self, self.x, self.y)
                        self.senal_movimieto.emit(direccion)
                else:
                    self.anim = Animacion(self.carpeta_personaje, "abajo", self)
                    self.anim.start()
                    self.x += 1
                    self.grilla.addWidget(self, self.x, self.y)
                    self.senal_movimieto.emit(direccion)

        elif direccion == "izquierda":
            if 0 < self.y:
                if type(self.zona.dic_objetos[(self.x, self.y - 1)]) == Objeto:
                    self.colision(self.zona.dic_objetos[(self.x, self.y - 1)])
                    if self.zona.dic_objetos[(self.x, self.y - 1)].tipo == "item":
                        self.anim = Animacion(self.carpeta_personaje, "izquierda", self)
                        self.anim.start()
                        self.y -= 1
                        self.grilla.addWidget(self, self.x, self.y)
                        self.senal_movimieto.emit(direccion)
                else:
                    self.anim = Animacion(self.carpeta_personaje, "izquierda", self)
                    self.anim.start()
                    self.y -= 1
                    self.grilla.addWidget(self, self.x, self.y)
                    self.senal_movimieto.emit(direccion)

        elif direccion == "derecha":
            if p.ANCHO_GRAVA - 1 > self.y:
                if type(self.zona.dic_objetos[(self.x, self.y + 1)]) == Objeto:
                    self.colision(self.zona.dic_objetos[(self.x, self.y + 1)])
                    if self.zona.dic_objetos[(self.x, self.y + 1)].tipo == "item":
                        self.anim = Animacion(self.carpeta_personaje, "derecha", self)
                        self.anim.start()
                        self.y += 1
                        self.grilla.addWidget(self, self.x, self.y)
                        self.senal_movimieto.emit(direccion)
                else:
                    self.anim = Animacion(self.carpeta_personaje, "derecha", self)
                    self.anim.start()
                    self.y += 1
                    self.grilla.addWidget(self, self.x, self.y)
                    self.senal_movimieto.emit(direccion)

    def definir_zona(self, zona, grilla):
        self.zona = zona
        self.grilla = grilla

    def colision(self, objeto):
        if objeto.tipo == "obstaculo":
            pass
        elif objeto.tipo == "item" and not objeto.recogido:
            self.items.append(objeto)
            objeto.recogido = True
            self.items.append(objeto)
            objeto.hide()
            label = QLabel("", self.zona)
            self.grilla.addWidget(label, self.x, self.y)
            self.grilla.addWidget(self, self.x, self.y)
            diccionario_a_enviar = {"objeto": objeto}
            self.senal_item_recogido.emit(diccionario_a_enviar)

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

    def moverse_preparacion(self, direccion):
        if direccion == "derecha":
            if 3 > self.y:
                self.anim = Animacion(self.carpeta_personaje, "derecha", self)
                self.anim.start()
                self.y += 1
                self.grilla.addWidget(self, self.x, self.y)
        elif direccion == "izquierda":
            if 0 < self.y:
                self.anim = Animacion(self.carpeta_personaje, "izquierda", self)
                self.anim.start()
                self.y -= 1
                self.grilla.addWidget(self, self.x, self.y)

    def definir_posicion(self, x, y):
        self.x = x
        self.y = y

    def habilidad_especial(self):
        if self.personaje == "Homero":
            contador = 0
            i = 0
            while i < len(self.items):
                if self.items[i].ruta == p.CARPETA_OBJETOS + "/Dona.png":
                    contador += 1
                    i += 1
                elif self.items[i].malo:
                    contador = 0
                    self.items = []
                i += 1
            if contador >= 10:
                if self.zona.ventana_juego.vida + p.PONDERADOR_HOMERO <= 1:
                    self.zona.ventana_juego.vida += p.PONDERADOR_HOMERO
                else:
                    self.zona.ventana_juego.vida = 1
                self.items = []

        elif self.personaje == "Lisa":
            for i in self.zona.dic_objetos:
                if isinstance(self.zona.dic_objetos[i], Objeto):
                    objeto = self.zona.dic_objetos[i]
                    if objeto.ruta == (p.CARPETA_OBJETOS + "/Saxofon.png") \
                            and not objeto.habilidad_lisa:
                        objeto.timer.setInterval((objeto.tiempo +
                                                  p.PONDERADOR_SAXOFONES_LISA) * 1000)
                        objeto.timer.timeout.connect(objeto.expirar)
                        objeto.habilidad_lisa = True
        elif self.personaje == "Moe":
            self.zona.ventana_juego.tiempo_aparicion_objeto /= 2
        elif self.personaje == "Krusty":
            self.zona.ventana_juego.tiempo_delay_gorgory *= 2


class Objeto(QLabel):

    def __init__(self, ruta, tipo, zona, posicion):
        super().__init__()
        self.ruta = ruta
        self.tipo = tipo
        self.bueno = False
        self.malo = False
        self.recogido = False
        self.corazon = False
        self.zona = zona
        self.posicion = posicion
        self.habilidad_lisa = False
        self.init_gui(ruta)

    def init_gui(self, ruta):
        pixles = QPixmap(ruta)
        pixeles2 = pixles.scaled(60, 60, Qt.KeepAspectRatio)
        self.setPixmap(pixeles2)
        self.timer = QTimer(self)
        self.zona.ventana_juego.tiempo_objeto()
        self.tiempo = self.zona.ventana_juego.tiempo_duracion_objeto
        self.timer.setInterval(self.tiempo * 1000)
        self.timer.timeout.connect(self.expirar)
        self.timer.start()

    def expirar(self):
        if self.tipo == "item":
            self.hide()
            self.zona.dic_objetos[self.posicion] = QLabel()
            self.recogido = True
            self.timer.stop()


class Gorgory(Personaje):

    senal_personaje_atrapado = pyqtSignal()

    def __init__(self, personaje, movimientos_iniciales, zona, grilla):
        super().__init__(personaje)
        self.lista_movimientos = movimientos_iniciales
        self.grilla = grilla
        self.zona = zona
        self.activarse()

    def anadir_movimiento(self, direccion):
        self.lista_movimientos.append(direccion)

    def activarse(self):
        timer_movimiento = QTimer(self)
        timer_movimiento.setInterval((1/p.VELOCIDAD_GORGORY * 4) * 1000)
        timer_movimiento.start()
        timer_movimiento.timeout.connect(self.avanzar)

        self.timer_atrapar = QTimer(self)
        self.timer_atrapar.setInterval(100)
        self.timer_atrapar.start()
        self.timer_atrapar.timeout.connect(self.atrapar)

    def avanzar(self):
        if len(self.lista_movimientos) >= 1 and not self.zona.ventana_juego.pausa:
            self.moverse(self.lista_movimientos[0])
            self.lista_movimientos.pop(0)

    def atrapar(self):
        if self.zona.personaje.x == self.x and self.zona.personaje.y == self.y:
            self.senal_personaje_atrapado.emit()
            self.timer_atrapar.stop()
