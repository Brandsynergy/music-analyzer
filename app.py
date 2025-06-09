from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import tempfile
import random

app = Flask(__name__)
CORS(app)

# Simulate analysis
def analyze_music_file(file_path):
    genres = ['electronic', 'rock', 'pop', 'jazz', 'afrobeat', 'amapiano']
    primary_genre = random.choice(genres)

    return {
        'genre': primary_genre,
        'confidence': round(random.uniform(0.7, 0.99), 2)
    }

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/music/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Service is healthy'})

@app.route('/api/music/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    file_ext = os.path.splitext(file.filename)[1]

    if file_ext not in ['.mp3', '.wav']:
        return jsonify({'error': 'Unsupported file format'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
        file.save(temp_file.name)
        result = analyze_music_file(temp_file.name)
        os.unlink(temp_file.name)
        return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


