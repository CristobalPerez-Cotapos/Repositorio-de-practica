from Cargar_usuarios import (cargar_usuarios,
                             cargar_contactos, cargar_grupos)
from Relacionar_contactos import (relacionar_contactos,
                                  relacionar_grupos, diccionarios_de_mensajes)
from Opciones_inicio import (agregar_usuario,detectar_usuario,
                             eniviar_mensaje_regular, agregar_contacto,
                             crear_grupo)


salir = False
while not salir:
    menu = "***** Menu de Inicio ***** \n \n " \
           "Selecciona una opción \n \n"
    opciones_1 = " [1] Crear usuario \n [2] " \
                 "Iniciar sesión \n [0] Salir"
    print(menu + opciones_1)
    opcion_elegida = input()
    if opcion_elegida == "0":
        print("Hasta luego, vuelve pronto para chatear "
              "con tus amigos :)")
        salir = True
    elif opcion_elegida == "1":
        print("Ingrese el nombre de usuario deseado, "
              "el cual no debe contener comas")
        nombre = input()
        if detectar_usuario(nombre):
            print(f"el usuario {nombre} ya existe,"
                  f"presione enter para volver al menu"
                  f" de inicio")
            input()
        else:
            agregar_usuario(nombre)
    elif opcion_elegida == "2":
        print("Ingrese su nombre de usuario")
        nombre_usuario = input()                              # este es el nombre del usuario
        if detectar_usuario(nombre_usuario):
            print(f"Un placer tenerte de vuelta {nombre_usuario}, presiona"
                  f" enter para continuar")
            input()                                            # Aquí el usuario ingresa al menu de chats
            volver = False
            while not volver:
                print("***** Menu de Chats *****"
                      "\n\nSelecciona una opción: \n\n"
                      "[1] Ver contactos \n"
                      "[2] Ver grupos \n"
                      "[0] Volver")
                opcion_elegida_chats = input()
                if opcion_elegida_chats == "0":
                    volver = True

                elif opcion_elegida_chats == "1":                   # Aquí empieza el menu de contactos
                    usuario = relacionar_contactos(nombre_usuario)  # función de Relacionar_contactos.py
                    salir_menu_contactos = False
                    while not salir_menu_contactos:
                        print("***** Menu de Contactos *****"
                              "\n\nSelecciona una opción: \n\n"
                              "[1] Ver contactos \n"
                              "[2] Añadir contacto \n"
                              "[0] Volver")
                        opcion_elegida_menu_contactos = input()
                        if opcion_elegida_menu_contactos == "1":                  #menu ver contactos COMPLETAR
                            print(f"Estos son tus contactos, {nombre_usuario}:")
                            for i in usuario.contactos:
                                print(i)
                            print("Ingresa el nombre del contacto con el "
                                  "que quieras hablar o presiona 0 "
                                  "para regresar al menu de contactos")
                            opcion_elegida_menu_ver_contactos = input()
                            if opcion_elegida_menu_ver_contactos in usuario.contactos:
                                chat = diccionarios_de_mensajes("regular")[str(usuario),
                                                                         opcion_elegida_menu_ver_contactos]
                                volver_frase = False
                                while not volver_frase:
                                    for i in chat:
                                        print(f"{i[1]},{i[0]} :\n {i[2]}")
                                    print("Escribe un mensaje o ingresa "
                                          "VOLVER_FRASE para volver al menu "
                                          "de contactos")
                                    eleccion_escribir = input()
                                    if eleccion_escribir == "VOLVER_FRASE":
                                        volver_frase = True
                                    else:
                                        print("Por favor escriba la hora a la que"
                                              " envía este mensaje, en el formato"
                                              " año/mes/dia hora:minuto:segundo")
                                        opcion_elegida_hora = input()
                                        eniviar_mensaje_regular(str(usuario),eleccion_escribir,
                                                                opcion_elegida_menu_ver_contactos,
                                                                opcion_elegida_hora)
                                        chat = diccionarios_de_mensajes("regular")[str(usuario),
                                                                                       opcion_elegida_menu_ver_contactos]



                                        ## implementar envio de mensajes


                            elif opcion_elegida_menu_ver_contactos == "0":
                                print("volviendo al menu de contactos, presiona enter")
                                input()
                            else:
                                print("Opcion no valida, presiona enter"
                                      " para volver al menu de contactos")
                                input()

                        elif opcion_elegida_menu_contactos == "2":
                            print("Escribe el nombre del contacto"
                                  " que deseas agregar")
                            contacto_a_agregar = input()
                            if detectar_usuario(contacto_a_agregar):
                                agregar_contacto(str(usuario), contacto_a_agregar)
                                usuario = relacionar_contactos(nombre_usuario)
                            else:
                                print("Este usuario no existe, presiona enter"
                                      "para volver al menu de contactos")
                                input()
                        elif opcion_elegida_menu_contactos == "0":
                            salir_menu_contactos = True
                        else:
                            print("Opción no valida, presiona"
                                  " enter para volver al menu "
                                  "de contactos")
                            input()


                elif opcion_elegida_chats == "2":                   # Aquí empieza el menu de grupos
                    volver_grupos = False
                    while not volver_grupos:
                        print("***** Menu de grupos *****"
                              "\n\nSelecciona una opción\n\n"
                              "[1] Ver grupos\n"
                              "[2] Crear grupo\n"
                              "[0] Volver\n")
                        opcion_menu_grupos = input()
                        if opcion_menu_grupos == "1":
                            usuario = relacionar_grupos(nombre_usuario)
                            print(f"Estos son tus grupos, {nombre_usuario}")
                            for i in usuario.grupos:
                                print(i)
                            input()
                            #implementar
                        elif opcion_menu_grupos == "2":
                            print("Escribe el nombre del grupo que deseas"
                                  " crear, o ingresa VOLVER para volver al menu"
                                  "de grupos")
                            opcion_crear_grupo_1 = input()
                            nombre_grupo_creado = opcion_crear_grupo_1
                            while opcion_crear_grupo_1 != "VOLVER":
                                print(f"Escribe el nombre de un usuario "
                                      f"que se unirá al grupo {nombre_grupo_creado}, o "
                                      f"escribe VOLVER para volver al menu "
                                      f"de grupos")
                                usuario_a_agregar = input()
                                opcion_crear_grupo_1 = usuario_a_agregar
                                if detectar_usuario(usuario_a_agregar):
                                    crear_grupo(nombre_grupo_creado,usuario_a_agregar)
                                elif usuario_a_agregar == "VOLVER":
                                    pass
                                else:
                                    print("este usuario no existe, presiona enter "
                                          "para intentarlo de nuevo")
                                    input()
                            # implementar
                            pass
                        elif opcion_menu_grupos == "0":
                            volver_grupos = True
                        else:
                            print("Opción elegida no valida,presiona"
                                  " enter para volver al menu de grupos")
                            input()

                else:
                    print("Opción no valida, intente de nuevo")

        else:
            print("Usuario no encontrado, presione enter"
                  " para volver al menu de inicio")
            input()
    else:
        print("Opción no valida, presione enter para "
              "volver al menu de inicio")
        input()
