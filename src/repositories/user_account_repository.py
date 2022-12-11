from src.models import User_account
from app import db

class UserRepository:
    def get_all_users(self):
        users = User_account.query.all()
        return users

    def get_user_by_id(self, user_id):
        return User_account.query.get(user_id)

    def create_user(self, first_name, last_name, username, password):
        new_user = User_account(first_name, last_name, username, password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

user_repository_singleton = UserRepository()
