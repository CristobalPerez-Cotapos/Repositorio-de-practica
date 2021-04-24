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
    for i in barcos:
        for j in cargar_tripulantes():
            if j.nombre in i.nombres_tripulacion:
                i.tripulacion.append(j)
    for i in barcos:
        for j in cargar_mercancia():
            if j.lote in i.codigos_carga:
                i.carga.append(j)
    return barcos


def cargar_canales():
    archivo = open("canales.csv", "r")
    lineas = archivo.readlines()
    canales = []
    lineas.pop(0)
    for i in lineas:
        i = i.strip("\n")
        i = i.split(",")
        canal = Canal(i[0], i[1], i[2])
        canales.append(canal)
    return canales


def cargar_mercancia():
    archivo = open("mercancia.csv", "r")
    lineas = archivo.readlines()
    cajas = []
    lineas.pop(0)
    for i in lineas:
        i = i.strip("\n")
        i = i.split(",")
        caja = Mercancia(i[0], i[1], i[2], i[3])
        cajas.append(caja)
    return cajas


def cargar_tripulantes():
    archivo = open("tripulantes.csv", "r")
    lineas = archivo.readlines()
    tripulantes = []
    lineas.pop(0)
    for i in lineas:
        i = i.strip("\n")
        i = i.split(",")
        if i[1] == "DCCapitÃ¡n":    # Para arreglar el tema de las tildes está escrito así
            persona = DCCapitan(i[0], i[2])
        elif i[1] == "DCCocinero":
            persona = DCCocinero(i[0], i[2])
        elif i[1] == "DCCarguero":
            persona = DCCarguero(i[0], i[2])
        else:
            raise ValueError("El tipo de este tripulante no existe")
        tripulantes.append(persona)
    return tripulantes
