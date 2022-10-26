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

@app.route('/login')
def home():
    #토큰 받기
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
    # 정보 받기
    input_data = request.form
    user_id = input_data['id']
    user_pw = input_data['pw']
    user_name = input_data['name']
    user_phone_number = input_data['phone_number']
    user_like_list = []
    user_hate_list = []
    user_star_list = []

    if db.users.find_one({'id':user_id}) == None :
        quests_user = {'id' : user_id, 'pw': user_pw, 'name': user_name, 'phone_number': user_pw, 'like_list': user_pw, 'hate_list': user_pw, 'star_list': user_pw}
        db.users.insert_one(quests_user)
        return jsonify({'result' : 'success'})
    else :
        return jsonify({'result' : 'fail'})
    

@app.route('/main', methods=['POST'])
def show_quests():
    user_id = request.form['user_id']
    sort = request.form['sort']

    user = db.users.find_one({'id':user_id}, {'_id':False})
    quest = list(db.quests.find({}))

    if(sort==0) :
        quest = list(db.quests.find({}, {'_id':False}).sort('like', 1))
    elif(sort==1) :
        quest = list(db.quests.find({}, {'_id':False}).sort('hate', 1))
    elif(sort==2) :
        quest = list(db.quests.find({}, {'_id':False}).sort('star', 1))
    elif(sort==3) :
        quest = list(db.quests.find({}, {'_id':False}).sort('treasure', 1))
    elif(sort==4) :
        quest = list(db.quests.find({}, {'_id':False}).sort('date', 1))

    for i in quest :
            for j in user['star_list'] :
                if quest['id'][i] == user['star_list'][j] :
                    temp = quest[i]
                    del quest[i]
                    quest.append(temp)
                    break

    quest.reverse()

    return jsonify({'result': 'success', 'quests_list': quest})

@app.route('/main', methods=['POST'])
def post_quests():
    title=request.form['title']
    content=request.form['content']
    user_id=request.form['user_id']
    treasure=request.form['treasure']
    like_default = 0
    hate_default = 0
    star_default = 0
    date = datetime.utcnow()
    overlap = False
    while not overlap :
        id = title + str(random.randint(0, 9999))
        overlap = db.quests.find({'id':id})

    quest = {'id' : id, 'writer' : user_id, 'title': title, 'content': content, 'like': like_default, 'hate': hate_default, 'star': star_default, 'treasure' : treasure, 'date': date}
    db.quests.insert_one(quest)

    return jsonify({'result': 'success'})

@app.route('/api/like', methods=['POST'])
def api_like() :
    user_id_receive = request.form['user_id_receive']
    quest_id_receive = request.form['quest_id_receive']
    quest = db.quests.find_one({'id':quest_id_receive})
    user = db.users.find_one({'id':user_id_receive})
    overlap = False

    for i in user['like_list'] :
        if user['like_list'][i] == quest['id']:
            overlap = True

    if overlap != True :
        temp = list(user['like_list'])
        temp.append(quest_id_receive)
        db.users.update_one({'id':id}, {'$set':{'like_list' :temp}})
        like_up = quest['like'] + 1
        db.quest.update_one({'id':quest_id_receive},{'$set':{'like':like_up}})
        return jsonify({'result': 'success'})
    else :
        return jsonify({'result': 'fail'})        

@app.route('/api/hate', methods=['POST'])
def api_hate() :
    user_id_receive = request.form['user_id_receive']
    quest_id_receive = request.form['quest_id_receive']
    quest = db.quests.find_one({'id':quest_id_receive})
    user = db.users.find_one({'id':user_id_receive})
    overlap = False

    for i in user['hate_list'] :
        if user['hate_list'][i] == quest['id']:
            overlap = True

    if overlap != True :
        temp = list(user['hate_list'])
        temp.append(quest_id_receive)
        db.users.update_one({'id':id}, {'$set':{'hate_list' :temp}})
        hate_up = quest['hate'] + 1
        db.quest.update_one({'id':quest_id_receive},{'$set':{'hate':hate_up}})
        return jsonify({'result': 'success'})
    else :
        return jsonify({'result': 'fail'})    

@app.route('/api/star', methods=['POST'])
def api_hate() :
    user_id_receive = request.form['user_id_receive']
    quest_id_receive = request.form['quest_id_receive']
    quest = db.quests.find_one({'id':quest_id_receive})
    user = db.users.find_one({'id':user_id_receive})
    overlap = False

    for i in user['star_list'] :
        if user['star_list'][i] == quest['id']:
            overlap = True

    if overlap != True :
        temp = list(user['star_list'])
        temp.append(quest_id_receive)
        db.users.update_one({'id':id}, {'$set':{'star_list' :temp}})
        star_up = quest['star'] + 1
        db.quest.update_one({'id':quest_id_receive},{'$set':{'star':star_up}})
        return jsonify({'result': 'success'})
    else :
        return jsonify({'result': 'fail'})  

@app.route('/api/delete', methods=['POST'])
def api_delete() :
    id_receive = request.form['id_receive']
    db.quests.delete_one({'id':id_receive})
    return jsonify({'result': 'success'})

@app.route('/api/edit', methods=['POST'])
def api_edit() :
    id = request.form['id']
    title = request.form['nt'] 
    content = request.form['nc']
    treasure = request.form['ntreasure']
    date = datetime.utcnow()
 
    db.quests.update_one({'id':id},{'$set':{'title':title}})
    db.quests.update_one({'id':id},{'$set':{'content':content}})
    db.quests.update_one({'id':id},{'$set':{'treasure':treasure}})
    db.quests.update_one({'id':id},{'$set':{'date':date}})

    return jsonify({'result': 'success'})

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)