from flask import Flask, redirect, render_template, request
import os
from dotenv import load_dotenv
from src.models import db
from src.repositories.user_account_repository import user_repository_singleton
from src.repositories.post_repository import post_repository_singleton

load_dotenv()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        postID = request.form.get("post")
        vote = request.form.get("vote")
        ##TODO update vote status on server
        print(postID, vote)
    all_posts = post_repository_singleton.get_all_posts()
    return render_template('index.html', posts = all_posts)



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
