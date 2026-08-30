"""
Estado de la flota de taxis: tiempos comprometidos, tiempo ocioso
acumulado por taxi y disponibilidad.
"""

from Simulacion.config import TIPOS_TAXI


class Flota:
    """
    Mantiene, para cada tipo de taxi, dos arrays de longitud igual a la
    cantidad de taxis de ese tipo (uno por taxi):
    - tiempo_comprometido[i]: momento en el que el taxi i queda libre.
    - tiempo_ocioso[i]: tiempo ocioso acumulado del taxi i.

    El tiempo ocioso se suma en el momento en que se detecta: cuando un
    taxi recibe un nuevo viaje, la brecha entre que quedó libre y el
    momento de la asignación es tiempo que estuvo ocioso. """

    def __init__(self, cantidad_convencionales, cantidad_electricos, cantidad_autonomos):
        cantidades = {
            "convencional": cantidad_convencionales,
            "electrico": cantidad_electricos,
            "autonomo": cantidad_autonomos,
        }
        self.cantidades = cantidades
        self.tiempo_comprometido = {tipo: [0.0] * cantidades[tipo] for tipo in TIPOS_TAXI}
        self.tiempo_ocioso = {tipo: [0.0] * cantidades[tipo] for tipo in TIPOS_TAXI}

    def taxi_disponible(self, tipo, T):
        """
        Revisa el array de tiempos comprometidos del tipo pedido.

        Devuelve (disponible_ahora, indice_taxi, espera):
        - disponible_ahora: True si T >= tiempo_comprometido[i] para ese taxi.
        - indice_taxi: índice del taxi que se libera primero (el de menor
          tiempo_comprometido), sea que esté libre ahora o no.
        - espera: 0 si está disponible ahora, o el tiempo que falta para
          que se libere ese taxi.
        """
        array = self.tiempo_comprometido[tipo]
        idx_min = min(range(len(array)), key=lambda i: array[i])
        tiempo_libre = array[idx_min]
        if T >= tiempo_libre:
            return True, idx_min, 0.0
        return False, idx_min, tiempo_libre - T



    def finalizar(self, HV):
        """
        Suma el tiempo ocioso final de cada taxi: desde que terminó su
        último viaje hasta el horizonte HV. Se llama una sola vez, al
        terminar la simulación.
        """
        for tipo in TIPOS_TAXI:
            for i, tiempo_libre in enumerate(self.tiempo_comprometido[tipo]):
                self.tiempo_ocioso[tipo][i] += max(0.0, HV - tiempo_libre)

    def tiempo_ocioso_promedio(self, tipo,tiempo_final):
        """
        Porcentaje promedio de tiempo ocioso de los taxis de `tipo`,
        respecto del tiempo final (llamar después de `finalizar`).
        """
        array = self.tiempo_ocioso[tipo]
        return 100 * sum(array)/tiempo_final