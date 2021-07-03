from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///models/flashcard.db', echo=True)  #use when run the app
# engine = create_engine('sqlite:///flashcard.db', echo=True) 
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

