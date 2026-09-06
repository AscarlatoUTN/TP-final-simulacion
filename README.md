# Simulación de flota de taxis 🚕⚡🤖
 
Simulación de eventos discretos de una flota de taxis compuesta por tres
tipos de vehículos —**convencionales**, **eléctricos** y **autónomos**—,
compitiendo por pasajeros según su reputación, con consumo de energía,
reabastecer/reabastecimiento y cálculo de beneficio neto.
 
## Cómo correrlo
 
Todos los archivos usan imports simples (sin paquete), así que alcanza con
ejecutarlos directo, parado en esta carpeta o desde el botón Run del IDE:
 
```bash
python main.py     # probar UNA franja horaria puntual, con salida detallada
python probar.py   # probar las CUATRO franjas horarias, una atrás de otra
```
 
## Qué hace cada archivo
 
### `config.py`
El "panel de control" del modelo: todas las constantes y parámetros en un
solo lugar. Cantidad de taxis por tipo y tarifa base por franja horaria,
parámetros del sistema de calificaciones (reputación inicial, tablas de
aceptación, filtro de apertura a autónomos) y parámetros energéticos
(capacidad de tanque/batería, consumo, umbral y tiempo de reabastecer,
costos). `TIPOS_FRANJAS` quedó como la lista de las 4 franjas
horarias (`madrugada`, `manana`, `tarde`, `noche`) que usa `probar.py`
para iterarlas. Cada franja tiene ahora su propia FDP
ajustada (ver `generadores.py`). Los parámetros de esas FDPs por franja
todavía viven adentro de `generadores.py`, no acá.
 
### `generadores.py`
Funciones de generación de variables aleatorias. El intervalo entre
arribos (`IA`) ya no es una única Exponencial: **cada franja horaria tiene
su propia FDP ajustada** (`generar_ia_1` a `generar_ia_4`, una por franja),
combinadas en `generar_intervalo_arribo(rng, franja)` según el nombre de
la franja. `madrugada` y `noche` usan una Exponencial desplazada (método
de la inversa), `tarde` una distribución de potencia inversa, y `manana`
usa **aceptación-rechazo** (genera candidatos hasta que uno cae bajo la
curva de densidad objetivo). La distancia del viaje (DIS) usa una Lognormal ajustada con scipy.stats.lognorm (parámetros s=0.9294, loc=0, scale=1.8581), generada por el método de la inversa: DIS = scale · e^(s·Φ⁻¹(R)) y
el tiempo de viaje en función de la distancia (`TV = 480 + 144·DIS`) siguen
siendo los mismos para las 4 franjas. Todas las funciones reciben el
generador `rng` como parámetro en vez de usar uno global, para que la
simulación sea reproducible con una semilla (`seed`).
 
### `flota.py`
La clase `Flota`: mantiene el estado físico de los vehículos. Para cada
tipo, dos arrays (uno por taxi): `tiempo_comprometido` (cuándo queda libre
cada uno) y `tiempo_ocioso` (cuánto tiempo acumulado pasó ocioso). Resuelve
la pregunta "¿qué taxi de este tipo se libera antes, y cuánto hay que
esperarlo?" (`taxi_disponible`), y calcula el % de tiempo ocioso promedio
de la flota al finalizar (`tiempo_ocioso_promedio`, tras llamar a
`finalizar` para sumar el tramo ocioso final de cada vehículo).
 
### `calificaciones.py`
La clase `SistemaCalificaciones`: implementa la reputación de cada tipo de
servicio como una ventana móvil de las últimas 100 valoraciones, arrancando
en la reputación inicial del enunciado. Decide qué tipo intenta primero el
pasajero (`mejor_tipo`, siempre el mejor calificado), si el pasajero acepta
ese servicio (`pasajero_acepta`, con el filtro del 29% para autónomos y la
tabla de probabilidad de aceptación por calificación), y calcula la
calificación de cada viaje completado (`registrar_viaje`, penalizando la
espera y ajustando según el tipo de vehículo).
 
### `Capacidad.py`
La clase `Capacidad`: mantiene el nivel de combustible/batería de cada
vehículo (equivalente a `CVC`, `CVE`, `CVA` del enunciado), uno por taxi.
Descuenta el consumo de cada viaje según la distancia recorrida
(`consumir`), detecta cuándo un vehículo cruza el umbral de reabastecer
(`necesita_reabastecimiento`), y calcula el costo y tiempo fijo de la
reabastecer/reabastecimiento (`reabastecer`).
 
### `simulacion.py`
La clase `Simulacion`: el orquestador. No sabe *cómo* se genera una
distancia, se elige un taxi o se calcula una calificación — solo coordina
`Flota`, `SistemaCalificaciones` y `Capacidad` en el loop de eventos
(`correr`): genera la próxima llegada, procesa la solicitud
(`procesar_solicitud`: elección + aceptación del servicio, asignación de
taxi, consumo de energía y reabastecer, cobro del viaje, calificación) hasta
llegar al horizonte `TF` (constante global definida en este mismo
archivo), y al final calcula las métricas: `TPE`, `PTOC`, `PTOE`, `PTOA`,
`PARR` y `BN`.
 
### `main.py`
**Corre UNA sola franja horaria** (la que esté en la constante `FRANJA` de
arriba del archivo) con una flota chica hardcodeada, y muestra el resultado
con un formato bien detallado: encabezado, resultados generales, tabla de
desempeño por tipo de taxi (% ocioso y calificación), y el estado interno
completo de la flota (tiempo comprometido, tiempo ocioso, nivel de
energía por vehículo). Es el archivo para "meterse a fondo" en una franja
puntual. La función `imprimir_resultado` que define también la reutiliza
`probar.py`.
 
### `probar.py`
**Corre las CUATRO franjas horarias**, una atrás de la otra, con la misma
flota chica y semilla fija, reusando el formato de impresión de `main.py`
para cada una. Es el archivo para comparar rápido cómo cambia el
comportamiento de la simulación entre madrugada, mañana, tarde y noche.
 
## Consideraciones adicionales

- **Distribución del componente aleatorio de la calificación** (`error` en
  `calificaciones.py`): se usa una función equiprobable entre 1 y 5 estrellas
- **Espera > 15 minutos**: en caso de que el usuario deba esperar más de 15 minutos,
  desiste de tomar el viaje. Caso contrario, lo toma y la penalización en la calificación
  dependerá de ese tiempo.
- **Nivel inicial de combustible/batería**: todos los vehículos arrancan
  con el tanque/batería llenos al inicio de cada simulación.
- **Costos de adquisición y FSD anual** (`COSTO_ADQUISICION`,
  `COSTO_FSD_ANUAL` en `config.py`): Son dos valores que representan costos.
   Para calcular el `BN' , a los ingresos generados por el pago de los clientes se les descuenta estos dos costos
  y el costo asociado a los gastos en combustibles 
