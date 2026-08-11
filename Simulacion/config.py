"""
Constantes y parámetros del modelo de simulación de la flota de taxis.
"""

TIPOS_TAXI = ("convencional", "electrico", "autonomo")

# --- Cantidad de taxis por tipo (ajustables según el escenario a simular) ---
CANTIDAD_CONVENCIONALES = 10
CANTIDAD_ELECTRICOS = 10
CANTIDAD_AUTONOMOS = 10

# --- Parámetros lambda de la FDP Exponencial de intervalo entre arribos ---
# IA = -ln(R) / lambda,  R ~ U(0,1)
LAMBDAS_FRANJA = {
    "madrugada": 0.1458,
    "manana": 0.3093,
    "tarde": 0.3403,
    "noche": 0.3709,
}

# --- Tarifa base según franja horaria (sistema de pago: Pago = B + 2.75*DIS) ---
TARIFA_BASE_FRANJA = {
    "madrugada": 3.5,
    "manana": 4.8,
    "tarde": 5.1,
    "noche": 4.3,
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
