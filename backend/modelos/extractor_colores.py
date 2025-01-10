from PIL import Image
from sklearn.cluster import KMeans

import numpy as np

# Función para extraer los colores dominantes del archivo usando KMeans.
def extractor_colores(archivo_imagen, num_colores = 5):

    # Abrimos la imagen
    imagen = Image.open(archivo_imagen)
    imagen = imagen.resize((100, 100)) # Reducimos el tamaño para mejorar el rendimiento.
    imagen_data = np.array(imagen)

    # Convertimos la imagen a un array bidimensional.
    pixeles = imagen_data.reshape(-1, 3)

    # Usamos KMeans para encontrar los colores dominantes.
    kmeans = KMeans(n_clusters = num_colores)
    kmeans.fit(pixeles)

    # Obtenemos los colores dominantes.
    colores = kmeans.cluster_centers_

    # Convertimos los colores a formato hexadecimal.
    hex_colores = ["#%02x%02x%02x" % tuple(map(int, color)) for color in colores]

    return hex_colores