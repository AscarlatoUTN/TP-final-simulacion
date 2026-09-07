"""
Constantes y parámetros del modelo de simulación de la flota de taxis.
"""

"""Variable global de High Value (en segundos) para determinar cuando termina la simulacion"""
TF = 3600 * 24 * 365 * 5 # 5 años

# --- Parámetros de la flota, la franja y el horizonte de prueba ---
CANTIDAD_CONVENCIONALES = [8, 8, 8, 10, 10, 10, 12, 12, 12, 14, 14, 14]
CANTIDAD_ELECTRICOS =     [18, 18, 18, 20, 20, 20, 22, 22, 22, 24, 24, 24]
CANTIDAD_AUTONOMOS =      [3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5]
FRANJA = "noche"  # una de: "madrugada", "manana", "tarde", "noche"
SEED = None

TIPOS_TAXI = ("convencional", "electrico", "autonomo")

TIPOS_FRANJAS=("madrugada", "manana", "tarde", "noche")

# --- Tarifa base según franja horaria (sistema de pago: Pago = B + 2.75*DIS) ---
TARIFA_BASE_FRANJA = {
    "madrugada": 4.0,
    "manana": 3.0,
    "tarde": 5.5,
    "noche": 4.0,
}

# --- Sistema de calificaciones ---
VENTANA_CALIFICACIONES = 100  # cantidad de valoraciones consideradas (ventana móvil)

# Reputación inicial (periodo de prueba / lanzamiento)
REPUTACION_INICIAL = {
    "convencional": 4.5,
    "electrico": 4.5,
    "autonomo": 4.0,
}

# Ajuste de satisfacción según tipo de vehículo (puntuación del viaje)
AJUSTE_SATISFACCION_TIPO = {
    "convencional": 0.0,
    "electrico": 0.2,
    "autonomo": -0.1,
}

# Filtro de apertura de pasajeros a viajar en autónomo
FILTRO_APERTURA_AUTONOMO = 0.29

# Probabilidad de aceptación según calificación promedio del servicio
# (tramo_minimo, probabilidad), evaluados de mayor a menor
TABLA_ACEPTACION_CON_ELEC = (
    (5.0, 1.00),
    (4.8, 0.95),
    (4.5, 0.85),
    (4.0, 0.70),
    (0.0, 0.50),
)
TABLA_ACEPTACION_AUTONOMO = (
    (5.0, 1.00),
    (4.8, 0.90),
    (4.5, 0.75),
    (4.0, 0.50),
    (0.0, 0.20),
)
# --- Parámetros energéticos de vehículos ---
# El autónomo comparte vehículo con el eléctrico (Model 3), por eso tiene
# los mismos parámetros de capacidad/consumo/reabastecer; lo único distinto es
# el costo de FSD (ver COSTO_FSD_ANUAL más abajo).
CAPACIDAD_TANQUE = {
    "convencional": 50.0,  # litros
    "electrico": 75.0,     # kWh
    "autonomo": 75.0,      # kWh
}

CONSUMO_POR_MILLA = {
    "convencional": 0.11,  # L/mi
    "electrico": 0.26,     # kWh/mi
    "autonomo": 0.26,      # kWh/mi
}

# Umbral de nivel restante a partir del cual el vehículo debe reabastecer/reabastecer
UMBRAL_REABASTECIMIENTO = {
    "convencional": 7.5,   # 15% de 50 L
    "electrico": 15.0,     # 20% de 75 kWh
    "autonomo": 15.0,      # 20% de 75 kWh
}

TIEMPO_REABASTECIMIENTO = {
    "convencional": 300,   # s (5 min)
    "electrico": 1800,     # s (30 min)
    "autonomo": 1800,      # s (30 min)
}

# Nivel al que queda el vehículo después de reabastecer/reabastecer.
# Convencional llena el tanque completo; eléctrico/autónomo cargan
# rápido y parcial, del 20% al 80% (0.8 * 75 kWh = 60 kWh).
NIVEL_TRAS_REABASTECIMIENTO = {
    "convencional": 50.0,
    "electrico": 60.0,
    "autonomo": 60.0,
}

PRECIO_POR_UNIDAD_CAPACIDAD = {
    "convencional": 0.92,  # USD/L
    "electrico": 0.38,     # USD/kWh
    "autonomo": 0.38,      # USD/kWh
}

# --- Costos de vehículos (no incorporados aún al cálculo de BN) ---
COSTO_ADQUISICION = {
    "convencional": 23125,
    "electrico": 47000,
    "autonomo": 47000,
}
COSTO_FSD_ANUAL = 1_200