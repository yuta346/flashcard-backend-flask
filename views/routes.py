from flask import Flask, request, jsonify
from models.word import Word
from models.user import User
from models.schema import Users, Words
from models.setting import session
from models.util import get_dictionary_info, Error, WordNotFoundError



app = Flask(__name__)

#pre: Users table is initialized
#post add new user's info to the table and return a message
#test curl -X POST http://127.0.0.1:5000/add/user -d '{"username":"u3","email":"u3@gmail.com","password":"33333"}'  -H "Content-Type: application/json"
@app.route("/create_account", methods=["POST"])  #modify password and session_id later
def create_account():

    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    session_id = "12345"

    new_user = User(username, email, password, session_id)
    new_user.insert()
    User.display()

    return jsonify({"status":"success"})















#pre: Word's table is initialized
#post: add user's custom data the database and return a status message 
#test curl -X POST http://127.0.0.1:5000/add/card -d '{"word":"banana","speech":"noun","definition":"fruit","example":"none"}'  -H "Content-Type: application/json"
@app.route("/add/card", methods=["POST"])  #create user's custom card
def add():

    data = request.get_json()
    print(data)
    word = data.get("word")
    speech = data.get("speech")
    definition = data.get("definition")
    example = data.get("example")
    user_id = data.get("user_id")

    try:
        speech, definition, example = get_dictionary_info(word)
        new_word = Word(word,speech,definition,example,user_id)
        new_word.insert()
        words = Word.display()
        print(words)
        return jsonify({"status":"success"})
    except WordNotFoundError as e:
        return jsonify({"status":"fail"})


#pre: Word's table is initialized
#post: call api and save data to Words table then return a status message 
#test curl -X POST http://127.0.0.1:5000/add/popup -d '{"word":"tangerine"}'  -H "Content-Type: application/json"
@app.route("/add/popup", methods=['POST']) 
def add_from_popup(): #add word from chrome extension popup
    data = request.get_json()
    word = data.get("word")

    try:
        speech, definition, example = get_dictionary_info(word)
        new_word = Word(word,speech,definition,example)
        new_word.insert()
        words = Word.display()
        print(words)
        return jsonify({"status":"success"})
    except WordNotFoundError as e:
        return jsonify({"status":"fail"})


#pre: words table is initialized
#post:return a word_list contains all the data in the Words' table
#test curl -X GET http://127.0.0.1:5000/display -H "Content-Type: application/json"
@app.route("/display/words", methods=['GET'])
def display():  
    
    # words = session.query(Words).all() 
    words = Word.display()
    print(words)
    word_list = []

    for word in words:
        word_dict = {}
        word_dict["word"] = word.word
        word_dict["speech"] = word.speech
        word_dict["definition"] = word.definition
        word_dict["example"] = word.example
        word_list.append(word_dict)
    print(word_list)
    return jsonify({"result":word_list})


#test  curl -X POST http://127.0.0.1:5000/uodate/card -d '{"word":"cherry","speech":"noun","definition":"fruit","example":"none"}'  -H "Content-Type: application/json"
@app.route("/update/card", methods=["POST"]) #modify it later
def update_card():
    data = request.get_json()
    word = data.get("word")
    speech = data.get("speech")
    definition = data.get("definition")
    example = data.get("example")

    word_update = session.query(Words).filter(Words.word==word).first()
    print(word_update)
    word_update.word = word
    word_update.speech = speech
    word_update.definition=definition
    word_update.example = example

    words = Word.display()
    print(words)

    return jsonify({"status":"success"})
    



