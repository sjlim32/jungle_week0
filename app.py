from flask import Flask, render_template, request, jsonify, url_for
from bson import ObjectId
from werkzeug.utils import secure_filename
import os

from jinja2 import Template

from pymongo import MongoClient

from routes import getInfo_bp, logIn_bp, main_bp

import re, json, os, uuid

app = Flask(__name__)

# * DB 연결
client = MongoClient('localhost', 27017)
db = client.jungle_week0

# * Blueprint 설정
app.register_blueprint(getInfo_bp)
app.register_blueprint(logIn_bp)
app.register_blueprint(main_bp)

# ! Router
@app.route("/")
def home():
  return render_template('index.html')  

@app.route("/user/<user_name>/comment")
def userPage(user_name):
  student = db.user.find({"Name": user_name})

  if student:
    return render_template('userPage.html', student=student)
  else :
    return "교육생 정보를 찾을 수 없습니다.", 404

@app.route("/user/signup")
def signUpPage():
  return render_template('signUp.html')

@app.route("/user/writing")
def writePage():
  return render_template('writing.html')  

# ! API

# ? 회원가입
@app.route('/user/feature/signup', methods=['post'])
def singup():
  Id = request.form['id']
  Pw = request.form['pw']
  PwConf = request.form['pwConf']
  Name = request.form['name']
  Nickname = request.form['nickname']
  Myself = request.form['myself']
  Img = request.files['img']

  # try:
  #   len(db.user.find({"Id": Id})) == 0 
  # except:
  #   return jsonify({"result": "id_fail"})

  # try:
  #   pw = db.user.find_one({"Pw": pw_receive})['Pw']
  # except:
  #   return jsonify({"result": "pw_fail"})

  if Img and allowed_file(Img.filename):
    filename = str(uuid.uuid4()) + Name
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename )
    Img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  
  doc ={
    "Id":Id,
    "Pw":Pw,
    "Name":Name,
    "Nickname":Nickname,
    "Myself":Myself,
    "Comment":["gg","kk"],
    "Img":{'filename': filename, 'path': file_path},
    "Gkeyword": [{'성실함':0},{'친화적':0},{'꼼꼼함':0},{'끈기있는':0}],
    "Bkeyword": [{'불성실함':0},{'비판적':0},{'비협조적':0},{'의지가 약한':0}],
    "Writed": " "
  }
  db.user.insert_one(doc)
  
  return render_template('index.html')


# 교육생의 장단점 키워드를 정렬
@app.route('/user/feature/getkey', methods=['POST'])
def getKey():

  pid_receive = request.form["pid_give"]
  info = db.user.find_one({"Id": pid_receive})
  
  GKey = info["Gkeyword"]
  sorted_Gkey = sorted(GKey, key=lambda x: next(iter(x.values())), reverse=True) # GPT

  BKey = info["Bkeyword"]
  sorted_Bkey = sorted(BKey, key=lambda x: next(iter(x.values())), reverse=True)
  # print(BKey)
  # print(sorted_Bkey)
  Comments = info["Comment"]
  # Nick = info["Nickname"]
  IsWrited = info["Writed"]

  IsShow_key = next(iter(sorted_Bkey[0]))
  IsShow = sorted_Bkey[0][IsShow_key]
  # print(IsShow)

  return jsonify({"result": "success", "GKey": sorted_Gkey, "BKey": sorted_Bkey, "Comment": Comments,
                  "IsWrited": IsWrited, "IsShow": IsShow }) 

@app.route('/user/feature/getdata', methods=['POST'])
def getData():
 # flask의 request.form을 사용하여 key 값인 title을 전달
  pid_receive = request.form["pid_give"]
  id_receive = request.form["id_give"]
  comment_receive = request.form["comment_give"]

  # Flask에서 Ajax에서 보내준 문자열 데이터를 parsing하여 JSONArray로 변환
  selectedGKey = json.loads(request.form["selectedGKey"]) 
  selectedBKey = json.loads(request.form["selectedBKey"])

  # DB에서 사용자 정보 가져오기
  user_info = db.user.find_one({"Id": pid_receive})
  if not user_info:
    return jsonify({"result": 'error'})

  # Comment 업데이트 또는 추가
  if type(user_info['Comment']) != None:
    # DB에 comment가 저장돼 있으면 append
    user_info['Comment'].append(comment_receive)
  else:
    # DB에 comment가 없으면 새로운 리스트 생성
    user_info['Comment'] = [comment_receive]

  # Writed 업데이트 또는 추가하기
  if 'Writed' not in user_info:
    user_info['Writed'] = [id_receive]
  elif isinstance(user_info['Writed'], str):
    user_info['Writed'] = [user_info['Writed'], id_receive]
  else:
    user_info['Writed'].append(id_receive)

  print(user_info['Writed'])
  
  # GKeyword 업데이트
  for g_key in selectedGKey:
      for db_g_key in user_info['Gkeyword']:
        if g_key in db_g_key:
          db_g_key[g_key] += 1

    # BKeyword 업데이트
  for b_key in selectedBKey:
      for db_b_key in user_info['Bkeyword']:
        if b_key in db_b_key:
          db_b_key[b_key] += 1

  # print(user_info)
  # DB 업데이트
  db.user.update_one({"Id": pid_receive}, {"$set": user_info})

  return jsonify({"result": "success"}) 

# ? 사진 업로드
# * 디렉토리 설정
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# * 파일 확장자 정의
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# * 파일 확장자 확인 함수
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# * 사진 불러오기
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ! Mac 환경에선 port 번호 5001, 배포 시에는 5000으로 수정
if __name__ == "__main__":
  app.run('0.0.0.0', port=5001, debug=True)
