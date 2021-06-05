from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
import parametros as p


class Musica(QObject):

    def __init__(self):
        super().__init__()
        self.ruta_cancion = p.RUTA_CANCION

    def comenzar(self):
        self.cancion = QtMultimedia.QSound(self.ruta_cancion)
        self.cancion.Infinite
        self.cancion.play()
