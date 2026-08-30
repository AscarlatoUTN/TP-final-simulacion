"""
Simulación evento a evento de la flota de taxis para una franja horaria.
"""

import random

from Simulacion import generadores
from Simulacion.calificaciones import SistemaCalificaciones
from Simulacion.flota import Flota
from Simulacion.energia import Energia


"""Variable global de High Value (en segundos) para determinar cuando termina la simulacion"""
HV = 9999


class Simulacion:
    """
    Parámetros
    ----------
    cantidad_convencionales, cantidad_electricos, cantidad_autonomos : int
        Cantidad de taxis de cada tipo.
    tarifa_base : float
        Franja horaria de la simulación, que determina la FDP del intervalo de arribo entre solicitudes y la tarifa base
        Tarifa base (B) del sistema de pago, según la franja horaria.
    seed : int | None
        Semilla del generador aleatorio, para reproducibilidad.
    """

    def __init__(
            self,
            cantidad_convencionales,
            cantidad_electricos,
            cantidad_autonomos,
            franja,
            tarifa_base=0.0,
            seed=None,
    ):
        self.franja = franja
        self.tarifa_base = tarifa_base
        self.rng = random.Random(seed)
        self.flota = Flota(cantidad_convencionales, cantidad_electricos, cantidad_autonomos)
        self.calificaciones = SistemaCalificaciones(self.rng)
        self.energia = Energia(cantidad_convencionales, cantidad_electricos, cantidad_autonomos)

        # --- Variables de tiempo de la simulación ---
        self.T = 0.0
        self.TPLL = 0.0

        # --- Acumuladores internos para calcular métricas al finalizar ---
        self._suma_esperas = 0.0
        self._cantidad_viajes_completados = 0
        self._cantidad_solicitudes = 0
        self._cantidad_arrepentidos = 0
        self._ingresos = 0.0
        self._costos = 0.0
        # --- Métricas finales (se completan al terminar correr()) ---
        self.TPE = 0.0
        self.TPOC = 0.0
        self.TPOE = 0.0
        self.TPOA = 0.0
        self.PARR = 0.0
        self.BN = 0.0

    # ------------------------------------------------------------------
    # Procesamiento de una solicitud de viaje
    # ------------------------------------------------------------------
    def procesar_solicitud(self):
        self._cantidad_solicitudes += 1

        tipo, promedio = self.calificaciones.mejor_tipo()
        if not self.calificaciones.pasajero_acepta(tipo, promedio):
            # El pasajero abandona: por su misma naturaleza, no prueba otro servicio.
            self._cantidad_arrepentidos += 1
            return

        esta_disponible_ahora, indice_taxi, tiempo_espera = self.flota.taxi_disponible(tipo, self.T)

        self._suma_esperas += tiempo_espera

        dis = generadores.generar_distancia(self.rng)
        tv = generadores.tiempo_viaje(dis)

        if esta_disponible_ahora:
            # Si esta disponible ahora, significa que hasta entonces el taxi estaba ocioso
            self.flota.tiempo_ocioso[tipo][indice_taxi] += self.T - self.flota.tiempo_comprometido[tipo][indice_taxi]

            inicio_viaje = self.T  # El viaje empieza en ese momento, porque el taxi estaba libre
            self.flota.tiempo_comprometido[tipo][indice_taxi] = inicio_viaje + tv
        else:
            # Si no esta disponible ahora, significa que el taxi estaba ocupado y el viaje empieza cuando se libera
            inicio_viaje = self.flota.tiempo_comprometido[tipo][indice_taxi]
            # El viaje tiene su tiempo comprometido hasta que termine ese viaje
            self.flota.tiempo_comprometido[tipo][indice_taxi] = inicio_viaje + tv

        # --- Consumo de energía y recarga ---
        # Apenas se sabe la distancia y el tiempo del viaje, se descuenta el
        # consumo del vehículo y, si cae por debajo del umbral, se recarga.
        self.energia.consumir(tipo, indice_taxi, dis)
        if self.energia.necesita_recarga(tipo, indice_taxi):
            tiempo_recarga, costo_recarga = self.energia.recargar(tipo, indice_taxi)
            # El tiempo de recarga se suma al tiempo comprometido del vehículo,
            # tal como indica el enunciado.
            self.flota.tiempo_comprometido[tipo][indice_taxi] += tiempo_recarga
            self._costos += costo_recarga
        self._cantidad_viajes_completados += 1
        pago = self.tarifa_base + 2.75 * dis
        self._ingresos += pago
        self.calificaciones.registrar_viaje(tipo, tiempo_espera)

    # ------------------------------------------------------------------
    # Loop principal de la simulación
    # ------------------------------------------------------------------
    def correr(self):
        while self.T < HV:
            self.T = self.TPLL
            intervalo_arribo = generadores.generar_intervalo_arribo(self.rng, self.franja)
            self.TPLL = self.T + intervalo_arribo
            self.procesar_solicitud()

        self._calcular_metricas_finales()
        return self

    def _calcular_metricas_finales(self):
        if self._cantidad_viajes_completados:
            self.TPE = self._suma_esperas / self._cantidad_viajes_completados

        self.TPOC = self.flota.porcentaje_tiempo_ocioso("convencional", self.T)
        self.TPOE = self.flota.porcentaje_tiempo_ocioso("electrico", self.T)
        self.TPOA = self.flota.porcentaje_tiempo_ocioso("autonomo", self.T)

        if self._cantidad_solicitudes:
            self.PARR = 100 * self._cantidad_arrepentidos / self._cantidad_solicitudes

        self.BN = self._ingresos - self._costos

    def __repr__(self):
        return (
            f"Simulacion(T={self.T:.1f}, TPE={self.TPE:.1f}, "
            f"TPOC={self.TPOC:.1f}, TPOE={self.TPOE:.1f}, TPOA={self.TPOA:.1f}, "
            f"PARR={self.PARR:.2f}%, BN={self.BN:.2f}, "
            f"calif_conv={self.calificaciones.promedio('convencional'):.2f}, "
            f"calif_elec={self.calificaciones.promedio('electrico'):.2f}, "
            f"calif_auto={self.calificaciones.promedio('autonomo'):.2f})"
        )
