# from flask import Flask, render_template, jsonify, request, redirect
# from pymongo import MongoClient
# from datetime import datetime, timedelta
# import json
# import jwt
# import random

# app = Flask(__name__)

# client = MongoClient('localhost', 27017)
# db = client.dbjungle

# name = "2krlhuhh0dkf"
# status = 1

# #db.test.update_one({'name' : 'asdf'}, {'$set':{'list':'1'}})

# temp = db.test.find_one({'name':'asdf'})
# temp2 = list(temp['list'])
# temp2.append(3)
# db.test.update_one({'name' : 'asdf'}, {'$set':{'list':temp2}})