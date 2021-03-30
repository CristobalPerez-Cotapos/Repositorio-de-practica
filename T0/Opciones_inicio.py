from Cargar_datos import cargar_usuarios, cargar_grupos


def agregar_usuario(nombre):                         # La función crea un usuario y lo agrega a usuarios.csv
    usuarios = open("usuarios.csv", "r")
    lista_usuarios = usuarios.readlines()
    usuarios.close()
    lista_usuarios[-1] = lista_usuarios[-1] + "\n"
    lista_usuarios.append(nombre)
    texto_final = ""
    for i in lista_usuarios:
        texto_final = texto_final + i
    usuarios_nuevo = open("usuarios.csv", "w")
    usuarios_nuevo.write(texto_final)
    usuarios_nuevo.close()


def detectar_usuario(nombre):                  # La función detecta si existe un usuario o no
    lista_usuarios = cargar_usuarios("usuarios.csv")
    for i in lista_usuarios[1:]:
        if str(i) == nombre:
            return True
    return False


def eniviar_mensaje(tipo, emisor, mensaje, receptor, hora):    # La función recibe los datos del mensaje y escribe en
    mensajes = open("mensajes.csv", "r")                       # mensajes.csv
    lista_mensajes = mensajes.readlines()
    mensajes.close()
    lista_mensajes[-1] = lista_mensajes[-1] + "\n"
    texto = f"{tipo},{emisor},{receptor},{hora},{mensaje}"
    lista_mensajes.append(texto)
    texto_final = ""
    for i in lista_mensajes:
        texto_final = texto_final + i
    mensajes_nuevo = open("mensajes.csv", "w")
    mensajes_nuevo.write(texto_final)
    mensajes_nuevo.close()


def agregar_contacto(usuario_1, usuario_2):                    # La función recibe el nombre de dos usuarios y
    contactos = open("contactos.csv", "r")                     # los agrega como contactos en contactos. cvs
    lista_contactos = contactos.readlines()
    contactos.close()
    lista_contactos[-1] = lista_contactos[-1] + "\n"
    texto = usuario_1+","+usuario_2
    lista_contactos.append(texto)
    texto_final = ""
    for i in lista_contactos:
        texto_final = texto_final + i
    contactos_nuevo = open("contactos.csv", "w")
    contactos_nuevo.write(texto_final)
    contactos_nuevo.close()


def crear_grupo(grupo, usuario):                              # La función recibe dos strings, y crea un string
    grupos = open("grupos.csv", "r")                          # grupo,usuarios (igual a los del archivo de contactos)
    lista_grupos = grupos.readlines()                         # y lo agrega a grupos.csv
    grupos.close()
    lista_grupos[-1] = lista_grupos[-1] + "\n"
    texto = grupo + "," + usuario
    lista_grupos.append(texto)
    texto_final = ""
    for i in lista_grupos:
        texto_final = texto_final + i
    grupos_nuevo = open("grupos.csv", "w")
    grupos_nuevo.write(texto_final)
    grupos_nuevo.close()


def abandonar_grupo(grupo, usuario):                   # La función recibe el nombre de un grupo y de un usuario
    grupos = open("grupos.csv", "r")                   # y borra esa relación del archivo grupos.csv
    lista_grupos = grupos.readlines()
    grupos.close()
    for i in range(len(lista_grupos)):
        if grupo in lista_grupos[i] and usuario in lista_grupos[i]:
            numero_a_eliminar = i
    lista_grupos.pop(numero_a_eliminar)               # La variable esta referenciada, por que esta opción solo
    texto_final = ""                                  # aparece para una persona que está en un grupo
    for i in lista_grupos:                            # siempre se alcanzará a referenciar
        texto_final = texto_final + i
    grupos_nuevo = open("grupos.csv", "w")
    grupos_nuevo.write(texto_final)
    grupos_nuevo.close()


def condiciones_grupo(grupo):                           # Esta función comprueba que el grupo tenga las condiciones
    lista_grupos = cargar_grupos("grupos.csv")       # para ser creado
    if len(grupo) < 1:
        return False
    for i in lista_grupos[1:]:
        if i[0] == grupo:
            return False
    return True


def en_el_grupo(grupo,usuario):
    lista_grupos = cargar_grupos("grupos.csv")
    for i in lista_grupos:
        if i[0] == grupo and i[1] == usuario:
            return True
    return False
