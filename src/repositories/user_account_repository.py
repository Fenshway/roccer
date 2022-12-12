from src.models import User_account
from app import db

class UserRepository:
    def get_all_users(self):
        users = User_account.query.all()
        return users

    def get_user_by_id(self, user_id):
        return User_account.query.get(user_id)

    def create_user(self, first_name, last_name, username, password, profile_path):
        new_user = User_account(first_name, last_name, username, password, profile_path)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
    #def update_user()

    def update_username(self, user_id, username):
        update_user = User_account.query.get(user_id)
        update_user.username = username
        db.session.commit()

    def update_user_first_name(self, user_id, first_name):
        update_user = User_account.query.get(user_id)
        update_user.first_name = first_name
        db.session.commit()

    def update_user_last_name(self, user_id, last_name):
        update_user = User_account.query.get(user_id)
        update_user.last_name = last_name
        db.session.commit()
    
    def update_password(self, user_id, password):
        update_user = User_account.query.get(user_id)
        update_user.user_password = password
        db.session.commit()

user_repository_singleton = UserRepository()
