from flask import Flask, render_template, jsonify, request, redirect
from pymongo import MongoClient
from datetime import datetime, timedelta
import json
import jwt

SECRET_KEY = 'jungle'

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbjungle

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try :
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('index.html')
    except jwt.ExpiredSignatureError :
        return redirect("http://localhost:5000/")
    except jwt.exceptions.DecodeError :
        return redirect("http://localhost:5000/")


@app.route('/login', methods=['POST'])
def login() :
    # id, pw 받기
    input_data = request.form
    user_id = input_data['id']
    user_pw = input_data['pw']

    #일치하는 경우
    if(user_id == ) :
        payload = {
            'id' : user_id,
            'exp' : datetime.utcnow() + timedelta(minutes=60) #로그인 60분 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result' : 'success', 'token' : token})

    else :
        return jsonify({'result' : 'fail'})

@app.sign_up('/sign_up', methods=['POST'])
def sign_up() :
    # id, pw 받기
    input_data = request.form
    user_id = input_data['id']
    user_pw = input_data['pw']

    memos = {'id' : id, 'title': title, 'content': content, 'like': like_default}
    db.memos.insert_one(memos)

    

@app.route('/main', methods=['POST'])
def show_quests():
    sort = request.form
    if(sort==0) :
        quest = list(db.quests.find({}, {'_id':False}).sort('like', -1))
    elif(sort==1) :
        quest = list(db.quests.find({}, {'_id':False}).sort('hate', -1))
    elif(sort==2) :
        quest = list(db.quests.find({}, {'_id':False}).sort('time', -1))
    elif(sort==3) :
        quest = list(db.quests.find({}, {'_id':False}).sort('treasure', -1))

    return jsonify({'result': 'success', 'quests_list': quest})

@app.route('/main', methods=['POST'])
def post_quests():
    title=request.form['title']
    content=request.form['content']
    like_default = 0
    hate_default = 0
    overlap = False
    while not overlap :
        id = title + str(random.randint(0, 9999))
        overlap = db.memos.find({'id':id})

    memos = {'id' : id, 'title': title, 'content': content, 'like': like_default}
    db.memos.insert_one(memos)

    return jsonify({'result': 'success'})

@app.route('/api/like', methods=['POST'])
def api_like() :
    id_receive = request.form['id_receive']
    quest = db.quests.find_one({'id':id_receive})
    new_like = quest['like']+1
    db.quest.update_one({'id':id_receive},{'$set':{'like':new_like}})
    return jsonify({'result': 'success'})

@app.route('/api/hate', methods=['POST'])
def api_hate() :
    id_receive = request.form['id_receive']
    quest = db.quests.find_one({'id':id_receive})
    new_hate = quest['hate']+1
    db.quest.update_one({'id':id_receive},{'$set':{'like':new_hate}})
    return jsonify({'result': 'success'})

@app.route('/api/delete', methods=['POST'])
def api_delete() :
    id_receive = request.form['id_receive']
    db.quests.delete_one({'id':id_receive})
    return jsonify({'result': 'success'})

@app.route('/api/edit', methods=['POST'])
def api_edit() :
    a = 'a'

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)