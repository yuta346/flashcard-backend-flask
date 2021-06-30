from flask import Flask, request, jsonify
from flask_cors import CORS
from models.word import Word

app = Flask(__name__)


#test curl -X POST http://127.0.0.1:5000/add -d '{"word":"grape","speech":"noun","definition":"fruit","example":"none"}'  -H "Content-Type: application/json"
@app.route("/add", methods=["POST"])
def add():

    data = request.get_json()

    word = data.get("word")
    speech = data.get("speech")
    definition = data.get("definition")
    example = data.get("example")
    
    new_word = Word(word, speech, definition, example)
    new_word.insert()

    return jsonify({"status":"added"})
