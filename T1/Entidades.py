from abc import ABC, abstractmethod
from Parametros import (MULTA_ALIMENTOS, MULTA_ROPA, MULTA_PETROLEO, DINERO_INICIAL, COBRO_USO_PRINCIPIANTE,
                        COBRO_USO_AVANZADO, COSTO_DESENCALLAR, PROB_BASE_DESENCALLAR, PONDERADOR_AVANZADO,
                        PONDERADOR_PRINCIPIANTE, TENDENCIA_ENCALLAR_CARGUERO, TENDENCIA_ENCALLAR_BUQUE,
                        TENDENCIA_ENCALLAR_PASAJEROS, TIEMPO_AVERIA_BUQUE, DINERO_INTOXICACION,
                        PROBABILIDAD_EVENTO_ESPECIAL, CARGA_EXTRA_CARGUERO)
from random import randint
from currency_converter import CurrencyConverter


class Barcos(ABC):

    def __init__(self, nombre, tipo, costo_de_mantencion, velocidad_base, pasajeros, carga_maxima,
                 moneda_de_origen, tripulacion, carga):
        self.nombre = nombre
        self.costo_de_mantencion = int(costo_de_mantencion)
        self.velocidad_base = int(velocidad_base)
        self.pasajeros = int(pasajeros)                               # con los objetos pasajeros
        self.carga_maxima = int(carga_maxima)
        self.moneda_de_origen = moneda_de_origen
        self.tipo = tipo
        self.nombres_tripulacion = tripulacion     # Son los nombres, pero va a haber una lista
        self.tripulacion = []                      # Con los objetos tripulación
        self.codigos_carga = carga
        self.carga = []                            # idem, pero con la carga
        self.encallado = False      # indica si está encallado o no
        self.avance = 0                  # indica cuanto ha avanzado el barco
        self.canal = None
        self.ocurrencia_evento = False
        self.horas_en_canal = 0
        self.dias_averia = 0

    def desplazarse(self):  # Falta bloquear el paso cuando encalla algo delante
        if not self.encallado: 
            minimo = min(1, (self.carga_maxima - self.peso_mercancia-(0.3*self.pasajeros))/self.carga_maxima)
            maximo = max(0.1, minimo)
            desplazmiento = maximo * self.velocidad_base
            self.avance += desplazmiento
            print(f"{self.nombre} ha avanzado hasta el Km {self.avance}")
        else:
            print(f"{self.nombre} no ha podido avanzar por que está encallado")

    def usar_especialidades(self):
        for i in self.tripulacion:
            i.especialidad()

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
        if ecuacion < 0:
            ecuacion = 0
        minimo = min(1, ecuacion)
        return minimo

    @abstractmethod
    def ejecutar_evento_especial(self):
        pass


class Barco_de_pasajeros(Barcos):

    def ejecutar_evento_especial(self):
        azar = randint(1, 100)
        if azar < PROBABILIDAD_EVENTO_ESPECIAL and not self.ocurrencia_evento:
            print(f"El barco {self.nombre} se ha intoxicado, debe pagar {DINERO_INTOXICACION} "
                  f"al canal {self.canal.nombre}")
            self.canal.dinero += DINERO_INTOXICACION
            self.ocurrencia_evento = True

    @property
    def prob_encallar(self):
        return super().encallar() * TENDENCIA_ENCALLAR_PASAJEROS * self.canal.ponderador

    def encallar(self):
        azar = randint(1, 100)
        if self.prob_encallar > azar:
            print(f"El barco {self.nombre} ha encallado")
            self.encallado = True
            self.canal.barcos_que_encallaron += 1
            return True
        return False


class Barco_carguero(Barcos):

    def ejecutar_evento_especial(self):        # Recordar que barco atacado no paga tarifa
        azar = randint(1, 100)
        if azar < PROBABILIDAD_EVENTO_ESPECIAL and not self.ocurrencia_evento:
            print(f"¡¡El barco {self.nombre} ha sido atacado por piratas!! han perdido toda su mercancía"
                  f" y no podrán pagar la tarifa al {self.canal.nombre}")
            self.carga = []
            self.ocurrencia_evento = True

    @property
    def prob_encallar(self):
        return super().encallar() * TENDENCIA_ENCALLAR_CARGUERO * self.canal.ponderador

    def encallar(self):
        azar = randint(1, 100)
        if self.prob_encallar > azar:
            print(f"El barco {self.nombre} ha encallado")
            self.encallado = True


class Buque(Barcos):

    def ejecutar_evento_especial(self):       # Recordar que este barco no avanza algunas horas
        azar = randint(1, 100)
        if azar < PROBABILIDAD_EVENTO_ESPECIAL and not self.ocurrencia_evento:
            print(f"El barco {self.nombre} ha sufrido una avería, no podrá avanzar durante {TIEMPO_AVERIA_BUQUE} horas")
            self.ocurrencia_evento = True
            self.dias_averia = TIEMPO_AVERIA_BUQUE

    @property
    def prob_encallar(self):
        return super().encallar() * TENDENCIA_ENCALLAR_BUQUE * self.canal.ponderador

    def encallar(self):
        azar = randint(1, 100)
        if self.prob_encallar > azar:
            print(f"El barco {self.nombre} ha encallado")
            self.encallado = True


class Mercancia:  # Completada

    def __init__(self, lote, tipo, tiempo_expiracion, peso):
        self.lote = lote
        self.tipo = tipo
        self.tiempo_expiracion = int(tiempo_expiracion)
        self.peso = int(peso)
        self.barco = None

    def expirar(self):            # solamente devuelve el monto que se debe cobrar
        if self.tiempo_expiracion == 0:    
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
            self.barco.canal.dinero_gastado += multa
            print(f"Se ha cobrado {multa} al {self.barco.canal.nombre} por la expiración de {self.tipo} "
                  f"en el {self.barco.nombre}")
        else:
            self.tiempo_expiracion -= 1


class Tripulacion(ABC):
    def __init__(self, nombre, tipo, experiencia):
        self.nombre = nombre
        self.experiencia = int(experiencia)
        self.barco = None
        self.uso_habilidad = False
        self.tipo = tipo

    @abstractmethod
    def especialidad(self):
        pass


class DCCapitan(Tripulacion):

    def especialidad(self):
        if self.barco.encallado and not self.uso_habilidad:
            self.barco.encallado = False
            self.uso_habilidad = True
            print(f"El capitán {self.nombre} del {self.barco.nombre} ha desencallado el barco")


class DCCocinero(Tripulacion):

    def especialidad(self):
        if not self.uso_habilidad:
            objetos = self.barco.carga
            for i in objetos:
                i.tiempo_expiracion = i.tiempo_expiracion * 2
            print(f"El cocinero {self.nombre} del {self.barco.nombre} ha hecho que los alimentos del barco"
                  f" duren más")
            self.uso_habilidad = True


class DCCarguero(Tripulacion):

    def especialidad(self):
        if not self.uso_habilidad:
            self.barco.carga_maxima += CARGA_EXTRA_CARGUERO
            print(f"El carguero {self.nombre} del {self.barco.nombre} ha aumentado la carga máxima el barco")
            self.uso_habilidad = True


class Canal:

    def __init__(self, nombre, largo, dificultad):
        self.nombre = nombre
        self.dinero = DINERO_INICIAL
        self.largo = int(largo)
        self.dificultad = dificultad
        self.barcos = []
        self.horas_simuladas = 0
        self.dinero_gastado = 0
        self.dinero_recibido = 0
        self.barcos_que_pasaron = 0
        self.barcos_que_encallaron = 0
        self.eventos_especiales_ocurridos = 0
        self.intento_desencallar = False

    @property
    def cobro_de_uso(self):
        if self.dificultad == "avanzado":
            return COBRO_USO_AVANZADO
        else:
            return COBRO_USO_PRINCIPIANTE

    @property
    def hay_encallado(self):
        for i in self.barcos:
            if i.encallado:
                return True
        return False

    @property
    def probablidad_de_desencallar(self):
        if self.dificultad == "avanzado":
            return PROB_BASE_DESENCALLAR * PONDERADOR_AVANZADO
        else:
            return PROB_BASE_DESENCALLAR * PONDERADOR_PRINCIPIANTE

    def barco_en_el_canal(self, barco):
        for i in self.barcos:
            if i.nombre == barco.nombre:
                return True
        return False

    @property
    def ponderador(self):
        if self.dificultad == "avanzado":
            return PONDERADOR_AVANZADO
        return PONDERADOR_PRINCIPIANTE

    def ingresar_barco(self, barco):    # esto solo se debe usar para un barco que no esté en el canal
        self.barcos.append(barco)

    def avanzar_barcos(self):
        self.intento_desencallar = False
        if self.hay_encallado:
            for i in self.barcos:
                if i.encallado:
                    bloqueo = i.avance
        else:
            bloqueo = -1

        barcos_que_avanzan = []
        for i in self.barcos:
            if i.avance > bloqueo:
                if i.dias_averia == 0:
                    barcos_que_avanzan.append(i)
                else:
                    i.dias_averia -= 1
                    print(f"{i.nombre} sigue averiado, le faltan {i.dias_averia}" 
                    f" horas para volver a avanzar")
            else:
                if i.dias_averia != 0:
                    i.dias_averia -= 1

        for i in barcos_que_avanzan:
            if not i.encallar():
                i.ejecutar_evento_especial()
                i.desplazarse()

    def desencallar_barco(self, barco):
        self.dinero -= COSTO_DESENCALLAR
        self.dinero_gastado += COSTO_DESENCALLAR
        self.intento_desencallar = True
        azar = randint(1, 100)
        if self.probablidad_de_desencallar >= azar:
            barco.encallado = False
            print(f"El barco {barco.nombre} ha sido desencallado con éxito :D")
            print("Presiona enter para continuar")
            input()
        else:
            print(f"No se ha podido desencallar el barco {barco.nombre} :( ")
            print("Presiona enter para continuar")
            input()

    def pagar_mantenimiento(self):
        for i in self.barcos:
            c = CurrencyConverter()
            costo = c.convert(100, i.moneda_de_origen, 'USD')
            self.dinero -= costo
            self.dinero_gastado += costo
            print(f"El canal {self.nombre} ha debido pagar {costo} al {i.nombre}")
