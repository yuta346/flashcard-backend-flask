from models.schema import Words
from models.setting import session

class Word:
    def __init__(self, word, speech, definition, example, user_id):
        self.word = word
        self.speech = speech
        self.definition = definition
        self.example = example
        self.user_id = user_id

    def __repr__(self):
        return f"<{self.word}, {self.speech}, {self.definition}, {self.example}, {self.user_id}>"
    
    def insert(self):
        new_word = Words()
        new_word.word = self.word
        new_word.speech = self.speech
        new_word.definition = self.definition
        new_word.example = self.example
        new_word.user_id = self.user_id
        session.add(new_word)
        session.commit()
        print("commited!!!!")
    
    @classmethod
    def display(self):
        all_words = session.query(Words).all() 
        return all_words
     
        



# w = Word("peach","noun")
# w.insert()

# words = session.query(Words).all()
# print(words)