import numpy as np
import re
import random
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.data.path.append("/opt/render/nltk_data")

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def predict_class(user_input,words,classes,model):
    bag = []

    input_words = user_input.lower().split()
    user_input = re.sub(r'[^a-zA-Z0-9\s]', '', user_input)
    input_words = [lemmatizer.lemmatize(word) for word in input_words if word not in stop_words]

    for word in words:
        bag.append(1) if word in input_words else bag.append(0)

    
    prediction = model.predict(np.array([bag]))[0]
    ERROR_THRESHOLD = 0.25
    intents_probabilities = [[intent,probability] for intent,probability in enumerate(prediction) if probability>ERROR_THRESHOLD]
    intents_probabilities.sort(key = lambda x:x[1], reverse=True)

    if not intents_probabilities:
        return None
    
    return classes[intents_probabilities[0][0]]


def get_response(intent,intents):
    if not intent:
        return "I'm sorry, I don't understand can you rephrase that"
    
    tag = intent
    for intent in intents['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
