from flask import Flask, request, jsonify
from flask_cors import CORS

from models.schema import Users, Words
from models.setting import session
from models.util import get_dictionary_info, Error, WordNotFoundError



app = Flask(__name__)
CORS(app)

#pre: Users table is initialized
#post: add new user's info to the table and return a message
#test curl -X POST http://127.0.0.1:5000/api/signup -d '{"username":"u3","email":"u3@gmail.com","password":"33333"}'  -H "Content-Type: application/json"
@app.route("/api/signup", methods=["POST"])  #modify password and session 
def signup():

    data = request.get_json()
    print(data)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    password_hash = Users.hash_password(password)
    session_id = str(Users.generate_session_id())

    if session.query(Users).filter(Users.username==username).first() is not None:
        return jsonify({"status":"fail", "message":"Account already exists"})

    Users.insert(username, email, password_hash, session_id)
    Users.display()

    return jsonify({"status":"success"})


#pre: user has signed up and user's data exist in the database
#post: return success if verified
#test curl -X POST http://127.0.0.1:5000/api/login -d '{"username":"u4", "password":"44444"}'  -H "Content-Type: application/json"
@app.route("/api/login", methods=["POST"])
def login():
    
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    session_id = str(Users.generate_session_id())
    
    user = session.query(Users).filter(Users.username==username).one()
    if user is None:
        return jsonify({"status": "fail", "message":"account does not exist"})

    Users.display()

    password_hash = user.password
    result = Users.verify_password(password, password_hash)
    if result == True and username == user.username:
        #update session_id in db
        user.session_id = session_id
        session.commit()
        Users.display()
        return jsonify({"status":"success", "username":user.username, "session_id":user.session_id})
    return jsonify({"status":"fail"})


#pre: session_id exists
#post: clear the session_id and return a status code and message
#test curl -X POST http://127.0.0.1:5000/api/logout -d '{"session_id":"06b76efe-19ab-4662-b1af-6b57aa0cab90"}'  -H "Content-Type: application/json"
@app.route("/api/logout", methods=["POST"])
def logout():

    data = request.get_json()
    session_id = data.get("session_id")
    user = session.query(Users).filter(Users.session_id == session_id).one()

    if user is None:
        return jsonify({"status":"fail"})

    user.session_id = None
    session.commit()
    Users.display()
    return jsonify({"status":"success"})



@app.route("/api/update", methods=["POST"])
def update():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    pass

#curl -X GET http://127.0.0.1:5000/api/display_users -H "Content-Type: application/json"
@app.route("/api/display_users", methods=["GET"])
def display_users():
    Users.display()
    return jsonify({"status":"success"})
    



#pre: Word's table is initialized
#post: add user's custom data the database and return a status message 
#test curl -X POST http://127.0.0.1:5000/api/add_word -d '{"word":"banana","speech":"noun","definition":"fruit","example":"none"}'  -H "Content-Type: application/json"
@app.route("/api/add_word", methods=["POST"])  #create user's custom card fix it later
def add_word():

    data = request.get_json()
    word = data.get("word")
    speech = data.get("speech")
    definition = data.get("definition")
    example = data.get("example")
    user = session.query(Users).filter(Users.username=='u4').one()  #get username or session_id from react
    user_id = user.id

    try:
        speech, definition, example = get_dictionary_info(word)
        Words.insert(word, speech, definition, example, user_id)
        Words.display() 
        return jsonify({"status":"success"})
    except WordNotFoundError as e:
        return jsonify({"status":"fail"})


#pre: Word's table is initialized
#post: call api and save data to Words table then return a status message 
#test curl -X POST http://127.0.0.1:5000/api/add_popup -d '{"word":"tangerine"}'  -H "Content-Type: application/json"
@app.route("/api/add_popup", methods=['POST'])   #how to authenticate?
def add_from_popup(): #add word from chrome extension popup
    data = request.get_json()
    word = data.get("word")

    try:
        speech, definition, example = get_dictionary_info(word)
        Words.insert(word, speech, definition, example)
        Words.display()
        return jsonify({"status":"success"})
    except WordNotFoundError as e:
        return jsonify({"status":"fail"})


#pre: Words table is initialized and cards exist
#post:return a word_list contains all the data in the Words' table
#test curl -X GET http://127.0.0.1:5000/api/display_all -H "Content-Type: application/json"
@app.route("/api/display_all_flashcards", methods=['GET'])
def display_all_flashcards():  
    
    words = Words.display()
    word_list = []

    for word in words:
        word_dict = {}
        word_dict["word"] = word.word
        word_dict["speech"] = word.speech
        word_dict["definition"] = word.definition
        word_dict["example"] = word.example
        word_list.append(word_dict)
    return jsonify({"result":word_list})


#test  curl -X POST http://127.0.0.1:5000/uodate/card -d '{"word":"cherry","speech":"noun","definition":"fruit","example":"none"}'  -H "Content-Type: application/json"
@app.route("/api/update_flashcard", methods=["POST"]) #modify it later
def update_flashcard():
    data = request.get_json()
    word = data.get("word")
    speech = data.get("speech")
    definition = data.get("definition")
    example = data.get("example")

    word_update = session.query(Words).filter(Words.word==word).one()
    print(word_update)
    word_update.word = word
    word_update.speech = speech
    word_update.definition=definition
    word_update.example = example

    words = Words.display()
    print(words)

    return jsonify({"status":"success"})


#pre: Words table is initialized and word exists
#post: return rondomly picked words, multiple choice with answer key 
#test: curl -X POST http://127.0.0.1:5000/api/generate_flashcards -d '{"session_id":"3d4abeec-097a-4931-80b6-d5d6d635ca7f", "num_cards":"0"}'  -H "Content-Type: application/json"
@app.route("/api/generate_flashcards", methods=["POST"])
def generate_flashcards():
    # word_list = Words.generate_ramdom_cards()
    # print(word_list)
    # return jsonify({"status":"success"})



    data = request.get_json()
    session_id = data.get("session_id")
    num_cards = int(data.get("num_cards"))
    user = session.query(Users).filter(Users.session_id == session_id).one()
    if user is None:
        return jsonify({"status":"fail"})
    user_id = user.id

    #generate__choices


    word_list = Words.generate_ramdom_cards(user_id, num_cards)
    # word_list = Words.generate_ramdom_cards(user_id)
    print(word_list)
    return jsonify({"result":word_list})





@app.route("/api/display_performances", methods=["POST"])
def display_performance():
    pass




