from flask import Flask, render_template, request, redirect, flash, session
import os
from dotenv import load_dotenv
from src.models import db, User_account, User_comment, Post
from flask_bcrypt import Bcrypt
from src.repositories.user_account_repository import user_repository_singleton
from src.repositories.post_repository import post_repository_singleton


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.secret_key = os.getenv('APP_SECRET_KEY')

db.init_app(app)

bcrypt = Bcrypt(app)

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


@app.route('/post', methods=['POST', 'GET'])
def post():
    if request.method == 'POST':
        postID = request.form.get("post")
        vote = request.form.get("vote")
        ##TODO update vote status on server
        print(postID, vote)
    all_posts = post_repository_singleton.get_all_posts()
    text = request.form.get('text')
    return render_template('post.html', posts = all_posts, text=text)

# @app.route("/reply-comment/<parent_post_id>", methods=['POST'])
# ## TODO: Login needs to be required to comment
# def create_comment(parent_post_id):
#     text = request.form.get('text')
#     if not text:
#         flash('Empty Comment. Try again.', category='error')
#     else: 
#         post = Post.query.filter_by(post_id = parent_post_id)
#         if post:
#             comment = User_comment(comment_text=text, parent_post_id=parent_post_id)
#             db.session.add(comment)
#             db.session.commit()
#         else:
#             flash('Post does not exist.', category='error')
#     return redirect('/post')

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

    new_user = user_repository_singleton.create_user(first_name, last_name, username, hashed_password)
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

    if not bcrypt.check_password_hash(existing_user.password, password):
        flash('Error logging in. Please try again.')
        return redirect('/login_page')

    session['user'] = {
        'user_account_id': existing_user.user_account_id
    }
    flash('I will delete this message soon. You are logged in.')
    return redirect('/')

@app.post('/logout')
def logout():
    session.pop('user')
    return redirect('/')

#@app.post('/delete')
#def delete():
#    user_to_delete = User_account.query.filter_by()