from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import random

from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import random
import os
import numpy as np
from PIL import Image
import io
import time

# In a real implementation, you would use:
# - A pre-trained deep learning model (like ResNet, EfficientNet, etc.)
# - A movie scene database or API (like TMDb)
# - Image feature extraction and matching algorithms

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample database of recognizable scenes (in a real app, this would be much larger)
# and would likely connect to an external movie/TV database API
SCENE_DATABASE = [
    {
        "id": "scene001",
        "title": "Stranger Things",
        "type": "TV Show",
        "season": "4",
        "episode": "9",
        "year": 2022,
        "mediaId": "st001",
        "features": np.random.rand(512),  # In real app: feature vector from the image
        "description": "The final confrontation between Eleven and Vecna in the Upside Down.",
        "actors": ["Millie Bobby Brown", "Jamie Campbell Bower", "Sadie Sink"]
    },
    {
        "id": "scene002",
        "title": "The Dark Knight",
        "type": "Movie",
        "year": 2008,
        "mediaId": "dk001",
        "features": np.random.rand(512),
        "description": "The iconic interrogation scene between Batman and the Joker.",
        "actors": ["Christian Bale", "Heath Ledger", "Gary Oldman"]
    },
    {
        "id": "scene003",
        "title": "Game of Thrones",
        "type": "TV Show",
        "season": "6",
        "episode": "10",
        "year": 2016,
        "mediaId": "got001",
        "features": np.random.rand(512),
        "description": "The dramatic 'Battle of the Bastards' scene where Jon Snow faces off against Ramsay Bolton.",
        "actors": ["Kit Harington", "Iwan Rheon", "Sophie Turner"]
    },
    {
        "id": "scene004",
        "title": "Inception",
        "type": "Movie",
        "year": 2010,
        "mediaId": "inc001",
        "features": np.random.rand(512),
        "description": "The famous rotating hallway fight scene.",
        "actors": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Tom Hardy"]
    },
    {
        "id": "scene005",
        "title": "Breaking Bad",
        "type": "TV Show",
        "season": "5",
        "episode": "14",
        "year": 2013,
        "mediaId": "bb001",
        "features": np.random.rand(512),
        "description": "Walter White's 'I am the one who knocks' monologue.",
        "actors": ["Bryan Cranston", "Anna Gunn"]
    }
]

@app.route('/api/recognize-scene', methods=['POST'])
def recognize_scene():
    # Check if image is included in the request
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    image_file = request.files['image']
    
    # Safety checks
    if image_file.filename == '':
        return jsonify({"error": "No image selected"}), 400
    
    try:
        # Read and process the image
        image_bytes = image_file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # In a real application:
        # 1. Preprocess the image (resize, normalize, etc.)
        # 2. Extract features using a CNN
        # 3. Compare against database or use specialized model
        # 4. Return best match with confidence score
        
        # For demo purposes, wait briefly and return a random scene
        # with confidence level between 80-99%
        time.sleep(2)  # Simulate processing time
        
        # Select a random scene from our database
        scene = random.choice(SCENE_DATABASE)
        confidence = random.randint(80, 99)
        
        return jsonify({
            "title": scene["title"],
            "type": scene["type"],
            "season": scene.get("season", None),
            "episode": scene.get("episode", None),
            "year": scene["year"],
            "mediaId": scene["mediaId"],
            "confidence": confidence,
            "description": scene["description"],
            "actors": scene["actors"]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# CHATBOT SECTION

# Predefined responses for different types of queries
movie_responses = {
    "greeting": [
        "Hello! How can I help you find your next favorite watch?",
        "Hi there! Looking for movie or show recommendations?",
        "Welcome! I can help you discover new content to watch."
    ],
    "recommendation": [
        "Based on popular trends, you might enjoy 'The Last Kingdom', 'Stranger Things', or 'Breaking Bad'.",
        "Some top-rated shows right now include 'Succession', 'The Bear', and 'The Boys'.",
        "If you're into action, I'd recommend 'John Wick', 'The Gray Man', or 'Extraction'."
    ],
    "genre": {
        "action": ["'The Gray Man', 'Extraction', 'John Wick' are great action picks.", 
                  "For action fans, check out 'Mission Impossible', 'Fast & Furious', or 'The Equalizer'."],
        "comedy": ["'Ted Lasso', 'The Office', and 'Brooklyn Nine-Nine' should give you a good laugh.",
                  "For comedy, I recommend 'Barb and Star Go to Vista Del Mar', 'Booksmart', or 'Palm Springs'."],
        "drama": ["'The Crown', 'Succession', and 'Better Call Saul' are excellent drama choices.",
                 "For drama fans, try 'The Last of Us', 'Yellowstone', or 'This Is Us'."],
        "horror": ["'The Haunting of Hill House', 'Midnight Mass', or 'Stranger Things' will keep you on edge.",
                  "For horror fans, check out 'Hereditary', 'The Witch', or 'Get Out'."],
        "sci-fi": ["'Dune', 'The Expanse', and 'Severance' are fantastic sci-fi options.",
                  "For sci-fi lovers, try 'Foundation', 'Westworld', or 'Black Mirror'."]
    },
    "release": {
        "new": ["Check out our 'Latest Drops' section for the newest releases.",
               "Some recent releases include 'Dune: Part Two', 'Challengers', and 'The Fall Guy'."],
        "upcoming": ["We're excited about upcoming titles like 'Gladiator 2', 'Furiosa', and 'Inside Out 2'.",
                    "Keep an eye out for 'The Batman 2', 'Dune 3', and 'Avatar 3' in the future."]
    },
    "account": ["You can manage your watchlist in your account settings.",
                "To update your subscription, please visit the account section."],
    "help": ["I can help with movie recommendations, account questions, or information about our content.",
            "Ask me about new releases, specific genres, or how to use our platform!"],
    "fallback": ["I'm not sure I understand. Could you rephrase that?",
                "Sorry, I didn't catch that. Try asking about movies, shows, or your account.",
                "I'm still learning! Try asking about recommendations or new releases."]
}

# Function to determine intent from user message
def get_intent(message):
    message = message.lower()
    
    # Check for greetings
    if re.search(r'\b(hi|hello|hey|greetings)\b', message):
        return "greeting"
    
    # Check for recommendation requests
    if re.search(r'\b(recommend|suggestion|what to watch|what should i watch)\b', message):
        return "recommendation"
    
    # Check for genre-specific requests
    genres = {
        "action": r'\b(action|adventure|exciting|thriller)\b',
        "comedy": r'\b(comedy|funny|laugh|humor)\b',
        "drama": r'\b(drama|emotional|powerful)\b',
        "horror": r'\b(horror|scary|terrifying|spooky)\b',
        "sci-fi": r'\b(sci-fi|science fiction|futuristic|space)\b'
    }
    
    for genre, pattern in genres.items():
        if re.search(pattern, message):
            return f"genre_{genre}"
    
    # Check for release-related queries
    if re.search(r'\b(new|latest|recent)\b', message):
        return "release_new"
    if re.search(r'\b(upcoming|coming soon|future|next)\b', message):
        return "release_upcoming"
    
    # Check for account-related queries
    if re.search(r'\b(account|profile|subscription|payment|watchlist)\b', message):
        return "account"
    
    # Check for help
    if re.search(r'\b(help|support|how to|guide)\b', message):
        return "help"
    
    # Fallback
    return "fallback"

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_message = data.get('message', '')
    
    # Get intent from user message
    intent = get_intent(user_message)
    
    # Generate response based on intent
    if intent == "greeting":
        response = random.choice(movie_responses["greeting"])
    elif intent == "recommendation":
        response = random.choice(movie_responses["recommendation"])
    elif intent.startswith("genre_"):
        genre = intent.split("_")[1]
        response = random.choice(movie_responses["genre"][genre])
    elif intent.startswith("release_"):
        release_type = intent.split("_")[1]
        response = random.choice(movie_responses["release"][release_type])
    elif intent == "account":
        response = random.choice(movie_responses["account"])
    elif intent == "help":
        response = random.choice(movie_responses["help"])
    else:
        response = random.choice(movie_responses["fallback"])
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=False)




