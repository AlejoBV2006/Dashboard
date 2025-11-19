import os

carpeta = "C:/Users/santi/Downloads"  # Ajusta la ruta
for nombre in os.listdir(carpeta):
    ruta_original = os.path.join(carpeta, nombre)

    if os.path.isfile(ruta_original):
        # Separar nombre y extensión
        nombre_sin_ext, extension = os.path.splitext(nombre)

        # Verificar que el nombre sea solo un número
        for i in range(1, 19):
            if nombre_sin_ext == f'ejercicio{i}':
                nuevo_nombre = f"ejercicioFusion{i}{extension}"
                ruta_nueva = os.path.join(carpeta, nuevo_nombre)
        
                os.rename(ruta_original, ruta_nueva)
                print(f"{nombre} → {nuevo_nombre}")

