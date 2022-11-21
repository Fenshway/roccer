from flask import Flask, render_template, request, redirect, flash, session
import os
from dotenv import load_dotenv
from src.models import db, User_account
from flask_bcrypt import Bcrypt
from src.repositories.user_account_repository import user_repository_singleton

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.secret_key = os.getenv('APP_SECRET_KEY')

db.init_app(app)

bcrypt = Bcrypt(app)

@app.get('/')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/profile/settings')
def settings():
  return render_template('settings.html')


@app.get('/post')
def post():
    return render_template('post.html')


@app.get('/create_post')
def create_post():
    return render_template('create_post.html')

@app.get('/register_form')
def register_form():
    return render_template('register.html')

@app.post('/register')
def register():
    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if (password != password2):
        flash('Passwords do not match. Please try again.')
        return render_template('/register_form')

    existing_user = User_account.query.filter_by(username=username).first()
    if existing_user:
        flash('Username already taken.')
        return redirect('/register_form')

    hashed_bytes = bcrypt.generate_password_hash(password, int(os.getenv('BCRYPT_ROUNDS')))
    hashed_password = hashed_bytes.decode('utf-8')

    new_user = user_repository_singleton.create_account(first_name, last_name, username, hashed_password)
    flash('Account created successfully.')
    return redirect('/profile')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.post('/login')
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    existing_user = User_account.query.filter_by(username=username).first()
    if not existing_user:
        flash('Error logging in. Please try again.')
        return redirect('/login_page')

    if not bcrypt.check_password_hash(existing_user.user_password, password):
        flash('Error logging in. Please try again.')
        return redirect('/login_page')

    session['user'] = {
        'user_account_id': existing_user.user_account_id
    }
    flash('Logged in. Remove this flash code before deployement')
    return redirect('/')

@app.post('/logout')
def logout():
    session.pop('user')
    return redirect('/')

#@app.post('/delete')
#def delete():
#    user_to_delete = User_account.query.filter_by()