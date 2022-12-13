from src.models import User_account, User_comment, Post, post_vote, comment_vote, db

def refresh_db():
    #post_vote.query.delete()
    #comment_vote.query.delete()
    User_comment.query.delete()
    Post.query.delete() 
    User_account.query.delete()
    db.session.commit()