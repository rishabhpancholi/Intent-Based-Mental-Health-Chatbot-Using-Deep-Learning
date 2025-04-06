import json
import pickle
import os
from flask import Flask,request,jsonify,render_template
from src.helper import predict_class,get_response
import nltk

nltk_data_path = os.path.join(os.getcwd(), 'nltk_data')

if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)

nltk.data.path.append(nltk_data_path)

try:
    stop_words = set(nltk.corpus.stopwords.words('english'))
except LookupError:
    # Download stopwords if not found
    nltk.download('stopwords', download_dir=nltk_data_path)
    stop_words = set(nltk.corpus.stopwords.words('english'))

app = Flask(__name__)

with open("artifacts/mental_health_chatbot.pkl", "rb") as file:
    model = pickle.load(file)
with open("artifacts/intents.json", encoding="utf-8") as file:
    intents = json.load(file)
with open("artifacts/words.pkl", "rb") as file:
    words = pickle.load(file)
with open("artifacts/classes.pkl", "rb") as file:
    classes = pickle.load(file)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat',methods = ['POST'])
def chatbot_response():
    user_input = request.json.get('message')
    intent = predict_class(user_input,words,classes,model,stop_words)
    response = get_response(intent,intents)
    return jsonify({"response":response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port)
