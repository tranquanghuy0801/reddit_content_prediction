import praw 
import pandas as pd 
import numpy as np
import datetime
import os 
import glob
import io
from os.path import join, dirname
from dotenv import load_dotenv
 
dotenv_path = join(os.getcwd(), '.env')
load_dotenv(dotenv_path)
 
# Accessing environment variables 
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
user_agent = os.getenv('USER_AGENT')

folder = 'resources'
url_folder = '/csv_files'
path = os.path.join(os.getcwd(), folder)
if not os.path.exists(path+url_folder):
	os.makedirs(path+url_folder)
input_path = path + '/reddits'
output_path = path + url_folder
today = datetime.date.today()
print(input_path)
print(output_path)

# Crawl the data from Reddit 
def process_url(input_path,output_path):
	for filename in os.listdir(input_path):
		if(filename.endswith(".txt")):
			file_path = os.path.join(input_path, filename)
			f = open(file_path,"r")
			for text in f:
				text = text.rstrip('\n').strip()
				print(text)
				reddit = praw.Reddit(client_id=client_id,client_secret=client_secret,user_agent=user_agent)
				# Save the crawled data to CSV file
				posts = []
				ml_subreddit = reddit.subreddit(text)
				for post in ml_subreddit.hot(limit=30):
					posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
				posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
				posts = posts[posts['body'] != '']
				os.makedirs(output_path+"/"+text)
				posts.to_csv(output_path+"/"+text+"/"+str(text)+"-"+str(today)+".csv")
		

process_url(input_path,output_path)
print("Crawling Completed");