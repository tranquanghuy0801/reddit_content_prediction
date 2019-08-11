Predict top 5 content labels using Praw API and Google Cloud Natural Language API for each reddit (/r/?)

Add all reddit links wanted to predict in directory: resources/reddits/urls.txt 

Steps to do 

1. Install gcloud terminal commands
2. Choose and config the GCP project
3. Enable the Google Cloud Natural Language API 
4. Download the JSON key and export it on terminal using (export GOOGLE_APPLICATION_CREDENTIALS="direction_json_key") 
5. Create a virtual environment using command (virtualenv reddit_crawl && source reddit_craw/bin/activate && pip install -r requirements.txt) 
6. Run (python3 predict_text_content.py) on the main directory to get results 
