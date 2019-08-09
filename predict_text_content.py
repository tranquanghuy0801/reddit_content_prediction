import os 
import pandas as pd 
from preprocess_text import create_dir
from classify_text_tutorial import index 

path = create_dir(os.getcwd(),'/resources')
process_path = create_dir(path,'/text_files')
reddit_link = path + '/reddits/urls.txt' 

def predict_label(reddit_link,process_path):
	f = open(reddit_link, "r")
	print("Start Predicting")
	for text in f:
		text = text.rstrip('\n').strip() 
		path_text = process_path + "/" + text 
		result = index(path_text,path_text,"index.json")
		data_loaded = pd.read_json(path_text+"/index.json")
		os.remove(path_text+"/index.json")
		data_loaded.to_csv(path_text+"/result.csv")
		df = pd.read_csv(path_text+"/result.csv")
		df['Count'] = df.apply(lambda x: x.count(), axis=1)
		df.rename(index=str,columns={'Unnamed: 0':'Categories'},inplace=True)
		grouped = df[['Categories','Count']]
		grouped = grouped.sort_values(by='Count',ascending=False)
		print('=' * 20)
		print('The top 5 content labels of /r/' + text + ' predicted by Google NLP API')
		print(grouped.head(5))
	print("Close Predicting")

predict_label(reddit_link,process_path)


'''
if not os.path.exists("result.csv"):
	data_loaded = pd.read_json("index.json")
	data_loaded.to_csv("result.csv")
df = pd.read_csv("result.csv")
df['Count'] = df.apply(lambda x: x.count(), axis=1)
df.rename(index=str,columns={'Unnamed: 0':'Categories'},inplace=True)
grouped = df[['Categories','Count']]
grouped = grouped.sort_values(by='Count',ascending=False)
print(grouped.head(5))
'''




