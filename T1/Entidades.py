from abc import ABC, abstractmethod
from Parametros import (MULTA_ALIMENTOS, MULTA_ROPA, MULTA_PETROLEO, DINERO_INICIAL, COBRO_USO_PRINCIPIANTE,
                        COBRO_USO_AVANZADO, COSTO_DESENCALLAR, PROB_BASE_DESENCALLAR, PONDERADOR_AVANZADO,
                        PONDERADOR_PRINCIPIANTE, TENDENCIA_ENCALLAR_CARGUERO, TENDENCIA_ENCALLAR_BUQUE,
                        TENDENCIA_ENCALLAR_PASAJEROS, TIEMPO_AVERIA_BUQUE, DINERO_INTOXICACION,
                        PROBABILIDAD_EVENTO_ESPECIAL, CARGA_EXTRA_CARGUERO)
from random import randint


class Barcos(ABC):

    def __init__(self, nombre, tipo, costo_de_mantencion, velocidad_base, pasajeros, carga_maxima,
                 moneda_de_origen, tripulacion, carga):
        self.nombre = nombre
        self.costo_de_mantencion = costo_de_mantencion
        self.velocidad_base = velocidad_base
        self.nombre_pasajeros = pasajeros                               # con los objetos pasajeros
        self.carga_maxima = carga_maxima
        self.moneda_de_origen = moneda_de_origen
        self.tipo = tipo
        self.nombres_tripulacion = tripulacion     # Son los nombres, pero va a haber una lista
        self.tripulacion = []                      # Con los objetos tripulación
        self.codigos_carga = carga
        self.carga = []                            # idem, pero con la carga
        self.encallado = False               # indica si está encallado o no
        self.avance = 0                     # indica cuanto ha avanzado el barco
        self.canal = None
        self.ocurrencia_evento = False
        self.horas_en_canal = 0

    def __str__(self):
        return f"Este barco es el {self.nombre}, con tripulación {self.nombres_tripulacion}"

    def desplazarse(self):  # Falta bloquear el paso cuando encalla algo delante
        minimo = min(1, (self.carga_maxima - self.peso_mercancia-(0.3*len(self.nombre_pasajeros)))/self.carga_maxima)
        maximo = max(0.1, minimo)
        desplazmiento = maximo * self.velocidad_base
        self.avance += desplazmiento
        pass

    @property
    def peso_mercancia(self):  # Completa
        peso = 0
        for i in self.carga:
            peso += i.peso
        return peso

    @property
    def exp_tripulacion(self):
        exp_total = 0
        for i in self.tripulacion:
            exp_total += i.experiencia
        return exp_total

    @abstractmethod
    def encallar(self):
        ecuacion = (self.velocidad_base + self.peso_mercancia - self.exp_tripulacion)/120
        return min(1, ecuacion)

    @abstractmethod
    def ejecutar_evento_especial(self):
        pass


class Barco_de_pasajeros(Barcos):

    def ejecutar_evento_especial(self):
        azar = randint(1, 100)
        if azar > PROBABILIDAD_EVENTO_ESPECIAL and not self.ocurrencia_evento:
            print(f"El barco {self.nombre} se ha intoxicado, debe pagar {DINERO_INTOXICACION} al canal {self.canal}")
            self.canal.dinero += DINERO_INTOXICACION
            self.ocurrencia_evento = True

    def encallar(self):
        base = super().encallar()
        prob_encallar = base * TENDENCIA_ENCALLAR_PASAJEROS
        azar = randint(1, 100)
        if prob_encallar > azar:
            print(f"El barco {self.nombre} ha encallado")
            self.encallado = True


class Barco_carguero(Barcos):

    def ejecutar_evento_especial(self):        # Recordar que barco atacado no paga tarifa
        azar = randint(1, 100)
        if azar > PROBABILIDAD_EVENTO_ESPECIAL and not self.ocurrencia_evento:
            print(f"¡¡El barco {self.nombre} ha sido atacado por piratas!! han perdido toda su mercancía"
                  f"y no podrán pagar la tarifa al canal {self.canal}")
            self.carga = []
            self.ocurrencia_evento = True

    def encallar(self):
        base = super().encallar()
        prob_encallar = base * TENDENCIA_ENCALLAR_CARGUERO
        azar = randint(1, 100)
        if prob_encallar > azar:
            print(f"El barco {self.nombre} ha encallado")
            self.encallado = True


class Buque(Barcos):

    def ejecutar_evento_especial(self):       # Recordar que este barco no avanza algunas horas
        azar = randint(1, 100)
        if azar > PROBABILIDAD_EVENTO_ESPECIAL and not self.ocurrencia_evento:
            print(f"El barco {self.nombre} ha sufrido una avería, no podrá avanzar durante {TIEMPO_AVERIA_BUQUE} horas")
            self.ocurrencia_evento = True

    def encallar(self):
        base = super().encallar()
        prob_encallar = base * TENDENCIA_ENCALLAR_BUQUE
        azar = randint(1, 100)
        if prob_encallar > azar:
            print(f"El barco {self.nombre} ha encallado")
            self.encallado = True


class Mercancia:  # Completada

    def __init__(self, lote, tipo, tiempo_expiracion, peso):
        self.lote = lote
        self.tipo = tipo
        self.tiempo_expiracion = tiempo_expiracion
        self.peso = peso
        self.barco = None

    def expirar(self):            # solamente devuelve el monto que se debe cobrar
        if self.tipo == "petroleo":
            multa = MULTA_PETROLEO
        elif self.tipo == "ropa":
            multa = MULTA_ROPA
        elif self.tipo == "alimentos":
            multa = MULTA_ALIMENTOS
        else:
            print("Error al calcular la multa, multa = 0")
            multa = 0
        self.barco.canal.dinero -= multa
        print(f"Se ha cobrado {multa} al canal {self.barco.canal}")


class Tripulacion(ABC):
    def __init__(self, nombre, experiencia):
        self.nombre = nombre
        self.experiencia = experiencia
        self.barco = None
        self.uso_habilidad = False

    @abstractmethod
    def especialidad(self):
        pass


class DCCapitan(Tripulacion):

    def especialidad(self):
        if self.barco.encallado and not self.uso_habilidad:
            self.barco.encallado = False
            self.uso_habilidad = True


class DCCocinero(Tripulacion):

    def especialidad(self):
        if not self.uso_habilidad:
            objetos = self.barco.carga
            for i in objetos:
                i.tiempo_expiracion = i.tiempo_expiracion * 2
        self.uso_habilidad = True


class DCCarguero(Tripulacion):

    def especialidad(self):
        if not self.uso_habilidad:
            self.barco.carga_maxima += CARGA_EXTRA_CARGUERO


class Canal:

    def __init__(self, nombre, largo, dificultad):
        self.nombre = nombre
        self.dinero = DINERO_INICIAL
        self.largo = largo
        self.dificultad = dificultad
        self.barcos = []

    @property
    def cobro_de_uso(self):
        if self.dificultad == "avanzado":
            return COBRO_USO_AVANZADO
        else:
            return COBRO_USO_PRINCIPIANTE

    @property
    def probablidad_de_desencallar(self):
        if self.dificultad == "avanzado":
            return PROB_BASE_DESENCALLAR * PONDERADOR_AVANZADO
        else:
            return PROB_BASE_DESENCALLAR * PONDERADOR_PRINCIPIANTE

    def ingresar_barco(self, barco):    # esto solo se debe usar para un barco que no esté en el canal
        self.barcos.append(barco)

    def avanzar_barcos(self):
        pass

    def desencallar_barco(self, barco):
        self.dinero -= COSTO_DESENCALLAR
        azar = randint(1, 100)
        if self.probablidad_de_desencallar >= azar:
            barco.encallado = False
            print(f"El barco {barco.nombre} ha sido desencallado con éxito :D")
            pass
        else:
            print(f"No se ha podido desencallar el barco {barco.nombre} :( ")
            pass
