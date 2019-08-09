from dotenv import load_dotenv
from os.path import join, dirname
import io
import praw
import pandas as pd
import numpy as np
import datetime
import os
from preprocess_text import preprocess

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
output_csv = path + url_folder
output_txt = path + '/text_files'
today = datetime.date.today()

# Crawl the data from Reddit
def process_url(input_path, output_csv, output_txt):
	for filename in os.listdir(input_path):
		if(filename.endswith(".txt")):
			file_path = os.path.join(input_path, filename)
			f = open(file_path, "r")
			for text in f:
				text = text.rstrip('\n').strip()
				print(text)
				reddit = praw.Reddit(client_id=client_id,
                                    client_secret=client_secret, user_agent=user_agent)
				# Save the crawled data to CSV file
				posts = []
				ml_subreddit = reddit.subreddit(text)
				for post in ml_subreddit.hot(limit=30):
					posts.append([post.title, post.score, post.id, post.subreddit,
                                            post.url, post.num_comments, post.selftext, post.created])
				posts = pd.DataFrame(posts, columns=[
                                    'title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
				posts = posts[posts['body'] != '']
				print(posts.isna().sum())
				if not os.path.exists(output_csv+"/"+text):
					os.makedirs(output_csv+"/"+text)
				if not os.path.exists(output_txt+"/"+text):
					os.makedirs(output_txt+"/"+text)
				posts.to_csv(output_csv+"/"+text+"/"+str(text)+"-"+str(today)+".csv")
				data = pd.read_csv(output_csv+"/"+text+"/"+str(text)+"-"+str(today)+".csv", names=[
				                   'title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
				data['title'] = data['title'].apply(preprocess)
				data['body'] = data['body'].apply(preprocess)
				#data.to_csv(output_csv+"/"+text+"/news.csv")
				#data = data['body'].replace('', np.nan, inplace=True)
				#data=data.dropna(axis=0, how='any')
				data['len_word'] = data['body'].apply(lambda x: len(x.split()))
				data = data[data['len_word'] >= 20]
				data['body'].to_csv(output_txt+"/"+text+"/"+str(text)+"-"+str(today) +
                                    ".txt", header=False, index=False, sep='\t')

				with open(output_txt+"/"+text+"/"+str(text)+"-"+str(today)+".txt") as csvfile:
					for i, line in enumerate(csvfile):
						with open(output_txt+"/"+text+"/file{}.txt".format(str(i+1)), "w") as txtfile:
							txtfile.write(line)
				if os.path.exists(output_txt+"/"+text+"/"+str(text)+"-"+str(today)+".txt"):
					os.remove(output_txt+"/"+text+"/"+str(text)+"-"+str(today)+".txt")


process_url(input_path, output_csv, output_txt)
print("Crawling Completed")

