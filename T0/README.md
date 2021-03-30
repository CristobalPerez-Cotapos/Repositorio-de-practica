# Tarea 0: DCConecta2 :school_satchel:

## Consideraciones generales :octocat:

* El codigo funciona y comple todo lo solicitado
* Siempre que se crea un usuario, grupo, contacto o mensaje todo queda registrado en su respectivo archivo .csv, por lo que todo quedara registrado para la proxima vez que se ejecute el programa
* El programa no se ejecutará correctamente si hay lineas en blanco en cualquiera de los archivos .csv


### Cosas implementadas y no implementadas :white_check_mark: :x:

* Menú de inicio: Hecho completa
* Flujo del programa:   
    * Menú de contactos: Hecho completo
    * Menú de chats: Hecho completo
    * Menú de grupos: Hecho completo
* Chats:
    * Chats de grupo: Hecho completo
    * Chats regulares: Hecho completo


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ``Menu.py``.


## Librerías :books:
### Librerías externas utilizadas
La unica libreria externa que utilicé fue la siguiente:

1. datetime: datetime / datetime : importé esto para agregarle la hora a los mensajes creados

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. Cargar_datos.py: Contiene las funciones que leén los achivos y devuelven listas, junto con la definición de la clase Usuario 
2. Relacionar_datos.py: Contiene funciones que relacionan los contactos, grupos y mensajes de los usuarios 
3. Opciones_inicio.py: Contiene funciones que realizan las acciones del usuario (enviar mensajes, abandonar grupos, etc.)
NOTA: puede ser más facil leer los archivos en el orden que esta aquí

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Los archivos no contienen lineas vacías y siguen el mismo formato en todas las lineas
2. Los datos de mensajes.csv estaran ordenados por fecha (en todos los del archivo original esto es así, y los nuevos mensajes que se creen se crearan con la fecha actual y al final del programa)
3. En el archivo grupos.csv original no hay datos duplicados




-------

