# Import libraries 
import pandas as pd 
import re 
from nltk.corpus import stopwords
import os 

# Read data crawled from Reddit 
data = pd.read_csv('crawling_result/file-2019-08-07.csv',names=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created']);

# Regex to preprocess data 
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))
path = os.path.join(os.getcwd(), 'crawling_result')
folder = "/resources" # Folder to save text file after preprocessing

def clean_text(text):
    """
        text: a string
        
        return: modified initial string
    """
    text = text.lower() # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # delete stopwors from text
    return text

data['title'] = data['title'].apply(clean_text)
data['body'] = data['body'].apply(clean_text)
data['len_word'] = data['body'].apply(lambda x: len(x.split()))
data = data[data['len_word'] >= 20]

if not os.path.exists(path+folder):
    os.path.makedirs(path+folder)
path = path+folder
data['body'].to_csv(path+"/new.txt",header=False,index=False, sep='\t')

with open(path+"/new.txt") as csvfile:
    for i, line in enumerate(csvfile):
        with open(path+"/file{}.txt".format(str(i+1)), "w") as txtfile:
            txtfile.write(line)

if os.path.exists(path+"/new.txt"):
    os.remove(path+"/new.txt")