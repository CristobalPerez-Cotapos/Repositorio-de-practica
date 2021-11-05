Entrga 2 del proyecto de óptimización

Hola!! Los archivos.py del proyecto son los que usamos para optimizar el modelo, aqui se encuentra:
- Paramtros.py: Contiene el largo de los conjuntos, están en un archivo aparte para facilitar su edición
- main.py: Es el archivo que contiene toda nuestra programación de gurobi, para usarlo hay que tener ojo que en las primeras lineas debe leer un archivo de excel, que contendrá los datos 
- Datos proyecto.xlsx: Contiene los datos usados para optimizar el proyecto, además de que significa cada uno y algunos calculos de interés
- Datos este si que si.xlsx: Este archivo contiene los mismos datos que Datos Proyecto.xlsx, pero ordenados de una forma que se facilita su lectura para optimizar.


Para ejecutar main.py es necesario contar con las siguientes librerías externas:
- gurobipy: Contiene la clase Model que utilizaremos para optimizar
- openpyxl: Esta librería contiene una serie de clases y metodos para facilitar la lectura de archivos tipo xlsx

En el archivo.py se cuenta con las mismas restricciones, variables y parametros que las descritas en el modelo, y usa los valores de los archivos.xlsx