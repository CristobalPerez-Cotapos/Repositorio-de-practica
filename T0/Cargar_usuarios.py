
class Usuario:                                # Creamos la Clase usuario para manejar el programa
    def __init__(self, nombre):
        self.nombre = nombre
        self.contactos = set()
        self.grupos = []

    def __str__(self):
        return self.nombre
        pass

    def agregar_contacto(self, contacto):    # Los contactos serán llaves para un diccionario de chats
        self.contactos.add(contacto)      # los chats serán namedtuples

    def agregar_grupo(self,grupo):
        self.grupos.append(grupo)




def cargar_usuarios(path):
    archivo = open(path, "r")
    usuarios = archivo.readlines()
    archivo.close()
    lista_usuarios = []
    for i in usuarios:
        i = i.strip("\n")
        lista_usuarios.append(Usuario(i))
    return lista_usuarios


def cargar_contactos(path):
    archivo = open(path, "r")
    contactos = archivo.readlines()
    archivo.close()
    lista_contactos = []
    contactos.pop(0)
    for i in contactos:
        i = i.strip("\n")
        i = i.split(",")
        lista_contactos.append(i)
        lista_contactos.append([i[1], i[0]])      # duplicamos los elementos en orden inverso, para
    return lista_contactos                        # facilitar la simetría

def cargar_grupos(path):
    archivo = open(path, "r")
    personas_por_grupo = archivo.readlines()
    archivo.close()
    for i in range(len(personas_por_grupo)):
        personas_por_grupo[i] = personas_por_grupo[i].strip("\n")
        personas_por_grupo[i] = personas_por_grupo[i].split(",")
    return personas_por_grupo

