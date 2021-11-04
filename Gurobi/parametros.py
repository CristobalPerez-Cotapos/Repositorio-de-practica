I_CENTROS_VAC = 1
J_TIPOS_VAC = 1
E_EMPRESAS_CAM = 1
M_METODOS_TRANSPORTE = 1
T_DIAS = 1

                                #parte de 0
def sumatoria(var, desde, hasta, posicion, base, par, dicc_par, pos_par, bas_par):
    resultado = 0
    if par:
        for i in range(desde, hasta+1):
            lista = []
            for j in range(len(base)):
                if j != posicion:
                    lista.append(base[j])
                else:
                    lista.append(i)
            lista = []
            for j in range(len(bas_par)):
                if j != pos_par:
                    lista.append(bas_par[j])
                else:
                    lista.append(i)
            print(lista)



    else:
        for i in range(desde, hasta+1):
            lista = []
            for j in range(len(base)):
                if j != posicion:
                    lista.append(base[j])
                else:
                    lista.append(i)
            print(lista)
            resultado += var[tuple(lista)]
    return resultado