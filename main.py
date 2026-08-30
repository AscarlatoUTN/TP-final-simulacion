"""
Prueba rápida y manual de la simulación para una sola franja horaria,
con parámetros chicos hardcodeados para revisar el comportamiento a
simple vista.

Ejecutalo directo con el botón Run del IDE, o con: python probar.py
"""

import os
from config import TARIFA_BASE_FRANJA
from simulacion import Simulacion

# --- Parámetros de la flota, la franja y el horizonte de prueba ---
# CANTIDAD_CONVENCIONALES = 10
# CANTIDAD_ELECTRICOS = 20
# CANTIDAD_AUTONOMOS = 5
CANTIDAD_CONVENCIONALES =   [8,  8,  8,  10, 10, 10, 12, 12, 12]
CANTIDAD_ELECTRICOS =       [18, 18, 18, 20, 20, 20, 22, 22, 22]
CANTIDAD_AUTONOMOS =        [3,  4,  5,  3,  4,  5,  3,  4,  5]
FRANJA = "madrugada"  # una de: "madrugada", "manana", "tarde", "noche"
SEED = None


def imprimir_resultado(i, franja, sim, archivo=None):
    ancho = 70

    def escribir(texto=""):
        if archivo:
            print(texto, file=archivo)
        else:
            print(texto)

    escribir()
    escribir("=" * ancho)
    escribir(f"{'SIMULACIÓN DE FLOTA DE TAXIS':^{ancho}}")
    escribir("=" * ancho)

    escribir(f"\n  Franja horaria : {franja.upper()}")
    escribir(f"  Tarifa base    : ${sim.tarifa_base:.2f}")
    escribir(f"  Configuración  : TC={CANTIDAD_CONVENCIONALES[i]}, TE={CANTIDAD_ELECTRICOS[i]}, TA={CANTIDAD_AUTONOMOS[i]}")
    escribir()

    escribir("-" * ancho)
    escribir(f"{'RESULTADOS GENERALES':^{ancho}}")
    escribir("-" * ancho)

    escribir(f"  {'Solicitudes totales':<35}: {sim._cantidad_solicitudes:>10}")
    escribir(f"  {'Viajes completados':<35}: {sim._cantidad_viajes_completados:>10}")
    escribir(f"  {'Pasajeros arrepentidos':<35}: {sim._cantidad_arrepentidos:>10}")
    escribir(f"  {'Porcentaje de arrepentimiento':<35}: {sim.PARR:>9.2f} %")
    escribir(f"  {'Tiempo promedio de espera':<35}: {sim.TPE:>9.2f} s")
    escribir(f"  {'Beneficio neto':<35}: ${sim.BN:>9.2f}")
    escribir()

    escribir("-" * ancho)
    escribir(f"{'DESEMPEÑO POR TIPO DE TAXI':^{ancho}}")
    escribir("-" * ancho)

    escribir(
        f"  {'Tipo':<18}"
        f"{'Tiempo ocioso':>18}"
        f"{'Calificación':>18}"
    )
    escribir("  " + "-" * 54)

    for tipo, tiempo_ocioso, nombre in (
            ("convencional", sim.TPOC, "Convencional"),
            ("electrico", sim.TPOE, "Eléctrico"),
            ("autonomo", sim.TPOA, "Autónomo"),
    ):
        calificacion = sim.calificaciones.promedio(tipo)

        escribir(
            f"  {nombre:<18}"
            f"{tiempo_ocioso:>17.2f} %"
            f"{calificacion:>18.2f}"
        )

    escribir()

    escribir("-" * ancho)
    escribir(f"{'ESTADO DE LA FLOTA':^{ancho}}")
    escribir("-" * ancho)

    escribir(f"\n  Tiempo comprometido:")
    escribir(f"    {sim.flota.tiempo_comprometido}")

    escribir(f"\n  Tiempo ocioso:")
    escribir(f"    {sim.flota.tiempo_ocioso}")

    escribir()
    escribir("=" * ancho)
    escribir(f"{'FIN DE LA SIMULACIÓN':^{ancho}}")
    escribir("=" * ancho)
    escribir()


def probar_simulacion(franja=FRANJA):

    carpeta_resultados = os.path.join(os.getcwd(), "resultados")
    os.makedirs(carpeta_resultados, exist_ok=True)

    for i in range(len(CANTIDAD_CONVENCIONALES)):
        sim = Simulacion(
            cantidad_convencionales=CANTIDAD_CONVENCIONALES[i],
            cantidad_electricos=CANTIDAD_ELECTRICOS[i],
            cantidad_autonomos=CANTIDAD_AUTONOMOS[i],
            franja=franja,
            tarifa_base=TARIFA_BASE_FRANJA[franja],
            seed=SEED,
        )

        sim.correr()
        # Abrimos el archivo y pasamos el manejador a imprimir_resultado
        nombre_archivo = os.path.join(carpeta_resultados, f"{franja}_{i+1}.txt")
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            imprimir_resultado(i, franja, sim, archivo=f)

        print(f"{FRANJA}_{i+1} Terminado")


if __name__ == "__main__":
    probar_simulacion()