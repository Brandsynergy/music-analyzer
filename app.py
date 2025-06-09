from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import tempfile
import random

app = Flask(__name__)
CORS(app)

# Simulate analysis
def analyze_music_file(file_path):
    genres = ['afrobeat', 'amapiano', 'afro-fusion', 'pop', 'r&b']
    primary_genre = random.choice(genres)

    beat_styles = {
        'afro_rhythm': round(random.uniform(0.7, 1.0), 2),
        'log_drum_intensity': round(random.uniform(0.5, 1.0), 2),
        'percussion_richness': round(random.uniform(0.6, 1.0), 2),
        'vocal_lift': round(random.uniform(0.5, 0.9), 2),
        'danceability': round(random.uniform(0.7, 1.0), 2),
        'call_response_style': round(random.uniform(0.3, 0.8), 2),
        'piano_roll_presence': round(random.uniform(0.4, 0.9), 2),
        'chop_vocal_elements': round(random.uniform(0.2, 0.7), 2)
    }

    return {
        'genre': primary_genre,
        'confidence': round(random.uniform(0.75, 0.95), 2),
        'beat_styles': beat_styles
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


