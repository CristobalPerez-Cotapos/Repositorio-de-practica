import sys
import parametros as p
from PyQt5.QtWidgets import QApplication
from forntend.Ventana_inicio import VentanaInicio
from forntend.Ventana_juego import Ventana_juego

app = QApplication(sys.argv)

ventana_inicio = VentanaInicio(p.ANCHO, p.LARGO, p.RUTA_LOGO)
ventana_juego = Ventana_juego("forntend/assets/sprites/Mapa/Planta_nuclear", "forntend/assets/sprites/Personajes", 100, 100)
ventana_juego.show()
sys.exit(app.exec())
