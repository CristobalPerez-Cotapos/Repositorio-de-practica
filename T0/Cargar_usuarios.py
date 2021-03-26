
class Usuario:                                # Creamos la Clase usuario para manejar el programa
    def __init__(self, nombre):
        self.nombre = nombre
        self.contactos = []
        self.grupos = []

    def __str__(self):
        return self.nombre
        pass

    def agregar_contacto(self, contacto):    # Los contactos serán llaves para un diccionario de chats
        self.contactos.append(contacto)      # los chats serán namedtuples
        pass


def cargar_usuarios(path):
    archivo = open(path, "r")
    usuarios = archivo.readlines()
    lista_usuarios = []
    for i in usuarios:
        i = i.strip("\n")
        lista_usuarios.append(Usuario(i))
    return lista_usuarios


def cargar_contactos(path):
    archivo = open(path, "r")
    contactos = archivo.readlines()
    lista_contactos = []
    contactos.pop(0)
    for i in contactos:
        i = i.strip("\n")
        i = i.split(",")
        lista_contactos.append(i)
        lista_contactos.append([i[1], i[0]])      # duplicamos los elementos en orden inverso, para
    return lista_contactos                        # facilitar la simetría


