# Paneles Solares y Baterias

## Opcion 455

Dimensiones del panel solar: 1903 × 1134 × 30 mm con 24,2 kg

| Parameter | Symbol | Value |
| --------- | ------ | ----- |
| Maximum Power | Pmax(W) | 455W
| Open Circuit Voltage | Voc(V) | 41.2V
| Shortcircuit Current | Isc(A) | 14.00A
| Max. Power Current | Imp(A) | 13.17A

## Opcion 505W

Dimensiones de 2093 x 1134 x 30mm con un peso de 26.3kg

| Parameter | Symbol | Value |
| --------- | ------ | ----- |
| Potencia nominal | Pmax | 505W
| Open circuit | (Voc) | 45.72V
| Shortcircuit | (Isc) | 14.00A
| Max power | (Imp) | 13.11A

After considering above two parameters, the recommended setup is two units in serie.

n paneles en serie:
- n * Vmp > 55Vdc
- n * Voc < 450Vdc

## Baterias

Vamos a calcular el sistema de baterías de plomo ácido para una vivienda que necesita una autonomía de 2 días de consumo. Tras tener en cuenta todos los elementos de la vivienda, obtenemos un consumo de 2 kWh por día

- Profundidad de descarga: para baterías de plomo-ácido (50%) 
- Factor de corrección = 1,2 para plomo ácido.

Total: 2 kWh (consumo) x 2 (días) x 1,2 (factor de corrección) / 0,5 (profundidad de descarga) = 2,4 kWh.

Ahora transformamos esos 2,4 kWh a Amperios hora, dividiendo por la tensión de la batería 2400Wh / 24Vdc = 100Ah

**Tiempo de carga**

- Acumulador = 100Ah * 24V = 2400Wh
- Generacion 455 * 2 = 910W --> Tiempo = 2.1 horas


## Material

Amazon:

- 5AWG (16 mm2) de 50cm de longitud
- Fuse 150A, en paralelo con Breaker 200A, 24V

LiTime baterías 12V 100Ah admiten hasta 4 en serie y 4 en paralelo (máx. 4S4P) para más capacidad (200Ah, 300Ah, 400Ah) y mayor voltaje (24V, 36V, máx. 48V). Se puede conectar un máximo de 16 celdas para crear un sistema de baterías de 48V 400Ah, que proporciona un máximo de 20,48kWh de energía y 20,48kW de potencia de carga. 

Obramat:

- Estructura para módulos de hasta 2279 x 1150 mm y espesores de entre 30 y 45 mm.
- latiguillo (34 mm2) con agujero M8
- Battery wire: 2 x 8AWG (10 mm2) de 1.5m de longitud
