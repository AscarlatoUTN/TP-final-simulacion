"""
Generadores de variables aleatorias del modelo, por método de la inversa.

Todas las funciones reciben el `rng` explícitamente (en vez de usar un
generador global) para que la simulación sea reproducible y fácil de testear.
"""

import math
from statistics import NormalDist

def generar_ia_1(rng):
    R = rng.random()
    return 0.5 - 1.5546 * math.log(R)

def generar_ia_2(rng):
    """
    Genera un intervalo entre arribos IA_2 mediante aceptación-rechazo.
    """
    M = 1.1956

    while True:
        R1 = rng.random()
        R2 = rng.random()

        X = 0.4145 + 3482.5855 * R1
        Y = M * R2

        f_x = (
                1
                / (1.9486 * (X - 0.4145))
                * math.exp(
            -((math.log(X - 0.4145) + 0.5436) ** 2)
            / 1.2087
        )
        )

        if Y <= f_x:
            return X

def generar_ia_3(rng):
    R = rng.random()
    return -8.6538 + 9.1538 * R ** (-1 / 15.2479)

def generar_ia_4(rng):
    R = rng.random()
    return 0.5 - 0.7335 * math.log(R)


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
