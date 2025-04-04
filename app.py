import json
import pickle
from flask import Flask,request,jsonify,render_template
from src.helper import predict_class,get_response
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


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
    intent = predict_class(user_input,words,classes,model)
    response = get_response(intent,intents)
    return jsonify({"response":response})

if __name__=="__main__":
    app.run(debug=True)
