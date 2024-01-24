import requests
import pandas as pd
from .vars import GITHUB_KEY

from io import BytesIO
from github import Github


def read_parquet(link:str,save:bool = False) -> pd.DataFrame:
    gran_data = requests.get(link)
    gran_data_df = pd.read_parquet((BytesIO(gran_data.content)))
    if save:
        gran_data_df.to_csv("../data/gran_data_.csv")
    return gran_data_df

def get_data_from_repo(repo_link:str,save:bool = False) -> dict[pd.DataFrame]:
    token = GITHUB_KEY
    g = Github(token)
    repo = g.get_repo(repo_link)
    contents = repo.get_contents("./")
    contents_links = [c.download_url for c in contents]
    
    df_dict = {}
    for link in contents_links:
        filename = link.split('/')[-1]
        df_name = filename.split(".csv")[0]+"_df"
        
        df_dict[df_name] = pd.read_csv(link)
        if save:
            df_dict[df_name].to_csv("../data/filename")
            
    return df_dict

