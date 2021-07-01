from models.schema import Users
from models.setting import session


class User:

    def __init__(self, username, email, hashed_password, session_id=None, pk=None):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.session_id = session_id
        self.pk = pk
    

    def __repr__(self):
        return f"<{self.username}, {self.email}, {self.hashed_password}, {self.session_id}, {self.pk}>"
    
    def insert(self):
        new_user = Users()
        new_user.username = self.username
        new_user.email = self.email
        new_user.password = self.hashed_password
        new_user.session_id = self.session_id
        session.add(new_user)
        session.commit()
        print("commited!!!!")
    
    @classmethod
    def display(self):
        all_users = session.query(Users).all() 
        print(all_users)
        return all_users