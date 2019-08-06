import praw 
import pandas as pd 

reddit = praw.Reddit(client_id="RAmbn7tRTvUBJw",client_secret="l5jdhfdVUw3PcQLijVKBOOTqwog",user_agent="WebScrape")

posts = []
ml_subreddit = reddit.subreddit("QUTreddit")
for post in ml_subreddit.hot(limit=None):
    posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
posts.to_csv("qut_reddit060819.csv")
print("Crawling Completed")
