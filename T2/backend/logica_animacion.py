from PyQt5.QtWidgets import (QLabel, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton)
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QThread, QMimeData
from PyQt5.QtGui import QPixmap, QDrag, QPainter, QCursor
from random import randint
import PyQt5
import parametros as p
from time import sleep
import threading

class Animacion(QThread):
    lock_animacion = threading.Lock()
    lock_animacion_gorgory = threading.Lock()

    def __init__(self, ruta_personaje, direccion, personaje):
        super().__init__()
        self.ruta = ruta_personaje
        self.direccion = direccion
        self.personaje = personaje

    def run(self):
        if self.personaje.personaje == "Gorgory":
            self.lock_animacion_gorgory.acquire()
        else:
            self.lock_animacion.acquire()
        tiempo = 1 / self.personaje.velocidad
        if self.direccion == "arriba":
            pos_1 = self.ruta + "/up_1.png"
            pos_2 = self.ruta + "/up_2.png"
            pos_3 = self.ruta + "/up_3.png"
            pixeles_pos_1 = QPixmap(pos_1)
            pixeles_pos_1 = pixeles_pos_1.scaled(60, 60, Qt.KeepAspectRatio)
            self.personaje.setPixmap(pixeles_pos_1)
            if self.personaje.x > 1 and False:
                self.personaje.x -= 1
            self.personaje.grilla.addWidget(self.personaje, self.personaje.x, self.personaje.y)
            sleep(tiempo)
            pixeles_pos_2 = QPixmap(pos_2)
            pixeles_pos_2 = pixeles_pos_2.scaled(60, 60, Qt.KeepAspectRatio)
            self.personaje.setPixmap(pixeles_pos_2)
            if self.personaje.x > 1 and False:
                self.personaje.x -= 1
            sleep(tiempo)
            pixeles_pos_3 = QPixmap(pos_3)
            pixeles_pos_3 = pixeles_pos_3.scaled(60, 60, Qt.KeepAspectRatio)
            self.personaje.setPixmap(pixeles_pos_3)
            sleep(tiempo)
            self.personaje.setPixmap(pixeles_pos_1)

        elif self.direccion == "abajo":
            pos_1 = self.ruta + "/down_1.png"
            pos_2 = self.ruta + "/down_2.png"
            pos_3 = self.ruta + "/down_3.png"
            pixeles_pos_1 = QPixmap(pos_1)
            pixeles_pos_1 = pixeles_pos_1.scaled(60, 60, Qt.KeepAspectRatio)
            self.personaje.setPixmap(pixeles_pos_1)
            if self.personaje.x < p.ALTO_GRAVA - 2 and False:
                self.personaje.x += 1
            self.personaje.grilla.addWidget(self.personaje, self.personaje.x, self.personaje.y)
            sleep(tiempo)
            pixeles_pos_2 = QPixmap(pos_2)
            pixeles_pos_2 = pixeles_pos_2.scaled(60, 60, Qt.KeepAspectRatio)
            self.personaje.setPixmap(pixeles_pos_2)
            if self.personaje.x < p.ALTO_GRAVA - 2 and False:
                self.personaje.x += 1
            sleep(tiempo)
            pixeles_pos_3 = QPixmap(pos_3)
            pixeles_pos_3 = pixeles_pos_3.scaled(60, 60, Qt.KeepAspectRatio)
            self.personaje.setPixmap(pixeles_pos_3)
            sleep(tiempo)
            self.personaje.setPixmap(pixeles_pos_1)

        elif self.direccion == "izquierda":
            pos_1 = self.ruta + "/left_1.png"
            pos_2 = self.ruta + "/left_2.png"
            pos_3 = self.ruta + "/left_3.png"
            pixeles_pos_1 = QPixmap(pos_1)
            pixeles_pos_1 = pixeles_pos_1.scaled(60, 60, Qt.KeepAspectRatio)
            self.personaje.setPixmap(pixeles_pos_1)
            if self.personaje.y > 1 and False:
                self.personaje.y -= 1
            self.personaje.grilla.addWidget(self.personaje, self.personaje.x, self.personaje.y)
            sleep(tiempo)
            pixeles_pos_2 = QPixmap(pos_2)
            pixeles_pos_2 = pixeles_pos_2.scaled(60, 60, Qt.KeepAspectRatio)
            self.personaje.setPixmap(pixeles_pos_2)
            if self.personaje.y > 1 and False:
                self.personaje.y -= 1
            sleep(tiempo)
            pixeles_pos_3 = QPixmap(pos_3)
            pixeles_pos_3 = pixeles_pos_3.scaled(60, 60, Qt.KeepAspectRatio)
            self.personaje.setPixmap(pixeles_pos_3)
            sleep(tiempo)
            self.personaje.setPixmap(pixeles_pos_2)

        elif self.direccion == "derecha":
            pos_1 = self.ruta + "/right_1.png"
            pos_2 = self.ruta + "/right_2.png"
            pos_3 = self.ruta + "/right_3.png"
            pixeles_pos_1 = QPixmap(pos_1)
            pixeles_pos_1 = pixeles_pos_1.scaled(60, 60, Qt.KeepAspectRatio)
            self.personaje.setPixmap(pixeles_pos_1)
            if self.personaje.x < p.ANCHO_GRAVA - 2 and False:
                self.personaje.x += 1
            self.personaje.grilla.addWidget(self.personaje, self.personaje.x, self.personaje.y)
            sleep(tiempo)
            pixeles_pos_2 = QPixmap(pos_2)
            pixeles_pos_2 = pixeles_pos_2.scaled(60, 60, Qt.KeepAspectRatio)
            self.personaje.setPixmap(pixeles_pos_2)
            if self.personaje.x < p.ANCHO_GRAVA - 2 and False:
                self.personaje.x += 1
            sleep(tiempo)
            pixeles_pos_3 = QPixmap(pos_3)
            pixeles_pos_3 = pixeles_pos_3.scaled(60, 60, Qt.KeepAspectRatio)
            self.personaje.setPixmap(pixeles_pos_3)
            sleep(tiempo)
            self.personaje.setPixmap(pixeles_pos_2)
        if self.personaje.personaje == "Gorgory":
            self.lock_animacion_gorgory.release()
        else:
            self.lock_animacion.release()