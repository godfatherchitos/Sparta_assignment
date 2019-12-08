import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbmusic

url = "https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908&hh=21&rtm=N"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

pageNum = 1

for page in range(1,5) :
    data = requests.get(url,params= params, headers=headers)
#https://www.genie.co.kr/chart/top200?ditc=D&ymd=20191109&hh=12&rtm=N&pg=2
soup = BeautifulSoup(data.text, 'html.parser')

songs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
pageNum +=1
rank = 1
for song in songs:
    a_tag = song.select_one('td.info > a.title.ellipsis')
    #양쪽 끝의 공백 문자를 제거하는 경우 - str.strip
    title = a_tag.text.strip()
    artist = song.select_one('a.artist.ellipsis').text
    rank = song.select_one('td.number').content[0].strip()
    doc = {
        'rank' : rank,
        'title' : title,
        'artist' : artist
    }
    #db.songs.insert_one(doc)
    print(rank,title,artist)
    rank += 1