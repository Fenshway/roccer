from flask import Flask, render_template, request

app = Flask(__name__)


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/settings')
def settings():
    pass

@app.get('/post')
def post():
    return render_template('post.html')
