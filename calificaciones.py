"""
Sistema de calificaciones: ventana móvil de reputación por tipo de taxi,
elección del pasajero (siempre el mejor calificado) y aceptación del
servicio según la calificación promedio.
"""

from collections import deque

from config import (
    AJUSTE_SATISFACCION_TIPO,
    FILTRO_APERTURA_AUTONOMO,
    REPUTACION_INICIAL,
    TABLA_ACEPTACION_AUTONOMO,
    TABLA_ACEPTACION_CON_ELEC,
    TIPOS_TAXI,
    VENTANA_CALIFICACIONES,
)


class SistemaCalificaciones:
    def __init__(self, rng):
        self.rng = rng
        self._historial = {
            tipo: deque(
                [REPUTACION_INICIAL[tipo]] * VENTANA_CALIFICACIONES,
                maxlen=VENTANA_CALIFICACIONES,
            )
            for tipo in TIPOS_TAXI
        }

    def promedio(self, tipo):
        valores = self._historial[tipo]
        return sum(valores) / len(valores)

    def mejor_tipo(self):
        """El pasajero siempre intenta primero el servicio mejor calificado."""
        tipos_disponibles = [tipo for tipo in TIPOS_TAXI if tipo != "autonomo"]
        promedios = {tipo: self.promedio(tipo) for tipo in tipos_disponibles}
        
        ranked = sorted(promedios.items(), key=lambda x: x[1], reverse=True)
        tipos_ordenados = [t for t, _ in ranked]
        promedios_ordenados = [p for _, p in ranked]
        return tipos_ordenados, promedios_ordenados

    def _probabilidad_aceptacion(self, tipo, promedio):
        tabla = TABLA_ACEPTACION_AUTONOMO if tipo == "autonomo" else TABLA_ACEPTACION_CON_ELEC
        for umbral, prob in tabla:
            if promedio >= umbral:
                return prob
        return tabla[-1][1]

    def pasajero_acepta(self, tipo, promedio):
        # Si el mejor calificado es autónomo, primero se filtra por apertura a la tecnología.
        if tipo == "autonomo" and self.rng.random() > FILTRO_APERTURA_AUTONOMO:
            return False
        prob = self._probabilidad_aceptacion(tipo, promedio)
        return self.rng.random() < prob

    def _penalizacion_espera(self, espera):
        minutos = espera / 60
        if minutos <= 5:
            return 0.0
        if minutos <= 10:
            return 0.5
        if minutos <= 15:
            return 1.5
        return 1.5

    def registrar_viaje(self, tipo, espera):
        """Calcula la calificación del viaje y la agrega a la ventana móvil."""
        penalizacion = self._penalizacion_espera(espera)
        ajuste = AJUSTE_SATISFACCION_TIPO[tipo]
        # TODO: el enunciado no especifica la distribución del componente
        error = self.rng.gauss(0, 0.2)
        calificacion = max(1.0, min(5.0, 5 - penalizacion + ajuste + error))
        self._historial[tipo].append(calificacion)
        return calificacion
