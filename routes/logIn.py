from flask import Flask, Blueprint, render_template, request, jsonify
from pymongo import MongoClient

import jwt
import datetime

client = MongoClient('localhost', 27017)
db = client.jungle_week0

logIn_bp = Blueprint('logIn', __name__, url_prefix="/user")

logIn_bp.config = {
    'SECRET_KEY': 'your-secret-key-for-login',
}

@logIn_bp.route("/login")
def logInPage():
  return render_template('/logIn.html')

# 로그인 페이지에서의 로그인 기능
@logIn_bp.route('/feature/login', methods=['POST'])
def logIn():
  data = request.get_json()
  get_id = data['id']
  get_pw = data['pw']

  try:
    db_id = db.user.find_one({"Id": get_id})['Id']
  except:
    return jsonify({"result": "id_fail"})


  if get_id == db.user.find_one({"Id": db_id})['Id'] and get_pw == db.user.find_one({"Id": db_id})['Pw']:
    name = db.user.find_one({"Id": get_id})["Name"]
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    token = jwt.encode({'name': name, 'exp': expiration_time}, logIn_bp.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({'result': 'success', 'token': token, 'user': name})
  else:
    return jsonify({'result' : 'pw_fail'})
