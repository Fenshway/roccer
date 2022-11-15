from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

post_vote = db.Table(
    'post_vote',
    db.Column('user_account_id', db.Integer, \
        db.ForeignKey('user_account.user_account_id'), primary_key=True),
    db.Column('post_id', db.Integer, \
        db.ForeignKey('post.post_id'), primary_key=True),
    db.Column('upvote', db.Boolean, nullable=False)
)

comment_vote = db.Table(
    'comment_vote',
    db.Column('user_account_id', db.Integer, \
        db.ForeignKey('user_account.user_account_id'), primary_key=True),
    db.Column('post_id', db.Integer, \
        db.ForeignKey('post.post_id'), primary_key=True),
    db.Column('upvote', db.Boolean, nullable=False)
)

class User_account(db.Model):
    user_account_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    user_password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), nullable=False)


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    post_type = db.Column(db.String, nullable=False)
    embedded_video_link = db.Column(db.String, nullable=True)
    stored_video_path = db.Column(db.String, nullable=True)
    stored_image_path = db.Column(db.String, nullable=True)
    post_text = db.Column(db.String, nullable=True)
    created_at = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    posted_by_id = db.Column(db.Integer,\
        db.ForeignKey('user_account.user_account_id'), nullable=True)
        
    posted_by = db.relationship('User_account', backref='posts')

    votes = db.relationship('User_account', secondary=post_vote, backref='votes')


class User_comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), nullable=False)

    parent_post_id = db.Column(db.Integer,\
        db.ForeignKey('post.post_id'), nullable=True)
    parent_post = db.relationship('Post', backref= 'comments')
    parent_comment_id = db.Column(db.Integer,\
        db.ForeignKey('user_comment.comment_id'), nullable=True)
    commented_by_id = db.Column(db.Integer,\
        db.ForeignKey('user_account.user_account_id'), nullable=True)
    commented_by = db.relationship('User_account', backref='comments')
        