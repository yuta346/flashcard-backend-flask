from flask import Flask, request, jsonify
from flask_cors import CORS

from models.schema import Users, Words, Activities
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

    user = Users.find_user(username)
    if user is not None:
        return jsonify({"status":"fail", "message":"Account already exists"})

    Users.insert(username, email, password_hash, session_id, None)
    Users.display()

    return jsonify({"status":"success", "username":username, "session_id":session_id})


#pre: user has signed up and user's data exist in the database
#post: return success if verified
#test curl -X POST http://127.0.0.1:5000/api/login -d '{"username":"u4", "password":"44444"}'  -H "Content-Type: application/json"
@app.route("/api/login", methods=["POST"])
def login():
    
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    user = Users.find_user(username)

    if user is None:
        return jsonify({"status": "fail", "message":"account does not exist"})

    password_hash = user.password_hash
    auth = Users.verify_password(password, password_hash)
    if auth == True and username == user.username:
        session_id = str(Users.generate_session_id())
        user.session_id = session_id
        session.commit()
        pending_length = len(Words.get_pending_words(user.id))
        return jsonify({"status":"success", "username":user.username, "session_id":user.session_id, "pending_length":pending_length})
    return jsonify({"status":"fail"})

@app.route("/api/popup/login", methods=["POST"])
def popup_login():
    
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = session.query(Users).filter(Users.username==username).one()
    if user is None:
        return jsonify({"status": "fail", "message":"account does not exist"})
    password_hash = user.password_hash
    result = Users.verify_password(password, password_hash)
    if result == True and username == user.username:
        session_id = str(Users.generate_session_id())
        user.session_id_extension = session_id
        session.commit()
        print(user)
        return jsonify({"status":"success", "username":user.username, "session_id":user.session_id_extension})


@app.route("/api/popup/logout", methods=["POST"])
def popup_logout():
    data = request.get_json()
    print(data)
    session_id = data.get("session_id")
    user = Users.session_extension_authenticate(session_id)
    if user is None:
        return jsonify({"status":"fail"})
    user.session_id_extension = None
    session.commit()
    Users.display()
    return jsonify({"status":"success"})




#pre: session_id exists
#post: clear the session_id and return a status code and message
#test curl -X POST http://127.0.0.1:5000/api/logout -d '{"session_id":"06b76efe-19ab-4662-b1af-6b57aa0cab90"}'  -H "Content-Type: application/json"
@app.route("/api/logout", methods=["POST"])
def logout():

    data = request.get_json()
    session_id = data.get("session_id")
    user = Users.session_authenticate(session_id)
    if user is None:
        return jsonify({"status":"fail"})
    user.session_id = None
    session.commit()
    Users.display()
    return jsonify({"status":"success"})



#pre: Word's table is initialized
#post: add user's custom data the database and return a status message 
#test curl -X POST http://127.0.0.1:5000/api/add_word -d '{"word":"banana","speech":"noun","definition":"fruit","example":"none"}'  -H "Content-Type: application/json"
@app.route("/api/add/word/dictionary", methods=["POST"])  #create user's custom card fix it later
def add_word():

    data = request.get_json()
    word_info_list = data.get("word_info_list")
    radioValue = data.get("radioValue")
    session_id = data.get("session_id")
    user = Users.session_authenticate(session_id)
    if user is None:
        return jsonify({"status":"fail", "message":"authentication failed"})

    try:
        for word_info in word_info_list:
            saved_words = session.query(Words).filter(Words.user_id == user.id).filter(Words.short_definition == word_info["short_definition"]).all()
            if not saved_words:
                if word_info["short_definition"]== radioValue:
                    Words.insert(word_info["word"], word_info["definition"], word_info["short_definition"], word_info["example"], True, False, user.id)
                else:
                    Words.insert(word_info["word"], word_info["definition"], word_info["short_definition"], word_info["example"], False, False, user.id)
            else:
                return jsonify({"status":"fail", "message":"Word with the same meaning alrady exists"})
        # print(session.query(Words).filter(Words.user_id == user.id).all())
        return jsonify({"status":"success"})
    except WordNotFoundError as e:
        return jsonify({"status":"fail", "message": "cannot find a word"})


@app.route("/api/add/word/custom", methods=["POST"])
def add_custom_word():
    data = request.get_json()
    user_input = data.get("userInput")
    session_id = data.get("session_id")
    user = Users.session_authenticate(session_id)

    if user is None:
        return jsonify({"status":"fail", "message":"authentication failed"})

    saved_words = session.query(Words).filter(Words.user_id == user.id).filter(Words.definition == user_input["definition"]).all()
    if not saved_words:
        Words.insert(user_input["word"], user_input["definition"], user_input["definition"], user_input["example"], True, False, user.id)
    else:
        return jsonify({"status":"fail", "message":"Word with the same meaning alrady exists"})
    return jsonify({"status":"success"})
    



@app.route("/api/serach/definitions", methods=["POST"])
def search_definitions():
    data = request.get_json()
    word = data.get("word")
    session_id = data.get("session_id")
    user = Users.session_authenticate(session_id)
    if user is None:
        return jsonify({"status":"fail", "message":"user does not exists"})

    try:
        word_info_list = get_dictionary_info(word)
        return jsonify({"status":"success", "definition_choice": word_info_list})
    except WordNotFoundError as e:
        return jsonify({"status":"fail", "message": "cannot find a word"})




#pre: Word's table is initialized
#post: call api and save data to Words table then return a status message 
#test curl -X POST http://127.0.0.1:5000/api/add/popup -d '{"word":"tangerine"}'  -H "Content-Type: application/json"
@app.route("/api/add/popup", methods=['POST'])   #
def add_from_popup(): #add word from chrome extension popup
    data = request.get_json()
    word = data.get("word")
    session_id_extension = data.get("session_id")
    user = Users.session_extension_authenticate(session_id_extension)

    try:
        word_info_list = get_dictionary_info(word)
        for word_info in word_info_list:
            Words.insert(word_info["word"], word_info["definition"], word_info["short_definition"], word_info["example"], False, True, user.id)
        return jsonify({"status":"success","definition_choice": word_info_list})
    except WordNotFoundError as e:
        return jsonify({"status":"fail"})


@app.route("/api/display/all/flashcards", methods=["POST"])
def display_all_flashcards():
    data = request.get_json()
    session_id = data.get("session_id")
    user = Users.session_authenticate(session_id)
    if user is None:
        return jsonify({"status":"fail"})
    all_flashcards = Words.get_all_words(user.id)
    print(all_flashcards)
    return jsonify({"all_flashcards":all_flashcards})


#pre: Words table is initialized and cards exist
#post:return a word_list and isMastered_dict for quiz and study
@app.route("/api/display/generated/flashcards", methods=['POST'])
def dislpay_generated_flashcards():  
    data = request.get_json()
    session_id = data.get("session_id")
    num_cards = data.get("num_cards")
    user = Users.session_authenticate(session_id)
    if user is None:
        return jsonify({"status":"fail"})
    word_list, isMastered_dict = Words.generate_flashcards(user.id, num_cards)  
    # print(word_list)
    # print(isMastered_dict)  
    return jsonify({"word_list":word_list, "isMastered_dict": isMastered_dict})



@app.route("/api/display/words/pending", methods=['POST'])
def display_pending_words():  
    data = request.get_json()
    session_id = data.get("session_id")
    user = Users.session_authenticate(session_id)
    if user is None:
        return jsonify({"status":"fail", "message":"user does not exist"})
    pending_words = Words.get_pending_words(user.id)
    return jsonify({"pending_words":pending_words})



@app.route("/api/update/pending", methods=["POST"])
def update_pending_word():
    data = request.get_json()
    session_id = data.get("session_id")
    selected_words = data.get("selected")
    pending_status = data.get("pending_status")
    if not selected_words:
        return jsonify({"status":"fail", "message":"no word selected"})
    user = Users.session_authenticate(session_id)
    if user is None:
        return jsonify({"status":"fail", "message":"user does not exist"})
    Words.update_pending_words(user.id, selected_words, pending_status)
    pending_words = Words.get_pending_words(user.id)
    return jsonify({"status":"success", "pending_words":pending_words})


#test  curl -X POST http://127.0.0.1:5000/uodate/card -d '{"word":"cherry","speech":"noun","definition":"fruit","example":"none"}'  -H "Content-Type: application/json"
@app.route("/api/update_flashcard", methods=["POST"]) #modify it later
def update_flashcard():
    data = request.get_json()
    word = data.get("word")
    speech = data.get("speech")
    definition = data.get("definition")
    short_definition = data.get("short_definition")
    example = data.get("example")

    word_update = session.query(Words).filter(Words.word==word).one()
    word_update.word = word
    word_update.speech = speech
    word_update.definition=definition
    word_update.example = example
    words = Words.display()
    print(words)

    return jsonify({"status":"success"})


#pre: Words table is initialized and word exists
#post: return rondomly picked words, multiple choice with answer key 
#test: curl -X POST http://127.0.0.1:5000/api/generate_flashcards -d '{"session_id":"f3a53399-3e0a-45ad-98ed-6e663d370667", "num_cards":"0"}'  -H "Content-Type: application/json"
# @app.route("/api/generate_flashcards", methods=["POST"]) #??
# def generate_flashcards():
   
#     data = request.get_json()
#     session_id = data.get("session_id")
#     num_cards = int(data.get("num_cards"))
#     user = Users.session_authenticate(session_id)

#     if user is None:
#         return jsonify({"status":"fail"})
#     word_list = Words.generate_ramdom_cards(user.id, num_cards)
#     return jsonify({"result":word_list})



# @app.route("/api/display_performances", methods=["POST"])
# def display_performance():
#     pass


@app.route("/api/update_activitiy", methods=["POST"])
def update_activity():
    data = request.get_json()
    session_id = data.get("session_id")
    isMastered_dict  = data.get("isMastered")
    print(isMastered_dict)
    user = Users.session_authenticate(session_id)
    if user is None:
        return jsonify({"status":"fail", "message":"user does not exist"})

    Activities.update_activity(user.id, isMastered_dict)
    return jsonify({"status":"success"})



@app.route("/api/get_activity", methods=["POST"])
def get_activity():
    data = request.get_json()
    session_id = data.get("session_id")
    user = Users.session_authenticate(session_id)
    if user is None:
        return jsonify({"status":"fail", "message":"user does not exist"})
    user_activities, activities_time_series, num_mastered = Activities.get_activities(user.id)
    return jsonify({"activities": user_activities, "numMastered": num_mastered, "time_series":activities_time_series})

