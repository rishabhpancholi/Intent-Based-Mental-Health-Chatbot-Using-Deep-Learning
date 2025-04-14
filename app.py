import json
import pickle
import os
from flask import Flask, request, jsonify, render_template

# Importing helper functions for intent prediction and response generation
from src.helper import predict_class, get_response

# Download necessary NLTK resources
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Load English stopwords
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

# Initialize Flask app
app = Flask(__name__)

# Load the trained chatbot model
with open("artifacts/mental_health_chatbot.pkl", "rb") as file:
    model = pickle.load(file)

# Load intents (questions & responses) from JSON
with open("artifacts/intents.json", encoding="utf-8") as file:
    intents = json.load(file)

# Load the vocabulary (tokenized words)
with open("artifacts/words.pkl", "rb") as file:
    words = pickle.load(file)

# Load the intent classes
with open("artifacts/classes.pkl", "rb") as file:
    classes = pickle.load(file)

# Home route - renders the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Chat route - receives user input and returns a chatbot response
@app.route('/chat', methods=['POST'])
def chatbot_response():
    # Get JSON data from the request
    data = request.get_json(force=True, silent=True)

    # Handle bad input gracefully
    if not data or 'message' not in data:
        return jsonify({"error": "Invalid input. 'message' key missing."}), 400

    # Extract user message
    user_input = data['message']

    # Predict the intent using the helper function
    intent = predict_class(user_input, words, classes, model, stop_words)

    # Get a response based on the predicted intent
    response = get_response(intent, intents)

    # Return the response in JSON format
    return jsonify({"response": response})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

