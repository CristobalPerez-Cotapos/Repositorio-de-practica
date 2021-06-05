import sys
import parametros as p
from PyQt5.QtWidgets import QApplication
from frontend.Ventana_inicio import VentanaInicio
from frontend.Ventana_juego import VentanaJuego
from frontend.Vetana_puntajes import VentanaPuntajes
from frontend.Ventana_preparacion import VentanaPreparacion
from frontend.Ventana_post_ronda import VentanaPostRonda

app = QApplication(sys.argv)

ventana_inicio = VentanaInicio()
ventana_puntajes = VentanaPuntajes(p.ANCHO, p.LARGO)
ventana_preparacion = VentanaPreparacion()
ventana_inicio.show()

ventana_inicio.senal_ver_mejores.connect(ventana_puntajes.abrir_ventana)
ventana_inicio.senal_enviar_nombre.connect(ventana_preparacion.abrir_ventana)
ventana_puntajes.senal_vovler_puntajes.connect(ventana_inicio.mostrarse)

ventana_juego = VentanaJuego(640, 480)
ventana_post_ronda = VentanaPostRonda()

ventana_preparacion.senal_eleccion.connect(ventana_juego.crear_zona)


ventana_juego.senal_fin_ronda.connect(ventana_post_ronda.abrir_ventana)
ventana_juego.senal_boton_salir.connect(ventana_inicio.mostrarse)
ventana_juego.senal_boton_salir.connect(ventana_puntajes.actualzar_archivo)

ventana_post_ronda.senal_salir_post_ronda.connect(ventana_inicio.mostrarse)
ventana_post_ronda.senal_salir_post_ronda.connect(ventana_puntajes.actualzar_archivo)
ventana_post_ronda.senal_continuar_post_ronda.connect(ventana_preparacion.continuar_jugando)

sys.exit(app.exec())
