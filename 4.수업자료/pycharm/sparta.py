import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20190909&page=2',headers=headers)

soap = BeautifulSoup(data.text, 'html.parser')

movies = soap.select('#old_content > table > tbody > tr')
#print(movies)


rank = 50
for movie in movies :
    a_tag = movie.select_one('td.title>div>a')
    if not a_tag == None :
        title = a_tag.text
        star = movie.select_one('td.point').text
        print(rank,title, star)
        rank += 1
#old_content > table > tbody > tr:nth-child(2) > td:nth-child(3) > div > div > img





