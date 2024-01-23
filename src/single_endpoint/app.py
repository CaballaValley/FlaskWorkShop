import os

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def say_hello():
    hello = "¡Hello!"
    return hello


@app.route('/custom-greeting', methods=['GET'])
def get_custom_greeting():
    # curl "http://127.0.0.1:5000/custom-greeting?talker=juan&listener=juana"
    # Get parameters from the request
    talker = request.args.get('talker', '')
    listener = request.args.get('listener', '')

    # Check if both parameters were provided
    if not talker or not listener:
        return "Both 'talker' and 'listener' parameters must be provided.", 400

    # Build the personalized greeting
    custom_greeting = f"Hello {listener}! I'm {talker} and I want to greet you."

    return custom_greeting


@app.route('/custom-greeting/<talker>/<listener>', methods=['GET'])
def get_custom_greeting_uri(talker, listener):
    # curl http://127.0.0.1:5000/custom-greeting/juan/juana
    # Check if both parameters were provided
    if not talker or not listener:
        return "Both 'talker' and 'listener' parameters must be provided.", 400

    # Build the personalized greeting
    custom_greeting = f"Hello {listener}! I'm {talker} and I want to greet you."

    return custom_greeting


@app.route('/custom-greeting', methods=['POST'])
def get_custom_greeting_post():
    # curl -X POST -H "Content-Type: application/json" -d '{"talker": "John", "listener": "Mary"}' http://127.0.0.1:5000/custom-greeting

    # Obtener los parámetros de la solicitud POST
    data = request.get_json()

    # Verificar si se proporcionaron ambos parámetros
    if 'talker' not in data or 'listener' not in data:
        return "Both 'talker' and 'listener' parameters must be provided in the JSON data.", 400

    # Obtener los valores de los parámetros
    talker = data['talker']
    listener = data['listener']

    # Construir el saludo personalizado
    custom_greeting = f"Hello {listener}! I'm {talker} and I want to greet you."

    return custom_greeting


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


@app.route('/upload-image', methods=['POST'])
def upload_image():
    # curl -X POST -F "file=@/home/ewokcillo/Imágenes/demigrante.jpg" -F "filename=careto.jpg" http://127.0.0.1:5000/upload-image
    # Verificar si la solicitud POST tiene el archivo adjunto
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # Verificar si se ha proporcionado un nombre de archivo en la solicitud POST
    if 'filename' not in request.form:
        return jsonify({'error': 'Filename not provided'}), 400

    filename = request.form['filename']

    # Verificar si el archivo tiene un nombre permitido y es una imagen
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400

    # Guardar el archivo en la carpeta de subidas con el nombre proporcionado
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return jsonify({'message': 'File uploaded successfully'}), 200


@app.route('/fibonacci/<int:start>/<int:end>', methods=['GET'])
def get_fibonacci(start, end):
    # curl http://127.0.0.1:5000/fibonacci/1/10
    # calculate fibonacci numbers between start and end
    fibonacci = [0, 1]
    while fibonacci[-1] < end:
        fibonacci.append(fibonacci[-1] + fibonacci[-2])
    fibonacci = fibonacci[1:-1]
    # filter fibonacci numbers between start and end
    fibonacci = list(filter(lambda x: x > start and x < end, fibonacci))

    # return fibonacci numbers in json format
    return jsonify(fibonacci)


if __name__ == '__main__':
    app.run(debug=True)
