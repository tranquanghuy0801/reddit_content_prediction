import praw 
import pandas as pd 
import numpy as np
import datetime
import os 
import glob
from os.path import join, dirname
from dotenv import load_dotenv
 
dotenv_path = join(os.getcwd(), '.env')
load_dotenv(dotenv_path)
 
# Accessing environment variables 
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
user_agent = os.getenv('USER_AGENT')
reddit = os.getenv('REDDIT')
csv_file = os.getenv('CSV_FILE')

# Create input and output paths to read files 
folder = 'resources'
path = os.path.join(os.getcwd(), folder)
if not os.path.exists(path+reddit):
	os.makedirs(path+reddit)
elif not os.path.exists(path+csv_file):
	os.makedirs(path+csv_file)
input_path = path + reddit
output_path = path + csv_file 
today = datetime.date.today()

# Crawl the data from Reddit 
def process_url(input_path,output_path):
	for filename in os.listdir(input_path):
		if(filename.endswith(".txt")):
			file_path = os.path.join(input_path, filename)
			f = open(file_path,"r")
			for text in f:
				text = text.rstrip('\n')
				reddit = praw.Reddit(client_id=client_id,client_secret=client_secret,user_agent=user_agent)
				# Save the crawled data to CSV file
				posts = []
				ml_subreddit = reddit.subreddit(text)
				for post in ml_subreddit.hot(limit=30):
					posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
				posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
				posts = posts[posts['body'] != '']
				if not os.path.exists(output_path+"/"+text):
					os.makedirs(output_path+"/"+text)
					posts.to_csv(output_path+"/"+text+"/"+str(text)+"-"+str(today)+".csv")
			f.close()
		
		if not os.path.isfile(file_path):
			print('Failed to process {}'.format(file_path))

process_url(input_path,output_path)
print("Crawling Completed");
