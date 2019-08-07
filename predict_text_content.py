import os 
import pandas as pd 

if not os.path.exists("result.csv"):
    data_loaded = pd.read_json("index.json")
    data_loaded.to_csv("result.csv")
df = pd.read_csv("result.csv")
df['Count'] = df.apply(lambda x: x.count(), axis=1)
df.rename(index=str,columns={'Unnamed: 0':'Categories'},inplace=True)
grouped = df[['Categories','Count']]
grouped = grouped.sort_values(by='Count',ascending=False)
print(grouped.head(5))




