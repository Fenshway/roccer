from src.models import User_account, db

class UserRepository:

    def create_account(self, first_name, last_name, username, user_password):
        new_user = User_account(first_name=first_name, last_name=last_name, username=username, user_password=user_password)
        db.session.add(new_user)
        db.session.commit()
        return new_user 

user_repository_singleton = UserRepository()