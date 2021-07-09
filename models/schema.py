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
    word_id = relationship("Words", lazy=True)
    acviity_id = relationship("Activities", lazy=True)

    def __repr__(self):
        return "<User(id='%s',username='%s', email='%s', password_hash='%s', session_id='%s')>" % (
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
    
    @classmethod
    def session_authenticate(cls, session_id):
        user = session.query(Users).filter(Users.session_id==session_id).one() 
        if user:
            return user
        return None


    @classmethod
    def find_user(cls, username):
        try:
            user = session.query(Users).filter(Users.username==username).one() 
            return user
        except:
            return None

    


class Words(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(String)
    speech = Column(String)
    definition = Column(String)
    short_definition = Column(String)
    example = Column(String)
    pending = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id'))
    # activity_id = relationship("Activities", back_populates="words",lazy=True, uselist=False)
    activity_id = relationship("Activities",lazy=True, )
    # child = relationship("Child", back_populates="parent", uselist=False)

    def __repr__(self):
        return "<Word(id='%s',word='%s', definition='%s', short_definition='%s',example='%s', pending='%s', user_id='%s')>" % (
                             self.id, self.word, self.short_definition, self.definition, self.example, self.pending, self.user_id)
    @classmethod
    def insert(cls, word, definition, short_definition, example, pending, user_id):
        new_word = Words()
        new_word.word = word
        new_word.definition = definition
        new_word.short_definition = short_definition
        new_word.example = example
        new_word.pending = pending
        new_word.user_id = user_id
        session.add(new_word)
        session.commit()

    @classmethod
    def display_all_cards(cls, user_id):
        return session.query(Words).filter(Words.user_id == user_id).all()



    @classmethod
    def get_flashcards(cls, user_id,  num_cards=20):
        words = session.query(Words).filter(Words.user_id == user_id).filter(Words.pending==False).limit(num_cards).all()
        
        word_list = []
        temp = []
        num_choices = len(words)
        
        for word in words:
            if word.word not in temp:
                temp.append(word.word)
                word_dict = {}
                word_dict["word_id"] = word.id
                word_dict["word"] = word.word
                word_dict["definition"] = word.definition
                word_dict["short_definition"] = word.short_definition
                word_dict["example"] = word.example
                word_dict["choices"] = Words.generate_choices(word.short_definition, user_id)
                word_dict["pending"] = word.pending
                word_list.append(word_dict)
        isMastered_dict = Words.generate_isMastered_dict(word_list)
        return word_list, isMastered_dict

    @classmethod
    def generate_choices(cls, short_definition, user_id):

        multiple_choices = [short_definition]
        words = session.query(Words).filter(Words.user_id == user_id).filter(Words.pending==False).order_by(func.random()).all()
        for word in words:
            if len(multiple_choices) <= 3:
                if word.short_definition != short_definition and word.short_definition not in multiple_choices and word.short_definition is not None:
                    multiple_choices.append(word.short_definition)
        multiple_choices_shaffle = random.sample(multiple_choices, len(multiple_choices))
        return multiple_choices_shaffle
    
    @classmethod
    def generate_isMastered_dict(cls, word_list):
        isMastered_dict = {}
        for word in word_list:
            isMastered_dict[word["word"]] = [word["word_id"], False]
        return isMastered_dict


        


    # @classmethod
    # def generate_ramdom_cards(cls, user_id, num_cards=20):

    #     num_choices = num_cards * 3

    #     if num_cards < 0:
    #         num_cards = 0

    #     words = session.query(Words).filter(Words.user_id == user_id).filter(Words.pending == False).order_by(func.random()).limit(num_cards).all()
    #     print(words)
    #     word_list = []

    #     if len(words) < num_cards:
    #         num_cards = len(words)
        
    #     for word in words:
    #         word_dict = {}
    #         word_dict["word"] = word.word
    #         word_dict["speech"] = word.speech
    #         word_dict["definition"] = word.definition
    #         word_dict["short_definition"] = word.short_definition
    #         word_dict["example"] = word.example
    #         word_dict["choices"] = Words.generate_choices(word.short_definition, user_id, num_choices)
    #         word_dict["mastered"] = False
    #         word_list.append(word_dict)
    #     return word_list
    
    #generate_choice
    




class Activities(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    isMastered = Column(Boolean)
    numAttempt = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    word_id = Column(Integer, ForeignKey('words.id'))

    def __repr__(self):
        return "<Activity(id='%s',date='%s',isMastered='%s', numAttempt='%s',user_id='%s' ,word_id='%s')>" % (
                             self.id, self.date, self.isMastered, self.numAttempt, self.user_id, self.word_id)

    @classmethod
    def get_activities(cls, user_id):
        try:
            all_activities = session.query(Activities).filter(Activities.user_id == user_id).all() 
            return all_activities
        except:
            return None

    
    @classmethod
    def insert(cls, user_id, word_id, isMastered):
        new_activity = Activities()
        new_activity.user_id = user_id
        new_activity.word_id = word_id
        new_activity.isMastered = isMastered
        session.add(new_activity)
        session.commit()
    
    @classmethod
    def update_activity(cls, user_id, isMastered_dict):

        activities = Activities.get_activities(user_id)
        word_ids = []
        if activities:
            for activity in activities:
                word_ids.append(activity.word_id)
    
        for key, value in isMastered_dict.items():
            if activities is None or value[0] not in word_ids:
                if value[1] == True:
                    Activities.insert(user_id, value[0], True)
                else:
                    Activities.insert(user_id, value[0], False)
                break
            else:
                print("yes, exits")
                print(session.query(Activities).filter(Activities.user_id == user_id).filter(Activities.word_id == 1).one() )
                session.query(Activities).\
                        filter(Activities.user_id == user_id).\
                        filter(Activities.word_id == value[0]).\
                        update({Activities.isMastered: value[1]}, synchronize_session = False)
        
        print(Activities.get_activities(user_id))
 
    
                    
# Base.metadata.create_all(engine)
