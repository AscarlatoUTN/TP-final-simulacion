"""
Generadores de variables aleatorias del modelo, por método de la inversa.

Todas las funciones reciben el `rng` explícitamente (en vez de usar un
generador global) para que la simulación sea reproducible y fácil de testear.
"""

import math
from statistics import NormalDist

def generar_ia_1(rng):
    R = rng.random()
    return 0.5 - 1.5546 * math.log(1-R)

def generar_ia_2(rng):

    MU = -0.5436
    SIGMA = 0.7773995111909964
    OFFSET = 0.4145

    R = rng.random()
    z = NormalDist().inv_cdf(R)
    return OFFSET + math.exp(MU + SIGMA * z)

def generar_ia_3(rng):
    R = rng.random()
    return -8.6539 + 9.1539 * (1-R) ** (-1 / 15.2479)

def generar_ia_4(rng):
    R = rng.random()
    return 0.5 - 0.7335 * math.log(1-R)


def generar_intervalo_arribo(rng, franja):
    if franja == "madrugada":
        return generar_ia_1(rng)

    elif franja == "manana":
        return generar_ia_2(rng)

    elif franja == "tarde":
        return generar_ia_3(rng)

    elif franja == "noche":
        return generar_ia_4(rng)

    else:
        raise ValueError(f"Franja desconocida: {franja}")


def generar_distancia(rng):
    """
    DIS ~ Lognormal, ajustada con scipy.stats.lognorm.fit(...).
    Parámetros (s, loc, scale) = (0.9293763600194365, 0, 1.8580729103281197).

    Generada por el método de la inversa: DIS = loc + scale * e^(s * Phi^-1(R)),
    con R ~ U(0,1) y Phi la CDF de la normal estándar.
    """
    S = 0.9293763600194365
    LOC = 0.0
    SCALE = 1.8580729103281197

    R = rng.random()
    z = NormalDist().inv_cdf(R)
    return LOC + SCALE * math.exp(S * z)


def tiempo_viaje(dis):
    """TV = f(DIS) = 480 + 144 * DIS"""
    return 480 + 144 * dis
