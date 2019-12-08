from flask import Flask,render_template,jsonify,request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.mmt                      # 'dbsparta'라는 이름의 db를 만듭니다.


@app.route('/')
def home():
   return render_template('index.html')
@app.route('/post',methods =['POST'])
def saving():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    author_receive = request.form['author_give']

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers = headers)

    soup = BeautifulSoup(data.text, 'html.parcer')
    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property = og: "title"]')
    og_description = soup.select_one('meta[property = og: "description"]')
    url_image = og_image['content']
    url_title = og_title['content']
    url_description = og_description['content']

    article = {'author': author_receive, 'url': url_receive, 'comment': comment_receive, 'image': url_image,
               'title': url_title, 'desc': url_description}

    db.articles.insert_one(article)

    return jsonify({'result': 'success'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5001,debug=True)



