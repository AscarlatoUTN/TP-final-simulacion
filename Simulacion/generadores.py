"""
Generadores de variables aleatorias del modelo, por método de la inversa.

Todas las funciones reciben el `rng` explícitamente (en vez de usar un
generador global) para que la simulación sea reproducible y fácil de testear.
"""

import math
from statistics import NormalDist


def generar_intervalo_arribo(rng, lambda_arribo):
    """IA = -ln(R) / lambda"""
    R = rng.random()
    return -math.log(R) / lambda_arribo


def generar_distancia(rng):
    """DIS = e^(0.74275 + 0.84577 * Phi^-1(P)), P = 0.0448 + 0.9544*R"""
    R = rng.random()
    P = 0.0448 + 0.9544 * R
    z = NormalDist().inv_cdf(P)
    return math.exp(0.74275 + 0.84577 * z)


def tiempo_viaje(dis):
    """TV = f(DIS) = 480 + 144 * DIS"""
    return 480 + 144 * dis
