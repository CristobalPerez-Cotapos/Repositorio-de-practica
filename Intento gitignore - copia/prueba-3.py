import threading
import time
from random import randint


def cuenta_hasta_diez():
    nombre_thread = threading.current_thread().name
    for numero in range(1, 11):
        time.sleep(randint(1, 5))
        print(f"{nombre_thread}: {numero}...")

# Instancia 5 threads distintos y ejecútalos.
uno = threading.Thread(name="uno", target = cuenta_hasta_diez)
dos = threading.Thread(name="dos", target = cuenta_hasta_diez)
tres = threading.Thread(name="tres", target = cuenta_hasta_diez)
cuatro = threading.Thread(name="cuatro", target = cuenta_hasta_diez)
cinco = threading.Thread(name="cinco", target = cuenta_hasta_diez)
uno.start()
dos.start()
tres.start()
cuatro.start()
cinco.start()