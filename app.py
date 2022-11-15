from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from src.models import db, User_account

load_dotenv()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)

@app.get('/')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/profile/settings')
def settings():

    return render_template('settings.html')

@app.get('/create_post')
def create_post():
    return render_template('create_post.html')