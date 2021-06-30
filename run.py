from routes.routes import app
from models.word import Word

Word.dbpath = "data/flashcard.db"

if __name__ == "__main__":
    app.run(debug=True)