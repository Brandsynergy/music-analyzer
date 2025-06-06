from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import tempfile
import random

app = Flask(__name__, static_folder='static')
CORS(app)

# Simple mock analysis function for demonstration
def analyze_music_file(file_path):
    """
    Mock analysis function that returns realistic results
    In a production environment, this would use Librosa and ML models
    """
    
    # Simulate different genres based on file characteristics
    genres = ['electronic', 'rock', 'pop', 'jazz', 'classical', 'hip-hop', 'country', 'blues']
    primary_genre = random.choice(genres)
    
    # Generate realistic style characteristics
    style_characteristics = {
        'acoustic': random.uniform(0.1, 0.9),
        'electronic': random.uniform(0.1, 0.9),
        'instrumental': random.uniform(0.2, 0.8),
        'vocal': random.uniform(0.2, 0.8),
        'energetic': random.uniform(0.3, 0.95),
        'calm': random.uniform(0.05, 0.7),
        'dark': random.uniform(0.1, 0.8),
        'bright': random.uniform(0.2, 0.9),
        'atmospheric': random.uniform(0.1, 0.9),
        'rhythmic': random.uniform(0.4, 0.95),
        'melodic': random.uniform(0.3, 0.9),
        'harmonic': random.uniform(0.2, 0.8),
        'distorted': random.uniform(0.05, 0.6),
        'clean': random.uniform(0.4, 0.95)
    }
    
    # Generate audio features
    features = {
        'spectral_centroid': random.uniform(1000, 5000),
        'spectral_bandwidth': random.uniform(800, 3000),
        'spectral_rolloff': random.uniform(2000, 8000),
        'zero_crossing_rate': random.uniform(0.01, 0.15),
        'rms': random.uniform(0.05, 0.3),
        'tempo': random.uniform(60, 180),
        'harmonic_ratio': random.uniform(0.3, 0.8),
        'percussive_ratio': random.uniform(0.2, 0.7),
        'mfcc_1': random.uniform(-300, 100),
        'mfcc_2': random.uniform(-50, 100),
        'mfcc_3': random.uniform(-30, 50),
        'mfcc_4': random.uniform(-20, 80),
        'chroma_1': random.uniform(0.1, 0.9),
        'chroma_2': random.uniform(0.1, 0.9),
        'chroma_3': random.uniform(0.1, 0.9),
        'chroma_4': random.uniform(0.1, 0.9)
    }
    
    # Generate alternative genres
    alternatives = []
    other_genres = [g for g in genres if g != primary_genre]
    for i in range(3):
        if other_genres:
            genre = random.choice(other_genres)
            other_genres.remove(genre)
            alternatives.append({
                'genre': genre,
                'probability': random.uniform(0.1, 0.4)
            })
    
    return {
        'genre': {
            'primary': primary_genre,
            'probability': random.uniform(0.7, 0.95),
            'alternatives': alternatives
        },
        'style_characteristics': style_characteristics,
        'features': features
    }
@app.route('/')
def home():
    return "Music Analyzer API is running!"

@app.route('/api/music/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Music analyzer API is running'})
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/music/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Music analyzer API is running'})

@app.route('/api/music/analyze', methods=['POST'])
def analyze_music():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension
        allowed_extensions = {'.mp3', '.wav', '.ogg', '.flac', '.m4a'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            return jsonify({'error': 'Unsupported file format'}), 400
        
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
        
        try:
            # Analyze the music file
            result = analyze_music_file(temp_path)
            return jsonify(result)
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

