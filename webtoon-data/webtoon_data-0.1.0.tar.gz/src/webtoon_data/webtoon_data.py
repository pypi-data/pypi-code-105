import requests
import re
import pandas as pd
import json

def get_webtoon_genre_list():

    url = "https://webtoon.p.rapidapi.com/originals/genres/list"

    querystring = {"language":"en"}

    headers = {
        'x-rapidapi-host': "webtoon.p.rapidapi.com",
        'x-rapidapi-key': "200898dbd8msh7effe9f4aca8119p1f02a4jsn9f53b70ac5e8"
        }

    response_gen = requests.request("GET", url, headers=headers, params=querystring)

    webtoon_gen_json = response_gen.json()
    webtoon_json_gen_df = pd.DataFrame(webtoon_gen_json['message']['result']['genreList']['genres'])
    print(webtoon_json_gen_df['name'].tolist())


def get_webtoon_list_ranking(genre):

    url = "https://webtoon.p.rapidapi.com/originals/titles/list-by-rank"

    querystring = {"count":"30","language":"en"}

    headers = {
        'x-rapidapi-host': "webtoon.p.rapidapi.com",
        'x-rapidapi-key': "200898dbd8msh7effe9f4aca8119p1f02a4jsn9f53b70ac5e8"
        }

    response_rank = requests.request("GET", url, headers=headers, params=querystring)

    webtoon_rank_json = response_rank.json()
    webtoon_json_rank_df = pd.DataFrame(webtoon_json['message']['result']['titleNoListByTabCode'])
    webtoon_json_rank_df.head()
    webtoon_json_rank_df.loc[webtoon_json_rank_df['tabCode']==genre]
