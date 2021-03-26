from Cargar_usuarios import cargar_usuarios, cargar_contactos

for i in cargar_usuarios("usuarios.csv"):
    for j in cargar_contactos("contactos.csv"):
        if str(i) == j[0]:
            i.agregar_contacto(j[1])


