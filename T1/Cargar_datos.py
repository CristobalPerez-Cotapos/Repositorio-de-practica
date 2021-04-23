from Entidades import (Buque, Barco_carguero, Barco_de_pasajeros, DCCarguero, DCCapitan,
                       Canal, DCCocinero, Mercancia)


def cargar_barcos():
    archivo = open("barcos.csv", "r")
    lineas = archivo.readlines()
    barcos = []
    for i in lineas:
        i = i.strip("\n")
        i = i.split(",")
        i[7] = i[7].split(";")
        i[8] = i[8].split(";")
        if i[1] == "Pasajero":
            barquito = Barco_de_pasajeros(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            barcos.append(barquito)
        elif i[1] == "Carguero":
            barquito = Barco_carguero(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            barcos.append(barquito)
        elif i[1] == "Buque":
            barquito = Buque(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            barcos.append(barquito)
    return barcos



lista = cargar_barcos()
for i in lista:
    print(str(i))