"""
Corre una simulación independiente por cada franja horaria y muestra
las métricas finales de cada una.

Uso: python -m taxis_simulacion.main
"""

from Simulacion.config import (
    CANTIDAD_AUTONOMOS,
    CANTIDAD_CONVENCIONALES,
    CANTIDAD_ELECTRICOS,
    LAMBDAS_FRANJA,
    TARIFA_BASE_FRANJA,
)
from simulacion import Simulacion


def correr_las_cuatro_franjas(seed=None):
    """Corre una simulación independiente por cada franja horaria."""
    resultados = {}
    for franja, lam in LAMBDAS_FRANJA.items():
        sim = Simulacion(
            cantidad_convencionales=CANTIDAD_CONVENCIONALES,
            cantidad_electricos=CANTIDAD_ELECTRICOS,
            cantidad_autonomos=CANTIDAD_AUTONOMOS,
            lambda_arribo=lam,
            tarifa_base=TARIFA_BASE_FRANJA[franja],
            seed=seed,
        )
        sim.correr()
        resultados[franja] = sim
    return resultados


if __name__ == "__main__":
    resultados = correr_las_cuatro_franjas(seed=42)
    for franja, sim in resultados.items():
        print(f"{franja:>10}: {sim}")
