"""
Prueba rápida y manual de la simulación para una sola franja horaria,
con parámetros chicos hardcodeados para revisar el comportamiento a
simple vista.

Ejecutalo directo con el botón Run del IDE, o con: python probar.py
"""

import os
import config
from simulacion import Simulacion

def imprimir_resultado(i, franja, sim, archivo=None):
    ancho = 70

    def escribir(texto=""):
        if archivo:
            print(texto, file=archivo)
        else:
            print(texto)

    # formateadores (estilo español: miles con '.' y decimales con ',')
    def format_num_es(n):
        try:
            return f"{int(n):,}".replace(",", ".")
        except Exception:
            return str(n)

    def format_float_es(x, decimals=2):
        try:
            s = f"{x:,.{decimals}f}"   # "1,234,567.89"
            return s.replace(",", "X").replace(".", ",").replace("X", ".")
        except Exception:
            return str(x)

    escribir()
    escribir("=" * ancho)
    escribir(f"{'SIMULACIÓN DE FLOTA DE TAXIS':^{ancho}}")
    escribir("=" * ancho)

    escribir(f"\n  Franja horaria : {franja.upper()}")
    escribir(f"  Tarifa base    : ${sim.tarifa_base:.2f}")
    escribir(f"  Configuración  : TC={config.CANTIDAD_CONVENCIONALES[i]}, TE={config.CANTIDAD_ELECTRICOS[i]}, TA={config.CANTIDAD_AUTONOMOS[i]}")
    escribir()

    escribir("-" * ancho)
    escribir(f"{'RESULTADOS GENERALES':^{ancho}}")
    escribir("-" * ancho)

    # líneas con formateo por separado (enteros y floats)
    escribir(f"  {'Solicitudes totales':<35}: {format_num_es(sim._cantidad_solicitudes):>15}")
    escribir(f"  {'Viajes completados':<35}: {format_num_es(sim._cantidad_viajes_completados):>15}")
    escribir(f"  {'Pasajeros arrepentidos':<35}: {format_num_es(sim._cantidad_arrepentidos):>15}")
    # porcentaje: mantener formato con punto decimal y símbolo %
    escribir(f"  {'Porcentaje de arrepentimiento':<35}: {sim.PARR:>15.2f} %")
    # tiempo promedio de espera (float grande) con formateo
    escribir(f"  {'Tiempo promedio de espera':<35}: {format_float_es(sim.TPE, 2):>15} s")
    # beneficio neto con separador de miles y coma decimal
    escribir(f"  {'Beneficio neto':<35}: ${format_float_es(sim.BN, 2):>14}")
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

        # tiempo_ocioso ya es porcentaje; lo dejamos con formato xx.yy %
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
    # Para imprimir estructuras complejas, convertimos números dentro de ellas si queremos,
    # pero aquí mantenemos la representación original para legibilidad técnica.
    escribir(f"    {sim.flota.tiempo_comprometido}")

    escribir(f"\n  Tiempo ocioso:")
    escribir(f"    {sim.flota.tiempo_ocioso}")

    escribir()
    escribir("=" * ancho)
    escribir(f"{'FIN DE LA SIMULACIÓN':^{ancho}}")
    escribir("=" * ancho)
    escribir()



def probar_simulacion(franja=config.FRANJA):

    carpeta_resultados = os.path.join(os.getcwd(), "resultados")
    os.makedirs(carpeta_resultados, exist_ok=True)

    for i in range(len(config.CANTIDAD_CONVENCIONALES)):
        sim = Simulacion(
            cantidad_convencionales=config.CANTIDAD_CONVENCIONALES[i],
            cantidad_electricos=config.CANTIDAD_ELECTRICOS[i],
            cantidad_autonomos=config.CANTIDAD_AUTONOMOS[i],
            franja=franja,
            tarifa_base=config.TARIFA_BASE_FRANJA[franja],
            seed=config.SEED,
        )

        sim.correr()
        # Abrimos el archivo y pasamos el manejador a imprimir_resultado
        nombre_archivo = os.path.join(carpeta_resultados, f"{franja}_{i+1}.txt")
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            imprimir_resultado(i, franja, sim, archivo=f)

        print(f"{config.FRANJA}_{i+1} Terminado")


if __name__ == "__main__":
    probar_simulacion()