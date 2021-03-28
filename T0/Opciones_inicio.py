from Cargar_usuarios import cargar_usuarios

def agregar_usuario(nombre):
    usuarios = open("usuarios.csv","r")
    lista_usuarios = usuarios.readlines()
    usuarios.close()
    lista_usuarios[-1] = lista_usuarios[-1] + "\n"
    lista_usuarios.append(nombre)
    texto_final = ""
    for i in lista_usuarios:
        texto_final = texto_final +i
    usuarios_nuevo = open("usuarios.csv", "w")
    usuarios_nuevo.write(texto_final)
    usuarios_nuevo.close()

def detectar_usuario(nombre):
    lista_usuarios = cargar_usuarios("usuarios.csv")
    for i in lista_usuarios[1:]:
        if str(i) == nombre:
            return True
    return False

def eniviar_mensaje_regular(emisor, mensaje, receptor ,hora):
    mensajes = open("mensajes.csv", "r")
    lista_mensajes = mensajes.readlines()
    mensajes.close()
    lista_mensajes[-1] = lista_mensajes[-1] + "\n"
    texto = f"regular,{emisor},{receptor},{hora},{mensaje}"
    lista_mensajes.append(texto)
    texto_final = ""
    for i in lista_mensajes:
        texto_final = texto_final + i
    mensajes_nuevo = open("mensajes.csv", "w")
    mensajes_nuevo.write(texto_final)
    mensajes_nuevo.close()

def agregar_contacto(usuario_1,usuario_2):
    contactos = open("contactos.csv", "r")
    lista_contactos = contactos.readlines()
    contactos.close()
    lista_contactos[-1] = lista_contactos[-1] + "\n"
    texto = f"{usuario_1,usuario_2}"
    lista_contactos.append(texto)
    texto_final = ""
    for i in lista_contactos:
        texto_final = texto_final + i
    contactos_nuevo = open("contactos.csv", "w")
    contactos_nuevo.write(texto_final)
    contactos_nuevo.close()