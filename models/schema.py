from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from models.setting import Base, session, engine, relationship
# from setting import Base, session, engine, relationship
from datetime import datetime


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    session_id = Column(String)
    words = relationship("Words", lazy=True)

    def __repr__(self):
        return "<User(id='%s',username='%s', email='%s', password='%s')>" % (
                             self.id, self.username, self.email, self.password)

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

