from Cargar_datos import (cargar_barcos, cargar_canales)

salir = False
while not salir:
    print("*** Menú de Inicio ***\n\n"
          "Selecciona una opción: \n"
          "[1] Comenzar una nueva simulación \n"
          "[2] Salir")
    opcion_inicio = input()
    if opcion_inicio == "1":
        canal_existente = False
        print("Escribe el nombre del canal que deseas simular \n")
        for i in range(len(cargar_canales())):
            print(f"{cargar_canales()[i].nombre}")
        opcion_canal = input()
        for i in cargar_canales():
            if opcion_canal == i.nombre:
                canal = i
                print("Canal seleccionado exitosamente \n")
                canal_existente = True
        if canal_existente:
            volver_1 = False
            while not salir and not volver_1:
                print("*** Menu de Acciones ***\n\n"
                      "Selecciona una opción: \n"
                      "[1] Mostrar riesgo de encallamiento\n"
                      "[2] Desencallar Barco\n"
                      "[3] Simular nueva hora\n"
                      "[4] Mostrar estado\n"
                      "[5] Volver\n"
                      "[6] Salir\n")
                opcion_accion = input()
                if opcion_accion == "1":
                    if len(canal.barcos) == 0:
                        print("No tienes barcos en el canal, presiona enter para volver al menú de acciones")
                        input()
                    else:
                        for i in canal.barcos:
                            prob = str(i.prob_encallar)
                            print(f"El barco {i.nombre} tiene una probabilidad de encallar de {prob}%")
                        print("Presiona enter para volver al menú de acciones")
                        input()
                elif opcion_accion == "2":
                    if canal.hay_encallado:
                        print("Barcos encallados:")
                        for i in canal.barcos:
                            if i.encallado:
                                print(i.nombre)

                        if not canal.intento_desencallar:
                            print("Escribe el nombre del barco que deseas desencallar, o escribe ´volver´ para volver")
                            opcion_desencallar = input()
                            if opcion_desencallar != "volver":
                                barco_elegido_real = False
                                for i in canal.barcos:
                                    if opcion_desencallar == i.nombre:
                                        canal.desencallar_barco(i)
                                        barco_elegido_real = True
                                if not barco_elegido_real:
                                    print("Opción de barco no aceptada, volviendo al menu de acciones")
                        else:
                            print("Solo se puede intentar desencallar un barco cada hora, simula nueva hora para"
                                  " intentarlo nuevamente.\nPresiona enter para volver al menu de acciones")
                            input()
                    else:
                        print("No hay ningún barco encallado :D Presiona enter para continuar")
                        input()
                elif opcion_accion == "3":
                    if canal.hay_encallado:
                        print("El canal esta bloqueado, no pueden ingresar nuevos barcos. Presiona enter para continuar")
                        input()
                    else:
                        eleccion_echa = False
                        while not eleccion_echa:
                            print("Los siguientes barcos esperan a entrar al canal, escribe el nombre \n"
                                  "de uno para hacerlo pasar, o escribe NINGUNO para que no ingrese ninguno")
                            contador = 0
                            contador_2 = 0
                            nombres_barcos = []
                            contador_limite = False
                            while contador_2 < 5 and not contador_limite:
                                if not canal.barco_en_el_canal(cargar_barcos()[contador]):
                                    nombres_barcos.append(cargar_barcos()[contador].nombre)
                                    print(f"{cargar_barcos()[contador].nombre}, tipo {cargar_barcos()[contador].tipo}")
                                    contador += 1
                                    contador_2 += 1
                                else:
                                    contador += 1
                                if contador >= len(cargar_barcos()):
                                    contador = 0
                                    contador_limite = True
                            barco_a_ingresar = input()
                            if barco_a_ingresar == "NINGUNO":
                                print("No se ha ingresado a ningún barco")
                                eleccion_echa = True
                            elif barco_a_ingresar in nombres_barcos:
                                eleccion_echa = True
                                for i in cargar_barcos():
                                    if i.nombre == barco_a_ingresar:
                                        canal.ingresar_barco(i)
                                        i.canal = canal
                                        print(f"{i.nombre} ha ingresado al canal, presiona enter para continuar")
                                        input()
                            else:
                                print("Opción elegida no valida, presiona enter para intentarlo de nuevo")
                                input()
                    print("** Iniciando nueva hora **")
                    canal.avanzar_barcos()
                    for i in canal.barcos:
                        i.usar_especialidades()
                    canal.pagar_mantenimiento()
                    for i in canal.barcos:
                        for j in i.carga:
                            j.expirar()
                    for i in range(len(canal.barcos)):
                        if canal.barcos[i].avance >= canal.largo:
                            canal.barcos[i].avance = 0
                            canal.dinero += canal.cobro_de_uso
                            canal.dinero_recibido += canal.cobro_de_uso
                            print(f"{canal.barcos[i]} ha salido del canal, y ha pagado {canal.cobro_de_uso} al canal")
                            canal.barcos.pop(i)
                    canal.horas_simuladas += 1
                    print("Presiona Enter para continuar")
                    input()


                    pass
                elif opcion_accion == "4":
                    print(f"*** Estado del canal *** \n"
                          f"\n---------------------------------------------------\n"
                          f"{canal.nombre}, de {canal.largo} Km de largo, con dificultad {canal.dificultad} \n"
                          f"Horas simuladas: {canal.horas_simuladas}\n"
                          f"Dinero disponible: {canal.dinero}\n"
                          f"Dinero gastado: {canal.dinero_gastado}\n"
                          f"Dinero recibido: {canal.dinero_recibido}\n"
                          f"Número de barcos que pasaron: {canal.barcos_que_pasaron}\n"
                          f"Numero de barcos que encallaron: {canal.barcos_que_encallaron}\n"
                          f"Eventos especiales ocurridos: {canal.eventos_especiales_ocurridos}\n\n"
                          f"---------------------------------------------------\n"
                          f"Presiona enter para volver al menú de acciones")
                    input()
                elif opcion_accion == "5":
                    volver_1 = True
                    print("Volviendo al menú de inicio, presiona enter")
                    input()
                elif opcion_accion == "6":
                    salir = True
        else:
            print("El canal seleccionado no existe, presiona enter para volver al menú de inicio")
            input()
    elif opcion_inicio == "2":
        salir = True
    else:
        print("Opción no valida, presiona enter para volver al menu de inicio")
        input()
print("Has salido de la simulación, esperamos verte pronto")
