from passlib.apps import custom_app_context as pwd_context
import uuid
from models.schema import Users
from models.setting import session



class User:

    def __init__(self, username, email, password_hash, session_id, pk=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.session_id = session_id
        self.pk = pk
    

    def __repr__(self):
        return f"<{self.username}, {self.email}, {self.password_hash}, {self.session_id}, {self.pk}>"
    
    def insert(self):
        new_user = Users()
        new_user.username = self.username
        new_user.email = self.email
        new_user.password = self.password_hash
        new_user.session_id = self.session_id
        session.add(new_user)
        session.commit()


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
    def session_authenticate():
        pass

    
    @classmethod
    def display(self):
        all_users = session.query(Users).all() 
        print(all_users)
        return all_users