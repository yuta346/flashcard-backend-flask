from types import ClassMethodDescriptorType
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from models.setting import Base, session, engine, relationship
# from setting import Base, session, engine, relationship
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
import uuid
import random


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    session_id = Column(String)
    words = relationship("Words", lazy=True)

    def __repr__(self):
        return "<User(id='%s',username='%s', email='%s', password='%s', self.session_id='%s')>" % (
                             self.id, self.username, self.email, self.password, self.session_id)
    
    @classmethod
    def insert(cls, username, email, password_hash, session_id):
        new_user = Users()
        new_user.username = username
        new_user.email = email
        new_user.password = password_hash
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
    # , ForeignKey('users.id')
    # performances = relationship("Performances", lazy=True)

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
    def generate_ramdom(cls, user_id):
        words = session.query(Words).filter(Words.user_id == user_id).all()
        word_list = []
        num_generated_words = len(words)

        if len(words) > 10:
            num_generated_words = 10
        
        for word in random.sample(words, num_generated_words):
            word_dict = {}
            word_dict["word"] = word.word
            word_dict["speech"] = word.speech
            word_dict["definition"] = word.definition
            word_dict["example"] = word.example
            word_list.append(word_dict)
        return word_list

# class Performances(Base):
#     __tablename__ = 'performances'
#     id = Column(Integer, primary_key=True)
#     isLearned = Column(Boolean)
#     date = Column(DateTime, default=datetime.utcnow)
#     word_id = Column(Integer, ForeignKey('words.id'))

#     def __repr__(self):
#         return "<Performance(id='%s',isLearned='%s', word_id='%s')>" % (
#                              self.id, self.isLearned, self.word_id)

    

    
                    
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

