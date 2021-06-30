from flask import Flask, request, jsonify
from flask_cors import CORS
from models.word import Word
from models.util import get_dictionary_info

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

#test curl -X POST http://127.0.0.1:5000/add/popup -d '{"word":"ace"}'  -H "Content-Type: application/json"
@app.route("/add/popup", methods=["POST"])
def from_popup():
    data = request.get_json()
    word = data.get("word")
    speech, definition, examples= get_dictionary_info(word)
    print(type(speech))
    print(type(definition))
    print(type(examples))
    new_word = Word(word, speech, definition, examples)
    new_word.insert()

    return jsonify({"speech":speech, "definition":definition, "examples":examples})


