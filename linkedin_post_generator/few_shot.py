import json

import pandas as pd
# from db import engine
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()
db_password=os.getenv('DB_PASSWORD')
engine = create_engine(f"mysql+pymysql://root:{db_password}@localhost:3306/post_generator_llm")

class FewShotPosts():
    def __init__(self,influencer="Akshat Shrivastava",file_path="data/processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self.unique_influencer= None
        self.unique_length=None
        self.unique_language=None
        self.influencer = influencer
        self.load_posts()

    def load_posts(self):
        # with open(file_path, encoding='utf-8') as f:
        #     posts =json.load(f)
        #     self.df = pd.json_normalize(posts)
        self.df = pd.read_sql(
            f"SELECT * FROM linkedin_posts WHERE influencer = \'{self.influencer}\'",
            con=engine
        )
        self.df['length'] = self.df['line_count'].apply(self.categorize_length)
        self.df['tags']= self.df['tags'].str.split(', ')
        all_tags = self.df['tags'].apply(lambda x : x).sum()
        self.unique_language = set(self.df['language'])
        # print(type(all_tags), all_tags)
        self.unique_tags = set(all_tags)
        self.unique_influencer = set(self.df['influencer'])
        self.unique_length = set(self.df['length'])


    def categorize_length(self,line_count):
        if line_count<5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"
    def get_tags(self):
        return self.unique_tags

    def get_influencer(self):
        return self.unique_influencer

    def get_length(self):
        return self.unique_length
    def get_language(self):
        return self.unique_language

    def get_filtered_posts(self,length,language,tag):
        df_filtered=self.df[
            (self.df['language'] == language) &
            (self.df['length'] == length) &
            (self.df['tags'].apply(lambda tags : tag in tags)
             # & (self.df['influencer'] == influencer)
             )
        ]
        return df_filtered.to_dict(orient='records')
if __name__ == '__main__':
    fs = FewShotPosts()
    posts=fs.get_filtered_posts("Long","English","Taxation")
    print(posts)