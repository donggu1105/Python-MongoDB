from bs4 import BeautifulSoup
import requests
import pymongo
import re
from pprint import pprint

# connect mongodb
username = "donggu"
password = "2245"
host = "3.35.255.138"
conn = pymongo.MongoClient(f"mongodb://{username}:{password}@{host}")

actor_db = conn.cine21
actor_collection = actor_db.actor_collection



url = "http://www.cine21.com/rank/person/content"
post_data = dict()
post_data["section"]  = "actor"
post_data["period_start"] = "2021-02"
post_data["gender"] = "all"
actors_detail_info = list()

for index in range(1,21):
     post_data["page"] = index

     res = requests.post(url, data=post_data)

     soup = BeautifulSoup(res.content, "html.parser")
     actors = soup.select("li.people_li div.name")
     hits = soup.select("ul.num_info > li > strong")
     movie_list = soup.select('ul.mov_list')
     ranks = soup.select('li.people_li span.grade')



     for index, actor in enumerate(actors):
          # print(re.sub('\(\w*\)', '', actor.text))
          actor_name = re.sub('\(\w*\)','', actor.text)
          actor_hits = int(hits[index].text.replace(',',''))
          rank = int(ranks[index].text)
          movie_titles = movie_list[index].select('li span')
          movie_title_list = list()
          for movie_title in movie_titles:
               movie_title_list.append(movie_title.text)



          actor_link = 'http://www.cine21.com'+actor.select_one('a').attrs['href']
          response_actor = requests.get(actor_link)
          soup_actor = BeautifulSoup(response_actor.content, "html.parser")
          default_info = soup_actor.select_one("ul.default_info")
          actor_details = default_info.select("li")


          actor_info_dict = dict()

          actor_info_dict["배우이름"] = actor_name
          actor_info_dict["흥행지수"] = actor_hits
          actor_info_dict["출연영화"] = movie_title_list
          actor_info_dict["랭킹"] = rank

          for actor_item in actor_details:
               actor_item_field = actor_item.select_one('span.tit').text
               actor_item_value = re.sub('<span.*?>.*?</span>', '', str(actor_item))
               actor_item_value = re.sub('<.*?>','', actor_item_value)

               actor_info_dict[actor_item_field] = actor_item_value

          actors_detail_info.append(actor_info_dict)



pprint(actors_detail_info)

# 특수한 정규 표현식

# Greedy vs. NonGreedy
# . 문자ㅡㄴ 줄바꿈 누자인 \n 을 제외한 모든 문자 한개를 의미함
#  * 는 앞 문자가 0번또는 그 이상 반복되는 패턴
