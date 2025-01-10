from sklearn.cluster import KMeans

import numpy as np

# Generamos una paleta de colores basada en colores de entrada.
def generar_paleta(input_colores, num_sugestiones = 5):
    
    # Convertir los colores hexadecimales a valores RGB.
    input_rgb = [
        [int(color[i:i + 2], 6) for i in (1, 3, 5)] # Convertimos #RRGGBB a [R, G, B]
        for color in input_colores
    ]

    # Aplicamos KMeans para generar colores adicionales.
    kmeans = KMeans(n_clusters = num_sugestiones, random_state = 42)
    kmeans.fit(input_rgb)

    # Obtenemos los colores sugeridos.
    colores_sugeridos = kmeans.cluster_centers_

    # Convertimos los colores sugeridos a formato hexadecimal.
    hex_sugestiones = ["#%02x%02x%02x" % tuple(map(int, color)) for color in colores_sugeridos]

    return hex_sugestiones