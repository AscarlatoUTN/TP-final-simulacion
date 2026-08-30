"""
Prueba rápida y manual de la simulación para una sola franja horaria,
con parámetros chicos hardcodeados para revisar el comportamiento a
simple vista.

Ejecutalo directo con el botón Run del IDE, o con: python probar.py
"""

from config import LAMBDAS_FRANJA, TARIFA_BASE_FRANJA
from simulacion import Simulacion

# --- Parámetros hardcodeados de la flota, la franja y el horizonte de prueba ---
CANTIDAD_CONVENCIONALES = 2
CANTIDAD_ELECTRICOS = 2
CANTIDAD_AUTONOMOS = 1
FRANJA = "madrugada"  # una de: "madrugada", "manana", "tarde", "noche"
SEED = 1


def imprimir_resultado(franja, sim):
    ancho = 70

    print()
    print("=" * ancho)
    print(f"{'SIMULACIÓN DE FLOTA DE TAXIS':^{ancho}}")
    print("=" * ancho)

    print(f"\n  Franja horaria : {franja.upper()}")
    print(f"  Lambda         : {sim.lambda_arribo}")
    print(f"  Tarifa base    : ${sim.tarifa_base:.2f}")
    print()

    print("-" * ancho)
    print(f"{'RESULTADOS GENERALES':^{ancho}}")
    print("-" * ancho)

    print(f"  {'Solicitudes totales':<35}: {sim._cantidad_solicitudes:>10}")
    print(f"  {'Viajes completados':<35}: {sim._cantidad_viajes_completados:>10}")
    print(f"  {'Pasajeros arrepentidos':<35}: {sim._cantidad_arrepentidos:>10}")
    print(f"  {'Porcentaje de arrepentimiento':<35}: {sim.PARR:>9.2f} %")
    print(f"  {'Tiempo promedio de espera':<35}: {sim.TPE:>9.2f} s")
    print(f"  {'Beneficio neto':<35}: ${sim.BN:>9.2f}")
    print()

    print("-" * ancho)
    print(f"{'DESEMPEÑO POR TIPO DE TAXI':^{ancho}}")
    print("-" * ancho)

    print(
        f"  {'Tipo':<18}"
        f"{'Tiempo ocioso':>18}"
        f"{'Calificación':>18}"
    )
    print("  " + "-" * 54)

    for tipo, tiempo_ocioso, nombre in (
            ("convencional", sim.TPOC, "Convencional"),
            ("electrico", sim.TPOE, "Eléctrico"),
            ("autonomo", sim.TPOA, "Autónomo"),
    ):
        calificacion = sim.calificaciones.promedio(tipo)

        print(
            f"  {nombre:<18}"
            f"{tiempo_ocioso:>17.2f} %"
            f"{calificacion:>18.2f}"
        )

    print()

    print("-" * ancho)
    print(f"{'ESTADO DE LA FLOTA':^{ancho}}")
    print("-" * ancho)

    print(f"\n  Tiempo comprometido:")
    print(f"    {sim.flota.tiempo_comprometido}")

    print(f"\n  Tiempo ocioso:")
    print(f"    {sim.flota.tiempo_ocioso}")

    print(f"\n  Nivel de energía:")
    print(f"    {sim.energia.nivel}")

    print()
    print("=" * ancho)
    print(f"{'FIN DE LA SIMULACIÓN':^{ancho}}")
    print("=" * ancho)
    print()


def probar_simulacion(franja=FRANJA):
    sim = Simulacion(
        cantidad_convencionales=CANTIDAD_CONVENCIONALES,
        cantidad_electricos=CANTIDAD_ELECTRICOS,
        cantidad_autonomos=CANTIDAD_AUTONOMOS,
        lambda_arribo=LAMBDAS_FRANJA[franja],
        tarifa_base=TARIFA_BASE_FRANJA[franja],
        seed=SEED,
    )
    sim.correr()
    imprimir_resultado(franja, sim)


if __name__ == "__main__":
    probar_simulacion()