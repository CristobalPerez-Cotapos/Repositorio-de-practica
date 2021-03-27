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