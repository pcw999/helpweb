from flask import Flask, render_template, jsonify, request, redirect
from pymongo import MongoClient
from datetime import datetime, timedelta
import json
import jwt
import random

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbjungle

name = "2krlhuhh0dkf"
status = 1

db.test.update_one({'2krlhuhh0dkf' : 1}, {'$set':{'name':'asdf'}})