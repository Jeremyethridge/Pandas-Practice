import requests
import pandas as pd
from sqlalchemy import create_engine


def extract()-> dict:
    #Grabs data from the url
    API_URL = "http://universities.hipolabs.com/search?country=United+States"
    data = requests.get(API_URL).json()
    return data


def transform(data:dict)-> pd.DataFrame:
    # Transforms the dataset into desired structure and filters
    df = pd.DataFrame(data)
    print(f"Total Number of Universities from API {len(data)}")
    df = df[df["name"].str.contains("North Carolina")]
    print(f"Number of Universities in North Carolina {len(df)}")
    df['domains'] = [','.join(map(str, l)) for l in df["domains"]]
    df['web_pages'] = [','.join(map(str, l)) for l in df['web_pages']]
    df = df.reset_index(drop=True)
    return df[['domains', 'country', 'web_pages', 'name']]

def load(df:pd.DataFrame) -> None:
    disk_engine = create_engine('sqlite:///my_lite_store.db')
    
    df.to_sql('cal_uni', disk_engine, if_exists='replace')



data = extract()
df = transform(data)
load(df)