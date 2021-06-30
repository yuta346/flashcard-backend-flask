from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Word(Base):

    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    word = Column(String, unique=True)
    speech = Column(String)
    definition = Column(String)
    example = Column(String)

    def __repr__(self):
       return "<Words(id='%s', word='%s', speech='%s', definitiion='%s', 'example')>" % (self.id, self.word, self.speech, self.definition, self.example)


if __name__ == "__main__":
    engine = create_engine('sqlite:///flashcard.db', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()