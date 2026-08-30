"""
Prueba rápida y manual de la simulación para una sola franja horaria,
con parámetros chicos hardcodeados para revisar el comportamiento a
simple vista.

Ejecutalo directo con el botón Run del IDE, o con: python probar.py
"""

from config import TARIFA_BASE_FRANJA
from simulacion import Simulacion

# --- Parámetros hardcodeados de la flota, la franja y el horizonte de prueba ---
CANTIDAD_CONVENCIONALES = 10
CANTIDAD_ELECTRICOS = 20
CANTIDAD_AUTONOMOS = 5
FRANJA = "madrugada"  # una de: "madrugada", "manana", "tarde", "noche"
SEED = None


def imprimir_resultado(franja, sim, archivo=None):
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

    escribir(f"\n  Nivel de energía:")
    escribir(f"    {sim.energia.nivel}")

    escribir()
    escribir("=" * ancho)
    escribir(f"{'FIN DE LA SIMULACIÓN':^{ancho}}")
    escribir("=" * ancho)
    escribir()


def probar_simulacion(franja=FRANJA):
    sim = Simulacion(
        cantidad_convencionales=CANTIDAD_CONVENCIONALES,
        cantidad_electricos=CANTIDAD_ELECTRICOS,
        cantidad_autonomos=CANTIDAD_AUTONOMOS,
        franja=franja,
        tarifa_base=TARIFA_BASE_FRANJA[franja],
        seed=SEED,
    )
    sim.correr()
    # Abrimos el archivo y pasamos el manejador a imprimir_resultado
    with open("resultados.txt", "w", encoding="utf-8") as f:
        imprimir_resultado(franja, sim, archivo=f)


if __name__ == "__main__":
    probar_simulacion()