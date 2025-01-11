from PIL import Image

# Varificamos si el archivo es una imagen válida.
def validar_imagen(archivo):

    try:
        Image.open(archivo).verify # Verificamos que el archivo es una imagen.
        return True
    except Exception:
        return False
    
# Calculamos el constraste entre dos colores en formato hexadecimal usando la fórmula de luminancia relativa.
def calcular_contraste(color1, color2):

    def hex_a_rgb(hex_color):
        return [int(hex_color[i:i + 2], 16) / 255.0 for i in (1, 3, 5)]
    
    def luminancia(rgb):
        r, g, b = rgb
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if r <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if r <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4

        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    rgb1 = hex_a_rgb(color1)
    rgb2 = hex_a_rgb(color2)

    lum1 = luminancia(rgb1)
    lum2 = luminancia(rgb2)

    radio_contraste = (lum1 + 0.05) / (lum2 + 0.05) if lum1 > lum2 else (lum2 + 0.05) / (lum1 + 0.05)

    return round(radio_contraste, 2)