from types import ClassMethodDescriptorType
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from models.setting import Base, session, engine, relationship
# from setting import Base, session, engine, relationship
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
import uuid
import random
from sqlalchemy import func


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    session_id = Column(String)
    words = relationship("Words", lazy=True)

    def __repr__(self):
        return "<User(id='%s',username='%s', email='%s', password_hash='%s', self.session_id='%s')>" % (
                             self.id, self.username, self.email, self.password_hash, self.session_id)
    
    @classmethod
    def insert(cls, username, email, password_hash, session_id):
        new_user = Users()
        new_user.username = username
        new_user.email = email
        new_user.password_hash = password_hash
        new_user.session_id = session_id
        session.add(new_user)
        session.commit()

    #for testing purpose
    @classmethod
    def display(cls):
        all_users = session.query(Users).all() 
        print(all_users)
        return all_users
    
    @classmethod
    def session_authenticate():
        pass
    
    @staticmethod
    def hash_password(password):
        password_hash = pwd_context.encrypt(password)
        return password_hash

    @staticmethod
    def verify_password(password, password_hash):
        return pwd_context.verify(password, password_hash)


    @staticmethod
    def generate_session_id():
        return uuid.uuid4()
    


class Words(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(String)
    speech = Column(String)
    definition = Column(String)
    example = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    performances = relationship("Performances", lazy=True)

    def __repr__(self):
        return "<Word(id='%s',word='%s', speech='%s', definition='%s', example='%s', user_id='%s')>" % (
                             self.id, self.word, self.speech, self.definition, self.example, self.user_id)
    @classmethod
    def insert(cls, word, speech, definition, example, user_id):
        new_word = Words()
        new_word.word = word
        new_word.speech = speech
        new_word.definition = definition
        new_word.example = example
        new_word.user_id = user_id
        session.add(new_word)
        session.commit()

    @classmethod
    def display(cls):
        all_words = session.query(Words).all() 
        print(all_words)
        return all_words
    
    @classmethod
    def generate_ramdom_cards(cls, user_id, num_cards):

        num_choices = num_cards * 2

        if num_cards < 0:
            num_cards = 0

        words = session.query(Words).filter(Words.user_id == user_id).order_by(func.random()).limit(num_cards).all()
        word_list = []

        if len(words) < num_cards:
            num_cards = len(words)
        
        for word in words:
            word_dict = {}
            word_dict["word"] = word.word
            word_dict["speech"] = word.speech
            word_dict["definition"] = word.definition
            word_dict["example"] = word.example
            word_dict["choices"] = Words.generate_choices(word.definition, user_id, num_choices)
            word_list.append(word_dict)
        return word_list
    
    #generate_choice
    @classmethod
    def generate_choices(cls, definition, user_id, num_choices):

        multiple_choices = [definition]
        words = session.query(Words).filter(Words.user_id == user_id).order_by(func.random()).limit(num_choices).all()
        for word in words:
            if word.definition !=  definition and word.definition not in multiple_choices:
                multiple_choices.append(word.definition)
        return multiple_choices


class Performances(Base):
    __tablename__ = 'performances'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    isLearned = Column(Boolean)
    numAttempt = Column(Boolean)
    word_id = Column(Integer, ForeignKey('words.id'))

    def __repr__(self):
        return "<Performance(id='%s',date='%s',isLearned='%s', numAttempt='%s',word_id='%s')>" % (
                             self.id, self.isLearned, self.word_id)

    @classmethod
    def display(cls):
        all_performances = session.query(Words).all() 
        print(all_performances)
        return all_performances

    
                    
# Base.metadata.create_all(engine)

#language column 


# w1 = Words()
# w1.word = "apple"
# w1.speech = "noun"
# session.add(w1)
# session.commit()

# w2 = Word("orange","noun")
# w2.insert()
# session.add(w2)
# session.commit()

# words = session.query(Words).all()
# print(words)

