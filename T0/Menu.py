from Cargar_usuarios import cargar_usuarios, cargar_contactos, cargar_grupos
from Relacionar_contactos import relacionar_contactos, relacionar_grupos, diccionarios
from Opciones_inicio import agregar_usuario, detectar_usuario


relacionar_contactos()
relacionar_grupos()

usuario_detectado = False

while usuario_detectado == False:
    menu = "***** Menu de Inicio ***** \n \n " \
           "Selecciona una opción \n \n"
    opciones_1 = " [1] Crear usuario \n [2] " \
                 "Iniciar sesión \n [0] Salir"
    print(menu + opciones_1)
    opcion_elegida = input()
    if opcion_elegida == "0":
        print("Hasta luego, vuelve pronto para chatear "
              "con tus amigos :)")
    elif opcion_elegida == "1":
        print("Ingrese el nombre de usuario deseado, "
              "el cual no debe contener comas")
        nombre = input()
        agregar_usuario(nombre)
    elif opcion_elegida == "2":
        print("Ingrese su nombre de usuario")
        nombre_usuario = input()                                    # este es el nombre del usuario
        if detectar_usuario(nombre_usuario):
            usuario_detectado = True
            print(f"Un placer tenerte de vuelta {nombre_usuario}, presiona"
                  f" enter para continuar")
        else:
            print("Usuario no encontrado, presione enter"
                  " para volver al menu de inicio")
            input()
    else:
        print("Opción no valida, presione enter para "
              "volver al menu de inicio")
        input()
