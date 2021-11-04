from gurobipy import GRB, Model, quicksum
from openpyxl import load_workbook
import parametros as p

model = Model("Distribución de tercera dosis")

ruta_datos = "Datos proyecto.xlsx"
libro_datos = load_workbook(ruta_datos)

hojas = libro_datos.get_sheet_names()

letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

## Primero cargamos los parametros

diccionario_parametros = {}

for hoja in hojas:
    sheet = libro_datos[hoja]
    filas = sheet.max_row
    columnas = sheet.max_column
    diccionario_parametros[hoja] = {}
    for i in range(filas):
        diccionario_parametros[hoja][i+1] = {}
        for j in range(columnas):
            diccionario_parametros[hoja][i+1][j+1] = sheet[letras[j] + str(i+1)].value
for i in diccionario_parametros:
    print(diccionario_parametros[i])

## Luego definimos las variables


R_ijtm = {}
for i in range(p.I_CENTROS_VAC):
    for j in range(p.J_TIPOS_VAC):
        for t in range(p.T_DIAS):
            for m in range(p.M_METODOS_TRANSPORTE):
                R_ijtm[(i+1, j+1, t+1, m+1)] = model.addVar(
                    vtype=GRB.INTEGER, name=f"R_{str(i+1)}{str(j+1)}{str(t+1)}{str(m+1)}")

CT_mt = {}
for m in range(p.M_METODOS_TRANSPORTE):
    for t in range(p.T_DIAS):
        CT_mt[(m+1, t+1)] = model.addVar(vtype=GRB.INTEGER, name=f"CT_{str(m+1)}{str(t+1)}")

CC_imt = {}
for i in range(p.I_CENTROS_VAC):
    for m in range(p.M_METODOS_TRANSPORTE):
        for t in range(p.T_DIAS):
            CC_imt[(i+1, m+1, t+1)] = model.addVar(
                vtype=GRB.INTEGER, name=f"CC_{str(i+1)}{str(m+1)}{str(t+1)}")

CN_mt = {}
for m in range(p.M_METODOS_TRANSPORTE):
    for t in range(p.T_DIAS):
        CT_mt[(m+1, t+1)] = model.addVar(vtype=GRB.INTEGER, name=f"CN_{str(m+1)}{str(t+1)}")

CA_met = {}
for m in range(p.M_METODOS_TRANSPORTE):
    for e in range(p.E_EMPRESAS_CAM):
        for t in range(p.T_DIAS):
            CA_met[(m+1, e+1, t+1)] = model.addVar(
                vtype=GRB.INTEGER, name=f"CA_{str(m+1)}{str(e+1)}{str(t+1)}")

I_tj = {}
for t in range(p.T_DIAS):
    for j in range(p.J_TIPOS_VAC):
        I_tj[(t+1, j+1)] = model.addVar(vtype=GRB.INTEGER, name=f"I_{str(t+1)}{str(j+1)}")

E_et = {}
for e in range(p.E_EMPRESAS_CAM):
    for t in range(p.T_DIAS):
        E_et[(e+1, t+1)] = model.addVar(vtype=GRB.INTEGER, name=f"E_{str(e+1)}{str(t+1)}")

DES_et = {}
for e in range(p.E_EMPRESAS_CAM):
    for t in range(p.T_DIAS):
        DES_et[(e+1, t+1)] = model.addVar(vtype=GRB.INTEGER, name=f"DES_{str(e+1)}{str(t+1)}")

VP_t = {}
for t in range(p.T_DIAS):
    VP_t[(t+1)] = model.addVar(vtype=GRB.INTEGER, name=f"VP_{str(t+1)}")

model.update()

## Después declaramos las restricciones

for i in range(p.I_CENTROS_VAC):
    for m in range(p.M_METODOS_TRANSPORTE):
        for t in range(p.T_DIAS):
            model.addConstr(quicksum(R_ijtm[(i +1, j+1 , t +1, m+1)] * diccionario_parametros["VOL_j"][1][j+1] for j in range(p.J_TIPOS_VAC))
                            <= diccionario_parametros["CAP_m"][1][m+1] *diccionario_parametros[f"CC_{str(i+1)}mt"][m+1][t+1],
                            name="R1")
for i in range(p.I_CENTROS_VAC):
    for j in range(p.J_TIPOS_VAC):
        for t in range(p.T_DIAS):
            model.addConstr(diccionario_parametros[f"DE_{str(i+1)}jt"][j+1][t+1] <=
                            quicksum(R_ijtm[(i+1, j+1, t+1, m+1)] * diccionario_parametros["CAC_j"][1][j+1]
                                     * diccionario_parametros["PPC_m"][1][m+1] for m in range(p.M_METODOS_TRANSPORTE)),
                            name= "R2")

for i in range(p.I_CENTROS_VAC):
    for t in range(p.T_DIAS):
        model.addConstr(quicksum(diccionario_parametros[f"DE_{str(i+1)}jt"] for j in range(p.J_TIPOS_VAC))
                        <= quicksum(R_ijtm[(i+1, j+1, t+1, m+1)] * diccionario_parametros["CAC_j"][1][j+1]
                                     * diccionario_parametros["PPC_m"][1][m+1] for j in range(p.J_TIPOS_VAC)
                                    for m in range(p.M_METODOS_TRANSPORTE)),
                        name="R3")

for j in range(p.J_TIPOS_VAC):
    for t in range(1, p.T_DIAS):
        model.addConstr(diccionario_parametros["V_jt"][j+1][t+1] + I_tj[j+1][t] * diccionario_parametros["PP_j"][1][j+1] ==
                        quicksum(R_ijtm[(i +1, j+1 , t +1, m+1)] for i in range(p.I_CENTROS_VAC) for m in range(p.M_METODOS_TRANSPORTE)) + I_tj[(t+1, j+1)]
                        , name="R4")

for j in range(p.J_TIPOS_VAC):
    for t in range(1):
        model.addConstr(diccionario_parametros["V_jt"][j+1][t+1] + diccionario_parametros["a_j"][1][j+1] * diccionario_parametros["PP_j"][1][j+1] ==
                        quicksum(R_ijtm[(i +1, j+1 , t +1, m+1)] for i in range(p.I_CENTROS_VAC) for m in range(p.M_METODOS_TRANSPORTE)) + I_tj[(t+1, j+1)]
                        , name="Caso limite de inventario")

for t in range(1,p.T_DIAS):
    model.addConstr(
        VP_t[t+1] == quicksum(quicksum(quicksum(R_ijtm[(i +1, j+1 , t +1, m+1)] * diccionario_parametros["CAC_j"][1][j+1] for m in range(p.M_METODOS_TRANSPORTE))
                                       -diccionario_parametros["DE_ijt"][i+1][j+1][t+1] for j in range(p.J_TIPOS_VAC))-diccionario_parametros["DG_it"][i+1][t+1] for i in range(p.I_CENTROS_VAC))
                              +quicksum(I_tj[(t, j+1)] * (1-diccionario_parametros["PP_j"][1][j+1]) for j in range(p.J_TIPOS_VAC)) + quicksum(R_ijtm[(i +1, j+1 , t +1, m+1)] * diccionario_parametros["CAC_j"][1][j+1] * (1- diccionario_parametros["PPC_m"][1][m+1]) for m in range(p.M_METODOS_TRANSPORTE) for j in range(p.J_TIPOS_VAC) for i in range(p.I_CENTROS_VAC)),
    name = "R5")

for t in range(1):
    model.addConstr(
        VP_t[t+1] == quicksum(quicksum(quicksum(R_ijtm[(i +1, j+1 , t +1, m+1)] * diccionario_parametros["CAC_j"][1][j+1] for m in range(p.M_METODOS_TRANSPORTE))
                                    -diccionario_parametros["DE_ijt"][i+1][j+1][t+1] for j in range(p.J_TIPOS_VAC))-diccionario_parametros["DG_it"][i+1][t+1] for i in range(p.I_CENTROS_VAC))
                            + quicksum(R_ijtm[(i +1, j+1 , t +1, m+1)] * diccionario_parametros["CAC_j"][1][j+1] * (1- diccionario_parametros["PPC_m"][1][m+1]) for m in range(p.M_METODOS_TRANSPORTE) for j in range(p.J_TIPOS_VAC) for i in range(p.I_CENTROS_VAC)), name = "Caso limite vacunas perdidas")


for t in range(p.T_DIAS):
    for m in range(p.M_METODOS_TRANSPORTE):
        model.addConstr(quicksum(CC_imt[(i+1, m+1, t+1)] for i in range(p.I_CENTROS_VAC)) <= CT_mt[(m+1, t+1)] + quicksum(CA_met[(m+1, e+1, t+1)] for e in range(p.E_EMPRESAS_CAM)), name= "R6")


for m in range(p.M_METODOS_TRANSPORTE):
    for t in range(1,p.T_DIAS):
        model.addConstr(CT_mt[(m+1, t+1)]==diccionario_parametros["CIN_m"][1][m+1]+ quicksum(CN_mt[(m+1,k+1)] for k in range(t)), name = "R7")

for m in range(p.M_METODOS_TRANSPORTE):
    for t in range(1):
        model.addConstr(CT_mt[(m+1, t+1)]==diccionario_parametros["CIN_m"][1][m+1], name = "Caso limite camiones")


for m in range(p.M_METODOS_TRANSPORTE):
    for t in range(p.T_DIAS):
        model.addConstr(CN_mt[(m+1,t+1)]<= diccionario_parametros["CD_mt"][m+1][t+1], name = "R8")

for m in range(p.M_METODOS_TRANSPORTE):
    for e in range(p.E_EMPRESAS_CAM):
        for t in range(p.T_DIAS):
            model.addConstr(CA_met[(m+1, e+1, t+1)<= diccionario_parametros[f"CAM_{str(m+1)}et"][e+1][t+1]*E_et[(e+1, t+1)], name = "R9")



for e in range(p.E_EMPRESAS_CAM):
    for t in range(p.T_DIAS):
        if t > 8:
            model.addConstr(quicksum(E_et[(e+1,k+1)] for k in range(t-7,t)) <=
                            6 + (t+1) * DES_et[(e+1,t+1)],
                            name="R10")

for t in range(p.T_DIAS):
    model.addConstr(quicksum(CT_mt[(m+1,t+1)] for m in range(p.M_METODOS_TRANSPORTE))<=
                    diccionario_parametros["MES"][1][1],
                    name="R11")
                    
