from flask import Flask, request, jsonify, render_template
from backend.modelos.extractor_colores import extractor_colores
from backend.modelos.modelo import generar_paleta
from backend.utils.helpers import validar_imagen, calcular_contraste

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods = ['POST'])

# Endpoint para cargar una imágen y generar una paleta de colores.
def cargar_imagen():

    if 'file' not in request.files:
        return jsonify({'error': 'No hay parte de archivo en la solicitud.'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No hay ningún archivo seleccionado.'}), 400
    
    if not validar_imagen(file):
        return jsonify({'error': 'Tipo de archivo invalido. Por favor, cargue una imagen.'}), 400
    
    # Procesamos la imagen para extraer colores.
    try:
        colores = extractor_colores(file)
        print(f"Colores extraídos: {colores}")
    except Exception as e:
        print(f"Error al procesar la imagen: {str(e)}")
        return jsonify({'error': f'Error al procesar la imagen: {str(e)}'}), 500

    return jsonify({'Colores': colores}), 200

@app.route('/api/palette', methods = ['POST'])

# Endpoint para generar una paleta basada en colores proporcionados o preferencias.
def generar_paleta_endpoint():
    
    try:
        # Obtener los datos enviados por el cliente.
        input_colors = request.json.get('colors', [])
        if not input_colors:
            return jsonify({'error': 'No se proporcionaron colores'}), 400

        # Generar la paleta de colores.
        palette = generar_paleta(input_colors)
        return jsonify({'palette': palette})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contrast', methods = ['POST'])

# Endpoint para analizar el contraste entre dos colores.
def analizar_contraste():
    
    data = request.get_json()
    if not data or 'color1' not in data or 'color2' not in data:
        return jsonify({'error': 'Faltan colores en la solicitud.'}), 400

    try:
        radio_contraste = calcular_contraste(data['color1'], data['color2'])
    except Exception as e:
        return jsonify({'error': f'Fallo al cacular el contraste: {str(e)}'}), 500

    return jsonify({'radio_constraste': radio_contraste}), 200

if __name__ == "__main__":
    app.run(debug = True)