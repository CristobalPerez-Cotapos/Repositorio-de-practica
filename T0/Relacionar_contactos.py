from Cargar_usuarios import (cargar_usuarios, cargar_contactos,
                             cargar_grupos)


def relacionar_contactos(usuario):
    for i in cargar_usuarios("usuarios.csv"):
        for j in cargar_contactos("contactos.csv"):
            if str(i) == j[0]:
                i.agregar_contacto(j[1])                   # todos los contactos está relacionados
        if str(i) == usuario:
            usuario = i
    return usuario

def relacionar_grupos(usuario):
    for i in cargar_usuarios("usuarios.csv"):
        if str(i) == usuario:
            usuario = i
        for j in cargar_grupos("grupos.csv"):
            if str(i) == j[1]:
                i.agregar_grupo(j[0])
    return usuario


def diccionarios_de_mensajes(tipo):                      ## FALLA, DEBES DUPLICAR LOS DICCIONARIOS PARA CADA LLAVE           # tipo ¿regular o grupo?
    archivo_mensajes = open("mensajes.csv")
    lineas_archivo_mensajes = archivo_mensajes.readlines()
    archivo_mensajes.close()
    for i in range(len(lineas_archivo_mensajes)):
        lineas_archivo_mensajes[i] = lineas_archivo_mensajes[i].strip(",")
        lista_mensaje = lineas_archivo_mensajes[i].split(",")
        lineas_archivo_mensajes[i] = lista_mensaje                    # lineas_archivo_mensajes ahora es una matriz

    dic_mensajes_regulares = {}       # key (usuario1,usuario2)
    dic_mensajes_grupo = {}           # key str(grupo)

    for i in lineas_archivo_mensajes:                   # creamos todas las entradas en los diccionarios
        if i[0] == "grupo":
            dic_mensajes_grupo[i[2]] = [""]
        else:
            tupla_llave = (i[1], i[2])
            dic_mensajes_regulares[tupla_llave] = [""]
            tupla_llave_2 = (i[2], i[1])
            dic_mensajes_regulares[tupla_llave_2] = [""]
    lista_contactos = cargar_contactos("contactos.csv")
    for i in lista_contactos:
        dic_mensajes_regulares[(i[1],i[0])] = [["Inicio del chat","Mensaje del sistema",""]]
        dic_mensajes_regulares[(i[0], i[1])] = [["Inicio del chat","Mensaje del sistema",""]]


    for i in lineas_archivo_mensajes:                   # ahora rellenamos esas entradas
        mensaje = ""
        for j in i[4:]:                                  # reconstruimos los mensajes que
            if len(mensaje) != 0:                       # contenian comas y destruimos al hacer split
                mensaje = mensaje + ", " + j
            else:
                mensaje = j
        mensaje = mensaje.strip("\n")

        if i[0] == "grupo":
            tupla_mensaje_grupo = (i[1], i[3], mensaje)           # contenido -> (emisor,hora,mensaje)
            dic_mensajes_grupo[i[2]].append(tupla_mensaje_grupo)
        else:
            tupla_mensaje_regular = (i[1],i[3], mensaje)
            dic_mensajes_regulares[i[2], i[1]].append(tupla_mensaje_regular)
            dic_mensajes_regulares[i[1], i[2]].append(tupla_mensaje_regular)    # contenido -> (hora, mensaje)
    if tipo == "grupo":
        return dic_mensajes_grupo
    else:
        return dic_mensajes_regulares
