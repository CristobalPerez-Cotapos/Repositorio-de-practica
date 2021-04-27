# Tarea 1: DCCanal :school_satchel:

## Consideraciones generales :octocat:

* El codigo funciona y comple todo lo solicitado
* El codigo no altera los archivo .csv
* El programa no se ejecutará correctamente si hay lineas en blanco en cualquiera de los archivos .csv
* Se puede salir y volver en todos los menús, pero no desde cualquier parte del programa
* En algunas partes, para continuar, se debe escribir una de las opciones textual
* Al momento de ingresar un barco, solo se mostrarán 5 opciónes, con el fin de añadir realismo y no llenar al usuario con 40 barcos

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Flujo del programa:   
    * Menú de inicio: Hecho completo
    * Menú de acciones: Hecho completo
* Simular hora: Hecho completo
* Mostrar estado: Hecho completo


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ``Menu.py``.


## Librerías :books:
### Librerías externas utilizadas
Las librerias externas utilizadas fueron:

1. Random, de donde se uso la funcion randint
2. CurrencyConverter, de donde se uso la funcion currencyconverter
3. abc, de donde se uso ABC y abstractmethod

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. Parametros.py: Contiene los parametros que controlan parte de la simulacion
2. Entidades.py: Contiene toda la definición de las clases (canales, barcos, mercancia y tripuacion) que se usar en el codigo
3. Cargar_datos.py: Contiene las funciones que leén los achivos y devuelven listas, con los barcos y canales
NOTA: puede ser más facil leer los archivos en el orden que esta aquí

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Los archivos no contienen lineas vacías y siguen el mismo formato en todas las lineas




-------

