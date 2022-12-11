from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from src.models import db, User_account, User_comment, Post
from flask_bcrypt import Bcrypt
from src.repositories.user_account_repository import user_repository_singleton
from src.repositories.post_repository import post_repository_singleton
from sqlalchemy import update


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

    if 'user' in session:
        username=session['user']['username']
        return render_template('index.html', posts = all_posts, username=username)
   
    return render_template('index.html', posts = all_posts)



@app.get('/profile')
def profile():
    if 'user' not in session:
        return redirect('/')

    first_name=session['user']['first_name']
    last_name=session['user']['last_name']
    username=session['user']['username']
    profile_path=session['user']['profile_path']
    
    return render_template('profile.html', first_name=first_name, last_name=last_name, username=username, profile_path=profile_path)

@app.post('/profile')
def update_profile_pic():
    # ---------------INCOMPLETE. Will finish -Ivan--------------

    
    # if 'profile' not in request.files:
    #     return redirect('/profile')

    # profile_picture = request.files['profile']

    # if profile_picture.filename == '':
    #     return redirect('/profile')
    
    # if profile_picture.filename.rsplit('.', 1)[1].lower() not in ['jpg', 'jpeg', 'gif', 'png']:
    #     return redirect('/profile')

    # safe_filename = secure_filename(profile_picture.filename)

    # profile_picture.save(os.path.join('static/assets', 'profile-pics', safe_filename))

    
    return render_template('profile.html')


@app.get('/profile/settings')
def settings():
    if 'user' not in session:
        return render_template('/')

    first_name=session['user']['first_name']
    last_name=session['user']['last_name']
    username=session['user']['username']
    profile_path=session['user']['profile_path']

    return render_template('settings.html', first_name=first_name, last_name=last_name, username=username, profile_path=profile_path)


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
def get_create_post():
    if 'user' not in session:
        return redirect('/login_page')

    username=session['user']['username']
    return render_template('create_post.html', username=username)

@app.post('/create_post')
def create_post():
    title = request.form.get('title')
    text = request.form.get('text')

    # print(f'Title: {title}')
    # print(f'Text: {text}')
    # print(f'Image: {image}')
    # print(f'Video: {video}')
    # print(f'Link: {url}')
    # print(f'Embed VIdeo: {embed_video}')

    

    if title and text:
        post_repository_singleton.create_post_text(title, text, session['user']['user_account_id'])

    elif title and 'image' in request.files:
        image = request.files['image']

        if image.filename == '':
            return redirect('/create_post')
    
        if image.filename.rsplit('.', 1)[1].lower() not in ['jpg', 'jpeg', 'gif', 'png']:
            return redirect('/create_post')
        
        safe_image_file = secure_filename(image.filename)
        image.save(os.path.join('static/assets', 'post_images', safe_image_file))

        post_repository_singleton.create_post_stored_image(title, safe_image_file, session['user']['user_account_id'])

    elif title and request.form.get('link'):
        url = request.form.get('link')
        embed_video = url.replace("watch?v=", "embed/")

        post_repository_singleton.create_post_embedded_video(title, embed_video, session['user']['user_account_id'])

    elif title and 'video' in request.files:
        video = request.files['video']

        if video.filename == '':
            return redirect('/create_post')
    
        if video.filename.rsplit('.', 1)[1].lower() not in ['mp4', 'ogg', 'webm']:
            return redirect('/create_post')

        safe_video_file = secure_filename(video.filename)
        video.save(os.path.join('static/assets', 'post_videos', safe_video_file))
        
        post_repository_singleton.create_post_stored_video(title, safe_video_file, session['user']['user_account_id'])
    else:
        return redirect('/create_post')

    return redirect('/')
    

@app.get('/register_form')
def register_form():
    return render_template('register.html')

@app.post('/register')
def register():
    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if (password != password2):
        flash('Passwords do not match. Please try again.')
        return redirect('/register_form')

    existing_user = User_account.query.filter_by(username=username).first()
    if existing_user:
        flash('Username already taken.')
        return redirect('/register_form')

    hashed_bytes = bcrypt.generate_password_hash(password, int(os.getenv('BCRYPT_ROUNDS')))
    hashed_password = hashed_bytes.decode('utf-8')

    if 'profile' not in request.files:
        flash('Error processing file. Please try again')
        return redirect('/register_form')

    profile_picture = request.files['profile']

    if profile_picture.filename == '':
        flash('Error processing file. Please try again')
        return redirect('/register_form')
    
    if profile_picture.filename.rsplit('.', 1)[1].lower() not in ['jpg', 'jpeg', 'gif', 'png']:
        flash('Please use one of the approved file formats (jpg, jpeg, gif, png)')
        return redirect('/register_form')

    safe_filename = secure_filename(f'{username}-{profile_picture.filename}')

    profile_picture.save(os.path.join('static/assets', 'profile-pics', safe_filename))

    user_repository_singleton.create_user(first_name, last_name, username, hashed_password, safe_filename)
    existing_user = User_account.query.filter_by(username=username).first()
    flash('Account created successfully.')
    session['user'] = {
        'user_account_id': existing_user.user_account_id,
        'first_name': existing_user.first_name,
        'last_name': existing_user.last_name,
        'username': existing_user.username,
        'user_account_id': existing_user.user_account_id,
        'profile_path': existing_user.profile_path,
    }
    return redirect('/profile')

@app.get('/login_page')
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
        'user_account_id': existing_user.user_account_id,
        'first_name': existing_user.first_name,
        'last_name': existing_user.last_name,
        'username': existing_user.username,
        'user_account_id': existing_user.user_account_id,
        'profile_path': existing_user.profile_path,
    }
    return redirect('/')

@app.post('/logout')
def logout():
    if 'user' not in session:
        return redirect('/')

    session.pop('user')
    return redirect('/')


@app.post('/delete')
def delete():
    user_to_delete = User_account.query.get(session['user']['user_account_id'])
    db.session.delete(user_to_delete)
    db.session.commit()
    return render_template('index.html')
    #user_to_delete = User_account.query.filter_by()

@app.get('/search')
def search():
    topic = request.args.get('topic')
    searched_posts = post_repository_singleton.search_post(topic)

    if 'user' in session:
        username=session['user']['username']
        return render_template('index.html', posts = searched_posts, username=username)
    
    return render_template('index.html', posts = searched_posts)

@app.get('/update_user_form')
def update_user_form():

    if 'user' not in session:
        return redirect('/')
    first_name=session['user']['first_name']
    last_name=session['user']['last_name']
    username=session['user']['username']
    return render_template('update_user.html', first_name=first_name, last_name=last_name, username=username)

@app.post('/update_user')
def update_user():
    if 'user' not in session:
        return redirect('/login')

    user_id=session['user']['user_account_id']
    first_name=session['user']['first_name']
    last_name=session['user']['last_name']
    username=session['user']['username']
    
    password = request.form.get('password')

    existing_user = User_account.query.filter_by(user_account_id=user_id).first()
    if not bcrypt.check_password_hash(existing_user.user_password, password):
        flash('Incorrect Password')
        return redirect('/update_user_form')

    new_username = request.form.get('username')
    if username != new_username:
        existing_user = User_account.query.filter_by(username=new_username).first()
        if existing_user is not None:
            flash('Username already taken.')
            return redirect('/update_user_form')
        user_repository_singleton.update_username(user_id, new_username)

    new_first_name = request.form.get('firstname')
    if first_name != new_first_name:
        user_repository_singleton.update_user_first_name(user_id, new_first_name)

    new_last_name = request.form.get('lastname')
    if last_name != new_last_name:
        user_repository_singleton.update_user_last_name(user_id, new_last_name)

    new_pw1 = request.form.get('new_pw')
    new_pw2 = request.form.get('new_pw2')

    if new_pw1 != '' and new_pw2 != '':
        if new_pw1 != new_pw2:
            flash('New passwords do not match')
            return redirect('/update_user_form')
        else:
            hashed_bytes = bcrypt.generate_password_hash(new_pw1, int(os.getenv('BCRYPT_ROUNDS')))
            hashed_password = hashed_bytes.decode('utf-8')
            user_repository_singleton.update_password(user_id, hashed_password)

    session.pop('user')

    existing_user = User_account.query.filter_by(user_account_id=user_id).first()
    session['user'] = {
        'user_account_id': existing_user.user_account_id,
        'first_name': existing_user.first_name,
        'last_name': existing_user.last_name,
        'username': existing_user.username,
        'user_account_id': existing_user.user_account_id,
        'profile_path': existing_user.profile_path,
    }
    
    return redirect('/profile/settings')




