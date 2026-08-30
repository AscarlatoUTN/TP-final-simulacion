"""
Consumo de combustible/batería y recarga de la flota.

Mantiene, para cada tipo de taxi, un array con el nivel de combustible o
batería de cada vehículo (equivalente a CVC, CVE y CVA del enunciado).
"""

from .config import (
    CAPACIDAD_TANQUE,
    CONSUMO_POR_MILLA,
    NIVEL_TRAS_RECARGA,
    PRECIO_POR_UNIDAD_ENERGIA,
    TIEMPO_RECARGA,
    TIPOS_TAXI,
    UMBRAL_RECARGA,
)


class Energia:
    """
    nivel[tipo][i] = combustible (L) o batería (kWh) restante del taxi i
    de ese tipo. Arranca con el tanque/batería llenos.
    """

    def __init__(self, cantidad_convencionales, cantidad_electricos, cantidad_autonomos):
        cantidades = {
            "convencional": cantidad_convencionales,
            "electrico": cantidad_electricos,
            "autonomo": cantidad_autonomos,
        }
        self.cantidades = cantidades
        self.nivel = {
            tipo: [CAPACIDAD_TANQUE[tipo]] * cantidades[tipo] for tipo in TIPOS_TAXI
        }

    def consumir(self, tipo, idx, dis):
        """Descuenta el consumo de un viaje de distancia `dis` (millas) al taxi `idx`."""
        self.nivel[tipo][idx] -= CONSUMO_POR_MILLA[tipo] * dis

    def necesita_recarga(self, tipo, idx):
        return self.nivel[tipo][idx] <= UMBRAL_RECARGA[tipo]

    def recargar(self, tipo, idx):
        """
        Recarga/reabastece el taxi `idx` de `tipo` hasta su nivel post-recarga.

        Devuelve (tiempo_recarga, costo) para que la simulación sume el
        tiempo al tiempo comprometido del vehículo y el costo al beneficio neto.
        """
        nivel_actual = self.nivel[tipo][idx]
        nivel_final = NIVEL_TRAS_RECARGA[tipo]
        costo = (nivel_final - nivel_actual) * PRECIO_POR_UNIDAD_ENERGIA[tipo]
        self.nivel[tipo][idx] = nivel_final
        return TIEMPO_RECARGA[tipo], costo