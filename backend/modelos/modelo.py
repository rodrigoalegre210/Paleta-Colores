# Librerías.
from sklearn.cluster import KMeans

import numpy as np
import random
import colorsys

# Generamos una paleta de colores basada en colores de entrada.
def generar_paleta(input_colores, num_sugestiones = 5):
    
    # Convertimos colores a RGB.
    def hex_a_rgb(hex_color):
        return [int(hex_color[i:i + 2], 16) for i in (1, 3, 5)]
    
    def rgb_a_hex(rgb_color):
        return "#%02x%02x%02x" % tuple(np.clip(rgb_color, 0, 250))
    
    # Convertimos colores RGB a HSL y viceversa.
    def rgb_a_hsl(rgb_color):
        r, g, b = [x / 255.0 for x in rgb_color]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return [h * 360, l * 100, s * 100] # Convertimos a escala convencional H, L, S.
    
    def hsl_a_rgb(hls_color):
        h, l, s = [x / 360.0 if i == 0 else x / 100.0 for i, x in enumerate(hls_color)]
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return [int(r * 255), int(g * 255), int(b * 255)]
    
    # Convertimos colores de entrada a RGB.
    input_rgb = np.array([hex_a_rgb(color) for color in input_colores])

    # Trabajamos colores repetidos.
    input_rgb = np.unique(input_rgb, axis = 0)

    # Convertimos colores a espacios HSL para agregar diversidad.
    input_hsl = np.array([rgb_a_hsl(color) for color in input_rgb])

    # Generamos más colores si es necesario.
    while len(input_hsl) < num_sugestiones:
        base_color = random.choice(input_hsl)
        nuevo_hue = (base_color[0] + random.uniform(15, 60)) % 360 # Cambiamos el tono.
        nuevo_hsl = [nuevo_hue, random.uniform(30, 70), random.uniform(40, 80)] # Diversidad en luz y saturación.
        input_hsl = np.vstack([input_hsl, nuevo_hsl])

    # Convertimos de vuelta a RGB para aplicar KMeans.
    input_rgb = np.array([hsl_a_rgb(hls) for hls in input_hsl])

    # Aplicamos KMeans.
    kmeans = KMeans(n_clusters = num_sugestiones, random_state = 42, n_init = 'auto')
    kmeans.fit(input_rgb)
    colores_sugeridos = kmeans.cluster_centers_

    # Convertimos colores a HEX.
    paleta_hex = [rgb_a_hex(color.astype(int)) for color in colores_sugeridos]

    # Retronamos una lista de colores únicos.
    return list(dict.fromkeys(paleta_hex))