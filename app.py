from flask import Flask

import re

from flask import Flask, render_template, request, jsonify

import json
from bson import ObjectId
from werkzeug.utils import secure_filename
import os

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.jungle_week0

app = Flask(__name__)

# ! 사진 업로드 구현

# * 디렉토리 설정
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# * 파일 확장자 정의
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# * 파일 확장자 확인 함수
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# 메인 페이지
@app.route("/")
def home():
  return render_template('index.html')

@app.route("/user/login")
def logInPage():
  return render_template('logIn.html')

@app.route("/user/signup")
def signUpPage():
  return render_template('signUp.html')

@app.route("/main/list")
def mainPage():
  return render_template('mainPage.html')

@app.route("/user/comment")
def userPage():
  return render_template('userPage.html')

@app.route("/user/writing")
def writePage():
  return render_template('writing.html')

# ! 회원가입
@app.route('/user/feature/signup', methods=['post'])
def singup():
  Name = request.form['name']
  Id = request.form['id']
  Pw = request.form['password']
  Nickname = request.form['nickname']
  Myself = request.form['myself']
  Img = request.files['file']

  if Img and allowed_file(Img.filename):
    filename = secure_filename(Img.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    Img.save(file_path)
  
  doc ={
    "Name":Name,
    "Id":Id,
    "Pw":Pw,
    "Nickname":Nickname,
    "Myself":Myself,
    "Comment":" ",
    "Img":[{'filename': filename, 'path': file_path}],
    "Gkeyword": [{'성실함':0},{'친화적':0},{'꼼꼼함':0},{'끈기있는':0}],
    "Bkeyword": [{'불성실함':0},{'비판적':0},{'비협조적':0},{'의지가 약한':0}],
    "Writed": " "
  }
  db.user.insert_one(doc)
  
  return render_template('index.html')

# ! 교육생 목록 
@app.route('/user/feature/userlist', methods=['get'])
def user_list():
    searched_data = list(db.user.find({}))
    new_data = []

    for data in searched_data:
        gkeywords = [', '.join(list(d.keys())) for d in data['Gkeyword']]
        new_data.append({"Name": data["Name"], "Gkeyword": gkeywords[:3]})

    return render_template('mainPage.html', new_data=new_data)
# 검색
@app.route('/user/feature/search', methods=['post'])
def search():
    user_name = request.form['name']
    searched_data = list(db.user.find({"Name": user_name}))
    new_data = []

    for data in searched_data:
        gkeywords = [', '.join(list(d.keys())) for d in data['Gkeyword']]
        new_data.append({"Name": data["Name"], "Gkeyword": gkeywords[:3]})

    return render_template('mainPage.html', new_data=new_data)


# # 카테고리 정렬
# @app.route('/user/feature/listsort', methods=['post'])
# def listsort():
#   sorted_user = list(db.users.find({}).sort[('name',-1),('gkeyword',-1)])  

# ! 로그인 페이지에서의 로그인 기능
@app.route('/user/feature/login', methods=['POST'])
def ismember():

  # 클라이언트로부터 데이터를 받기
  id_receive = request.form['id_give']
  pw_receive = request.form['pw_give']
  
  # 클라이언트로부터 받은 데이터와 DB의 데이터가 불일치할시, "NoneType" 객체 반환하는 것을 방지하기 위해 try문 작성
  try:
    id = db.user.find_one({"Id": id_receive})['Id']
  except:
    return jsonify({"result": "id_fail"})
  
  try:
    pw = db.user.find_one({"Pw": pw_receive})['Pw']
  except:
    return jsonify({"result": "pw_fail"})
  
  return jsonify({"result": "success"})

# 작성하고 아래로 옮기자
# @app.route('/user/feature/getinfo', methods=['POST'])
# def getInfo():
  
#   id_receive = request.form["id_give"]
#   info = db.user.find_one({"Id": id_receive})
  
#   if info:
#     info["_id"] = str(info["_id"])

#   return jsonify({"result": "success", "user_info": info})

# ! Mac 환경에선 port 번호 5001, 배포 시에는 5000으로 수정
if __name__ == "__main__":
  app.run('0.0.0.0', port=5001, debug=True)
