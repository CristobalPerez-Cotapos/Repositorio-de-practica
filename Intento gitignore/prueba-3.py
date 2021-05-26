import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel)


class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializa_gui()

    def inicializa_gui(self):
        self.etiqueta = QLabel('Etiqueta', self)
        self.etiqueta.move(20, 10)
        self.resize(self.etiqueta.sizeHint())

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Teclado')
        self.show()

    def keyPressEvent(self, event):
        """
        Este método maneja el evento que se produce al presionar las teclas.
        """
        self.etiqueta.setText(f'Presionaron la tecla: {event.text()} de código: {event.key()}')
        self.etiqueta.resize(self.etiqueta.sizeHint())


if __name__ == '__main__':
    app = QApplication([])
    ex = MiVentana()
    sys.exit(app.exec_())
