from flask import Flask, render_template, jsonify, request, redirect
from pymongo import MongoClient
from datetime import datetime, timedelta
import json
import jwt
import random

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
        return redirect("http://localhost:5000/login")
    except jwt.exceptions.DecodeError :
        return redirect("http://localhost:5000/login")


@app.route('/login', methods=['POST'])
def login() :
    # id, pw 받기
    input_data = request.form
    user_id = input_data['id']
    user_pw = input_data['pw']
    db_user = db.users.find_one({'id' : user_id})

    #일치하는 경우
    if(db_user['pw']==user_pw) :
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
    user_name = input_data['name']
    user_phone_number = input_data['phone_number']

    if db.users.find_one({'id':user_id}) == None :
        quests_user = {'id' : user_id, 'pw': user_pw}
        db.quests_users.insert_one(quests_user)
        return jsonify({'result' : 'success'})
    else :
        return jsonify({'result' : 'fail'})
    

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
        overlap = db.quests.find({'id':id})

    writer = request.form['user_id']
    quest = {'id' : id, 'writer' : writer, 'title': title, 'content': content, 'like': like_default, 'hate': hate_default}
    db.quests.insert_one(quest)
    db.users.update_one=({'id' : writer}, {'$set':{id : 0}})

    return jsonify({'result': 'success'})

@app.route('/api/like', methods=['POST'])
def api_like() :
    user_id_receive = request.form['user_id_receive']
    quest_id_receive = request.form['quest_id_receive']
    quest = db.quests.find_one({'id':quest_id_receive})
    user = db.users.find_one({'id':user_id_receive})

    try :
        if user[quest_id_receive] == 0 :
            db.users.update_one({'id' : quest[id]}, {'$set':{quest[id]:1}})
            like_up = quest['like'] + 1
            db.quests.update_one({'like':like_up})
    except :
        print('이미 좋아요')
            

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