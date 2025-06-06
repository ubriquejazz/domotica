import time
from picamzero import Camera

print("Iniciando la camara...")
try:
	cam = Camera()
	print("Presiona CTRL+C para salir.")
	time.sleep(2)
	cam.take_photo("azotea.jpg")
except KeyboardInterrupt:
    print("\nPrograma interrumpido por el usuario.")
except Exception as e:
    print(f"Error: {e}")
finally:
    print("Cerrando el programa correctamente.")