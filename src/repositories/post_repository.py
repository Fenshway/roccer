from src.models import Post
from app import db

class PostRepository:
    def get_all_posts(self):
        posts = Post.query.all()
        return posts
    def get_post_by_id(self, post_id):
        return Post.query.get(post_id)
        
    def create_post_embedded_video(self, title, embedded_video_link, posted_by_id):
        new_post = Post(title, 'embedded_video', embedded_video_link, None, None, None, posted_by_id)
        db.session.add(new_post)
        db.session.commit()
        return new_post
    def create_post_stored_video(self, title, video_path, posted_by_id):
        new_post = Post(title, 'stored_video', None, video_path, None, None, posted_by_id)
        db.session.add(new_post)
        db.session.commit()
        return new_post

    def create_post_stored_image(self, title, image_path, posted_by_id):
        new_post = Post(title, 'stored_image', None, None, image_path, None, posted_by_id)
        db.session.add(new_post)
        db.session.commit()
        return new_post
    
    def create_post_text(self, title, post_text, posted_by_id):
        new_post = Post(title, 'text', None, None, None, post_text, posted_by_id)
        db.session.add(new_post)
        db.session.commit()
        return new_post

    def search_post(self, post_title, user_id, post_type):
        pass
    

post_repository_singleton = PostRepository()