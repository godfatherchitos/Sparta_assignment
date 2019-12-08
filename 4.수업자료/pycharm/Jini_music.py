import requests
from bs4 import BeautifulSoup

from openpyxl import load_workbook
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.upcoming

url = 'https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url,headers = headers)
soup = BeautifulSoup(data.text, 'html.parser')
musics = soup.select('#body-content > div.newest-list > div > table > tbody ')
print(musics[0])

rank = 1
for music in musics:
    # movie 안에 a 가 있으면,
    a_tag = music.select_one('td.title > div > a')
    if a_tag is not None:
        title = a_tag.text
        star = music.select_one('td.point').text

        doc = {
            'rank': rank,
            'title': title,
            'star': star
        }
        db.movies.insert_one(doc)
        rank += 1

#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
#old_content > table > tbody > tr:nth-child(2) > td.title > div > a