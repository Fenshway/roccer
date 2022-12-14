from flask import current_app
import time
import atexit
from src.repositories.post_repository import post_repository_singleton
import datetime
from src.models import Post,db
import app
from app import db
import math
import random
import requests

class Post_bot:
    AVERAGE_POST_PER_HOUR = 3
    UPDATE_SECONDS = 1200

    def preform_post(self):
        with app.app.app_context():
            time_1_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
            posts = db.session.query(Post).filter(
                Post.created_at >= time_1_hour_ago
                ).all()
            standardized_ratio = 1
            if len(posts) > 0:
                standardized_ratio = (len(posts) / -(self.AVERAGE_POST_PER_HOUR)) + 1
            if random.random() < standardized_ratio:
                stashed_posts = post_repository_singleton.get_all_bot_stashed_posts()
                if stashed_posts == []:
                    sources = ['youtube']
                    selected_source = random.choice(sources)
                    queries = ['soccer', 'soccer news', 'fifa', "fifa world cup"]
                    if selected_source == 'youtube':
                            search_url = 'https://www.googleapis.com/youtube/v3/search'
                            video_url = 'https://www.googleapis.com/youtube/v3/videos'
                            max_results = 3
                            search_parameters = {
                                'key' : current_app.config['YOUTUBE_API_KEY'],
                                'q' : random.choice(queries),
                                'part' : 'snippet',
                                'maxResults' : max_results,
                                'type' : 'video'
                            }
                            youtube_request = requests.get(search_url,params=search_parameters)

                            results = ''
                            try:
                                results = youtube_request.json()['items']
                            except:
                                print("API Error, could not connect to API or query limit hasd been reached.")
                                return
                            
                            video_ids = []
                            for result in results:
                                video_ids.append(result['id']['videoId'])
                            
                            video_params = {
                                'key': current_app.config['YOUTUBE_API_KEY'],
                                'id': ','.join(video_ids),
                                'part': 'snippet,status',
                                'maxResults' : max_results

                            }
                            youtube_request = requests.get(video_url, params=video_params)
                            results = youtube_request.json()['items']
                            for result in results:
                                title = result['snippet']['title']
                                url = 'https://www.youtube.com/embed/' + str(result['id'])
                                embedable = result['status']['embeddable']
                                watch_url = 'https://www.youtube.com/watch?v=' + str(result['id'])

                                if post_repository_singleton.post_has_unique_title(title) and embedable:
                                    if result['snippet']['channelTitle'] in ['FOX Soccer', 'FIFA'] :
                                        post_repository_singleton.create_post_text(title, watch_url,None,True)
                                    else:
                                        post_repository_singleton.create_post_embedded_video(title, url, None,True)
                post_repository_singleton.unstash_random_post()


            print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
        
    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

post_bot_singleton = Post_bot()