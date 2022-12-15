from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, update
db = SQLAlchemy()
from datetime import datetime

class Post_Vote(db.Model):
    __tablename__ = "post_vote"
    user_account_id = db.Column(db.ForeignKey("user_account.user_account_id"), nullable=False, primary_key=True)
    post_id = db.Column(db.ForeignKey("post.post_id"), nullable=False, primary_key=True)
    created_at = db.Column(db.TIMESTAMP(timezone=False), nullable=False, server_default=func.now())
    upvote = db.Column(db.Boolean, nullable=False)

    post = db.relationship('Post', backref= 'votes')
    def __init__(self, user_account_id, post_id, vote):
        self.user_account_id = user_account_id
        self.post_id = post_id
        self.upvote = vote


class Comment_vote(db.Model):
    user_account_id = db.Column(db.Integer, primary_key=True)
    user_comment_id = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=False), nullable=False, server_default=func.now())

class User_account(db.Model):
    user_account_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    user_password = db.Column(db.String, nullable=False)
    profile_path = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=False), nullable=False, server_default=func.now())

    def __init__(self, first_name, last_name, username, password, profile_path):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.user_password = password
        self.profile_path = profile_path

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    post_type = db.Column(db.String, nullable=False)
    embedded_video_link = db.Column(db.String, nullable=True)
    stored_video_path = db.Column(db.String, nullable=True)
    stored_image_path = db.Column(db.String, nullable=True)
    post_text = db.Column(db.String, nullable=True)
    created_at = db.Column(db.TIMESTAMP(timezone=False), nullable=False, server_default=func.now())
    posted_by_id = db.Column(db.Integer,\
        db.ForeignKey('user_account.user_account_id'), nullable=True)
        
    posted_by = db.relationship('User_account', backref='posts')
    post_bot_stashed = db.Column(db.Boolean, nullable = False, default=False)

    def __init__(self, title, post_type, embedded_video_link, stored_video_path, stored_image_path, post_text, posted_by_id, stashed=False):
        self.title = title
        self.post_type = post_type
        self.embedded_video_link = embedded_video_link
        self.stored_video_path = stored_video_path
        self.stored_image_path = stored_image_path
        self.post_text = post_text
        self.posted_by_id = posted_by_id
        self.post_bot_stashed = stashed
    
    def get_vote_count(post):
        total = 0
        votes = post.votes 
        for vote in votes:
            if vote.upvote:
                total += 1
            else:
                total -= 1
        return total
        


    def get_time_text(post):
        now = datetime.now()
        minutes = (now - post.created_at).total_seconds() / 60
        if minutes < 2:
            return('1 minute ago')
        if minutes < 60:
            return(str(int(minutes)) + ' minutes ago')
        
        hours = minutes / 60
        if hours < 2:
            return('1 hour ago')
        if hours < 24:
            return(str(int(hours)) + ' hours ago')
        
        days = hours / 24
        if days < 2:
            return('1 day ago')
        if days < 365:
            return(str(int(days)) + ' days ago')

        years = days / 365
        if years < 2:
            return('1 year ago')
        return(str(int(years)) + ' years ago')


class User_comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    parent_post_id = db.Column(db.Integer,\
        db.ForeignKey('post.post_id'), nullable=True)
    parent_post = db.relationship('Post', backref= 'comments')
    parent_comment_id = db.Column(db.Integer,\
        db.ForeignKey('user_comment.comment_id'), nullable=True)
    commented_by_id = db.Column(db.Integer,\
        db.ForeignKey('user_account.user_account_id'), nullable=False)
    commented_by = db.relationship('User_account', backref='comments')

    def get_time_text(self):
        now = datetime.now()
        print(self.created_at)
        print(now)
        minutes = (now - self.created_at).total_seconds() / 60
        if minutes < 2:
            return('1 minute ago')
        if minutes < 60:
            return(str(int(minutes)) + ' minutes ago')
        
        hours = minutes / 60
        if hours < 2:
            return('1 hour ago')
        if hours < 24:
            return(str(int(hours)) + ' hours ago')
        
        days = hours / 24
        if days < 2:
            return('1 day ago')
        if days < 365:
            return(str(int(days)) + ' days ago')

        years = days / 365
        if years < 2:
            return('1 year ago')
        return(str(int(years)) + ' years ago')
            
