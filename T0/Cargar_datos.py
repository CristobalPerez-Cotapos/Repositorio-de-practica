
class Usuario:                                # La clase usuario será la forma en que se guardarán
    def __init__(self, nombre):               # todos los contactos y grupos de un individuo
        self.nombre = nombre
        self.contactos = set()
        self.grupos = []

    def __str__(self):
        return self.nombre
        pass

    def agregar_contacto(self, contacto):    # agrega los contactos
        self.contactos.add(contacto)

    def agregar_grupo(self, grupo):         # agrega los grupos de un usuario
        self.grupos.append(grupo)


def cargar_usuarios(path):                  # Devuelve una lista de todos los usuarios
    archivo = open(path, "r")               # transformados en la clase Usuario
    usuarios = archivo.readlines()
    archivo.close()
    lista_usuarios = []
    for i in usuarios:
        i = i.strip("\n")
        lista_usuarios.append(Usuario(i))
    return lista_usuarios


def cargar_contactos(path):                       # devuelve una lista con todos los contactos
    archivo = open(path, "r")                     # que están en el archivo
    contactos = archivo.readlines()
    archivo.close()
    lista_contactos = []
    contactos.pop(0)
    for i in contactos:
        i = i.strip("\n")
        i = i.split(",")
        lista_contactos.append(i)
        lista_contactos.append([i[1], i[0]])      # duplicamos los elementos en orden inverso, para
    return lista_contactos                        # facilitar la simetría entre contactos


def cargar_grupos(path):                               # devuelve una lista de listas que contienen
    archivo = open(path, "r")                          # los de grupos y usuarios de grupos.csv
    personas_por_grupo = archivo.readlines()
    archivo.close()
    for i in range(len(personas_por_grupo)):
        personas_por_grupo[i] = personas_por_grupo[i].strip("\n")
        personas_por_grupo[i] = personas_por_grupo[i].split(",")
    return personas_por_grupo
