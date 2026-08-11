from simulacion import Simulacion


def probar_simulacion():
    sim = Simulacion(
        cantidad_convencionales=2,
        cantidad_electricos=2,
        cantidad_autonomos=1,
        lambda_arribo=0.05,
        seed=1,
    )
    sim.correr()

    print(sim)
    print("tiempo_comprometido:", sim.flota.tiempo_comprometido)
    print("tiempo_ocioso:", sim.flota.tiempo_ocioso)
    print("porcentaje de pasajeros arrepentidos:", )


if __name__ == "__main__":
    probar_simulacion()