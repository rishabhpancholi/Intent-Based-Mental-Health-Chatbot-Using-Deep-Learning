import numpy as np
import re
import random
from nltk.stem import WordNetLemmatizer

# Initialize the WordNet lemmatizer
lemmatizer = WordNetLemmatizer()

# Function to predict the intent of the user input
def predict_class(user_input, words, classes, model, stop_words):
    bag = []  # Bag of words representation

    # Convert input to lowercase and tokenize
    input_words = user_input.lower().split()

    # Remove special characters from input
    user_input = re.sub(r'[^a-zA-Z0-9\s]', '', user_input)

    # Lemmatize and remove stopwords
    input_words = [lemmatizer.lemmatize(word) for word in input_words if word not in stop_words]

    # Create the bag of words: 1 if word exists in input, else 0
    for word in words:
        bag.append(1) if word in input_words else bag.append(0)

    # Predict probabilities for each class using the trained model
    prediction = model.predict(np.array([bag]))[0]

    # Set a minimum threshold to filter out low-confidence predictions
    ERROR_THRESHOLD = 0.25
    intents_probabilities = [
        [intent, probability] 
        for intent, probability in enumerate(prediction) 
        if probability > ERROR_THRESHOLD
    ]

    # Sort intents by probability in descending order
    intents_probabilities.sort(key=lambda x: x[1], reverse=True)

    # Return the class with the highest probability if available
    if not intents_probabilities:
        return None
    
    return classes[intents_probabilities[0][0]]

# Function to get a random response for a given intent
def get_response(intent, intents):
    # If no intent was detected
    if not intent:
        return "I'm sorry, I don't understand. Can you rephrase that?"

    tag = intent

    # Search for matching intent in the intents JSON
    for intent in intents['intents']:
        if intent['tag'] == tag:
            # Return a random response from the list of responses
            return random.choice(intent['responses'])

