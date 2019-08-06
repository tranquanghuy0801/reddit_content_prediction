import praw 
import pandas as pd 
import numpy as np
import datetime
import os 
from os.path import join, dirname
from dotenv import load_dotenv
 
dotenv_path = join(os.getcwd(), '.env')
load_dotenv(dotenv_path)
 
# Accessing environment variables 
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
user_agent = os.getenv('USER_AGENT')

folder = 'crawling_result'
path = os.path.join(os.getcwd(), folder)
today = datetime.date.today()

# Crawl the data from Reddit 
reddit = praw.Reddit(client_id=client_id,client_secret=client_secret,user_agent=user_agent)

posts = []
ml_subreddit = reddit.subreddit("QUTreddit")
for post in ml_subreddit.hot(limit=None):
	posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
posts = posts[posts['body'] != '']
if not os.path.exists(path):
	os.makedirs(path)
posts.to_csv("crawling_result/file-"+str(today)+".csv")
print("Crawling Completed");
