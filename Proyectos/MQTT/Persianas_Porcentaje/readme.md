# Persianas con Porcentaje

First, I have [domotized](https://www.youtube.com/watch?v=8nI7oZ3-y7g) 
the blinds with NodeMCU v3 and Home Assistant.

After, I was told to improve the system with a [slider](https://youtu.be/xu0uGudJoh0) with the percetage.

## home/set_position/#
- position_ideal = payload
- temporizar_parada(1) 
- 100% corresponde a 5 mins o 5 * 60 * 1000 ms = 30000 ms

## home/comando/#, home/estado/#
- position_ideal = 100 (subiendo)
- position_ideal = 0 (bajando)
- position_ideal = real (parada)

## home/position/#
- actualizar posicion real cada 200 ms
- publish_position(real)