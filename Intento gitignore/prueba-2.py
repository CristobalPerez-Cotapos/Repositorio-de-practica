from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, QThread, QTimer
import sys
from random import randint


class MiVentana (QWidget):

    def __init__(self):
        super().__init__()
        self.init_gui()
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle("Ventana de mierda")

    def init_gui(self):


        pixeles = QPixmap("tortuga.jpg")
        self.cuadrado = QLabel(self)
        self.cuadrado.setGeometry(10,10,50,50)
        self.cuadrado.setScaledContents(True)
        self.cuadrado.setPixmap(pixeles)
        
        self.a = randint(0, 500)
        self.b = randint(0, 500)
        
        self.cuadrado.move(self.a, self.b)


    def mousePressEvent(self, event):
        if  self.b < event.y() < self.b + 50:
            if self.a < event.x() < self.a + 50:
                self.a = randint(0, 500)
                self.b = randint(0, 500)
                self.cuadrado.move(self.a, self.b)

class mithred(QThread):

    def __init__(self, senal,a ,b):
        super().__init__()
        self.senal = senal
        self.a = a
        self.b = b

    def run(self):
        for i in range:
            pass





app = QApplication([])
form = MiVentana()
form.show()
sys.exit(app.exec_())

