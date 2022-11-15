from flask import Flask, render_template, request

app = Flask(__name__)


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/settings')
def settings():
    pass

@app.route('/profile')
def profile():
    return render_template ('profile.html')
