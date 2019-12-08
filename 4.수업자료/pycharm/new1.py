from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
   return 'This is Home!'

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)

@app.route('/mypage/')
def mypage():
    return'This is My page!'
@app.route('/mypage/')
def test_post():
    return
#@app.route('/test', methods=['POST'])
## API 역할을 하는 부분
def test_post():
   title_receive = request.form['title_give']
   print(title_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 POST!'})

@app.route('/test/db',methods = ['POST'])
def test_postdb():
    rank_receive = request.form['rank_give']
    print(rank_receive)
    rank_receive = int(rank_receive)
    star_receive = request.form['star_give']


    db.movies.update_one({'rank': rank_receive}, {'$set': {'star': star_receive}})
    return jsonify({'result':'success','msg':'update 요청완료'})

@app.route('/test/db', methods = ['GET'])
def test_getdb():
    rank_receive = request.args.get('rank_give')
    rank_receive = int(rank_receive)
    movie = db.movies.find_one({'rank':rank_receive},{'_id':0})
    print(movie)
    return jsonify({'result':'success'})

@app.route('/test/new',methods = ['POST'])
def new_post():
    rank_receive = int(request.form['rank_give'])
    title_receive = request.form['title_give']
    star_receive = request.form['star_give']

    db.movies.insert_one({'rank':rank_receive,'title':title_receive, 'star':star_receive})

    return jsonify({'result':'success'})
@app.route('/test', methods=['GET'])
def test_get():
  title_receive = request.args.get('title_give')
  print(title_receive)
  return jsonify({'result':'success', 'msg': '이 요청은 GET!'})

@app.route('/test', methods=['GET'])
def test_get():
  #title_receive = request.args.get('title_give')
   #print(title_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 GET!'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)

