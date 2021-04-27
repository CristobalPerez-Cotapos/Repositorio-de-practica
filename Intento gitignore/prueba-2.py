import threading
import time


def deletrea_palabra(palabra, periodo):
    for caracter in palabra:
        time.sleep(periodo)
        print(caracter.upper())


# Instancia 3 threads distintos y ejecútalos con los parametros dados.
uno = threading.Thread(name = "uno", target=deletrea_palabra, args =("be í",3))
dos = threading.Thread(name = "dos", target=deletrea_palabra, args =("ud cIUes",5))
tres = threading.Thread(name = "tres", target=deletrea_palabra, args =("naHq",7))
uno.start()
dos.start()
tres.start()
