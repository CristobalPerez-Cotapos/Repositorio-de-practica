from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, Qt, QMimeData
from PyQt5.QtGui import QPixmap, QDrag, QPainter
import parametros as p


class PersonajePreparacion(QLabel):

    senal_vida_personje = pyqtSignal(float)

    def __init__(self, personaje):
        super().__init__()
        self.personaje = personaje
        self.init_gui()
        self.nombre = self.personaje.personaje
        self.vida = 1

    def init_gui(self):
        ruta_imagen_inicial = self.personaje.ruta_imagen_inicial
        pixles = QPixmap(ruta_imagen_inicial)
        pixeles2 = pixles.scaled(60, 60, Qt.KeepAspectRatio)
        self.setPixmap(pixeles2)
        self.setScaledContents(False)

    def mousePressEvent(self, evento):
        if evento.button() == Qt.LeftButton:
            self.senal_vida_personje.emit(self.vida)
            self.drag_posicion_inicial = evento.pos()

    def mouseMoveEvent(self, evento):
        if evento.buttons() & Qt.LeftButton:
            drag = QDrag(self)
            mimedata = QMimeData()
            mimedata.setText(self.nombre)
            drag.setMimeData(mimedata)
            pixmap = QPixmap(self.size())
            painter = QPainter(pixmap)
            painter.drawPixmap(self.rect(), self.grab())
            painter.end()
            drag.setPixmap(pixmap)
            drag.setHotSpot(evento.pos())
            drag.exec(Qt.CopyAction | Qt.MoveAction)

    def mousePressEvent(self, evento):
        if evento.buttons() & Qt.LeftButton:
            self.senal_vida_personje.emit(self.vida)


class Edificio_preparacion(QLabel):

    senal_mapa_elegido = pyqtSignal(dict)

    def __init__(self, mapa, fondo):
        super().__init__()
        self.setAcceptDrops(True)
        self.nombre_mapa = mapa
        self.init_gui()
        self.fondo = fondo

    def init_gui(self):
        pixeles = QPixmap(self.mapa)
        pixeles = pixeles.scaled(150, 130, Qt.KeepAspectRatio)
        self.setPixmap(pixeles)
        self.setScaledContents(True)

    @property
    def mapa(self):
        if self.nombre_mapa == "Bar":
            return p.RUTA_BAR
        elif self.nombre_mapa == "Krustyland":
            return p.RUTA_KRUSTYLAND
        elif self.nombre_mapa == "Planta nuclear":
            return p.RUTA_PLANTA_NUCLEAR
        elif self.nombre_mapa == "Primaria":
            return p.RUTA_PRIMARIA
        else:
            raise ValueError("El mapa no es valido")

    #def dragEnterEvent(self, evento):
    #    if evento.mimeData().hasText():
    #        evento.acceptProposedAction()

    #def dropEvent(self, evento):
    #    nombre_personaje = evento.mimeData().text()
    #    eleccion = {"personaje": nombre_personaje, "mapa":  self.nombre_mapa}
    #    self.fondo.ventana_preparacion.enviar_senal_eleccion(eleccion)
    #    evento.acceptProposedAction()
