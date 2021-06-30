import sqlite3

class Word:

    dbpath = "../data/flashcard.db"
    tablename = "words"

    def __init__(self, word, speech, definition, exapmle, pk=None):
        self.word = word
        self.speech = speech
        self.definition = definition
        self.example = exapmle
        self.pk = pk
    
    def insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            cursor = conn.cursor()
            sql = f"""INSERT INTO {self.tablename} (word, speech, definition, example)
                      VALUES (?,?,?,?)
                   """
            cursor.execute(sql, (self.word, self.speech, self.definition, self.example))

    @classmethod
    def show_words(cls):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            sql = f"""SELECT *
                      FROM {cls.tablename}
                   """
            cursor.execute(sql)
            return cursor.fetchall()
    




# if __name__ == "__main__":
    # w1 = Word("apple","noun","fruit","none")
    # w1.insert()
    # w2 = Word("orange","noun","orange fruit","none")
    # w2.insert()
# print(Word.show_words())