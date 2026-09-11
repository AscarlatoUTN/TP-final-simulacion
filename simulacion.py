"""
Simulación evento a evento de la flota de taxis para una franja horaria.
"""

import random

import generadores
from calificaciones import SistemaCalificaciones
from flota import Flota
from capacidad import Capacidad
import config

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
        self.capacidad = Capacidad(cantidad_convencionales, cantidad_electricos, cantidad_autonomos)
        
        # --- Variables de tiempo de la simulación ---
        self.T = 0.0
        self.TPLL = 0.0

        # --- Acumuladores internos para calcular métricas al finalizar ---
        self._suma_esperas = 0.0
        self._cantidad_viajes_completados = 0
        self._cantidad_solicitudes = 0
        self._cantidad_arrepentidos = 0
        self._ingresos = 0.0
        self._costos_variables = config.COSTO_FSD_ANUAL * self.flota.cantidades_autonomos * config.TF / (3600 * 24 * 365)
        self._costos_fijos = config.COSTO_ADQUISICION["convencional"] * self.flota.cantidades_convencionales + config.COSTO_ADQUISICION["electrico"] * (self.flota.cantidades_electricos + self.flota.cantidades_autonomos)
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
        tipo = "autonomo"

        if not self.calificaciones.pasajero_acepta(tipo, self.calificaciones.promedio("autonomo")):
            tipos, promedios = self.calificaciones.mejor_tipo()
            if self.calificaciones.pasajero_acepta(tipos[0], promedios[0]):
                tipo = tipos[0]
            elif self.calificaciones.pasajero_acepta(tipos[1], promedios[1]):
                tipo = tipos[1]
            else:
                # El pasajero abandona: por su misma naturaleza, no prueba otro servicio.
                self._cantidad_arrepentidos += 1
                return

        esta_disponible_ahora, indice_taxi, tiempo_espera = self.flota.taxi_disponible(tipo, self.T)

        if tiempo_espera > 900:
            self._cantidad_arrepentidos += 1
            return

        self._suma_esperas += tiempo_espera

        dis = generadores.generar_distancia(self.rng)
        tv = generadores.tiempo_viaje(dis)

        if esta_disponible_ahora:
            # Si esta disponible ahora, significa que hasta entonces el taxi estaba ocioso
            self.flota.tiempo_ocioso[tipo][indice_taxi] += self.T - self.flota.tiempo_comprometido[tipo][indice_taxi]

            self.flota.tiempo_comprometido[tipo][indice_taxi] = self.T + tv
        else:
            # Si no esta disponible ahora, significa que el taxi estaba ocupado y el viaje empieza cuando se libera
            self.flota.tiempo_comprometido[tipo][indice_taxi] = self.T + tv

        # --- Consumo de energía y reabastecer ---
        # Apenas se sabe la distancia y el tiempo del viaje, se descuenta el
        # consumo del vehículo y, si cae por debajo del umbral, se reabastecer.
        self.capacidad.consumir(tipo, indice_taxi, dis)
        if self.capacidad.necesita_reabastecimiento(tipo, indice_taxi):
            tiempo_reabastecimiento, costo_reabastecimiento = self.capacidad.reabastecer(tipo, indice_taxi)
            # El tiempo de reabastecer se suma al tiempo comprometido del vehículo,
            # tal como indica el enunciado.
            self.flota.tiempo_comprometido[tipo][indice_taxi] += tiempo_reabastecimiento
            self._costos_variables += costo_reabastecimiento
        self._cantidad_viajes_completados += 1
        pago = self.tarifa_base + 2.75 * dis
        self._ingresos += pago
        self.calificaciones.registrar_viaje(tipo, tiempo_espera)

    # ------------------------------------------------------------------
    # Loop principal de la simulación
    # ------------------------------------------------------------------
    def correr(self):
        while self.T < config.TF:
            self.T = self.TPLL
            intervalo_arribo = generadores.generar_intervalo_arribo(self.rng, self.franja)
            self.TPLL = self.T + intervalo_arribo
            self.procesar_solicitud()

        self._calcular_metricas_finales()
        return self

    def _calcular_metricas_finales(self):
        if self._cantidad_viajes_completados:
            self.TPE = self._suma_esperas / self._cantidad_viajes_completados

        self.flota.finalizar(self.T)
        self.TPOC = self.flota.porcentaje_tiempo_ocioso("convencional", self.T) / self.flota.cantidades_convencionales
        self.TPOE = self.flota.porcentaje_tiempo_ocioso("electrico", self.T) / self.flota.cantidades_electricos
        self.TPOA = self.flota.porcentaje_tiempo_ocioso("autonomo", self.T) / self.flota.cantidades_autonomos

        if self._cantidad_solicitudes:
            self.PARR = 100 * self._cantidad_arrepentidos / self._cantidad_solicitudes



        self.BN =self._ingresos - self._costos_fijos - self._costos_variables

    def __repr__(self):
        return (
            f"Simulacion(T={self.T:.1f}, TPE={self.TPE:.1f}, "
            f"TPOC={self.TPOC:.1f}, TPOE={self.TPOE:.1f}, TPOA={self.TPOA:.1f}, "
            f"PARR={self.PARR:.2f}%, BN={self.BN:.2f}, "
            f"calif_conv={self.calificaciones.promedio('convencional'):.2f}, "
            f"calif_elec={self.calificaciones.promedio('electrico'):.2f}, "
            f"calif_auto={self.calificaciones.promedio('autonomo'):.2f})"
        )
