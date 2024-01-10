from flask import Flask

import re

from flask import Flask, render_template, request, jsonify, url_for

import json
from bson import ObjectId
from werkzeug.utils import secure_filename
import os
import uuid

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.jungle_week0

app = Flask(__name__)

######### ? 사진 업로드

# * 디렉토리 설정
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# * 파일 확장자 정의
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

########## ? 업로드 된 사진 불러오기
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# * 파일 확장자 확인 함수
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# 메인 페이지
@app.route("/")
def home():
  return render_template('index.html')

# 로그인 페이지에서의 로그인 기능
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
# 교육생의 정보를 제공하는 API
@app.route('/user/feature/getinfo', methods=['POST'])
def getInfo():
  
  pid_receive = request.form["pid_give"]
  info = db.user.find_one({"Id": pid_receive})
  
  # JSON 형식 중 ObjectId는 BSON 타입이라 ajax에 반환될 때 직렬화해주어야 한다.
  if info:
    info["_id"] = str(info["_id"])

  return jsonify({"result": "success", "user_info": info})

# 교육생의 장단점 키워드를 정렬
@app.route('/user/feature/getkey', methods=['POST'])
def getKey():

  pid_receive = request.form["pid_give"]
  info = db.user.find_one({"Id": pid_receive})
  
  GKey = info["Gkeyword"]
  sorted_Gkey = sorted(GKey, key=lambda x: next(iter(x.values())), reverse=True) # GPT
  print(GKey)
  print(sorted_Gkey)

  BKey = info["Bkeyword"]
  sorted_Bkey = sorted(BKey, key=lambda x: next(iter(x.values())), reverse=True)
  print(BKey)
  print(sorted_Bkey)
  Comments = info["Comment"]
  Nick = info["Nickname"]

  return jsonify({"result": "success", "GKey": sorted_Gkey, "BKey": sorted_Bkey, "Comment": Comments, "Nickname": Nick}) 

@app.route('/user/feature/getdata', methods=['POST'])
def getData():
 # flask의 request.form을 사용하여 key 값인 title을 전달
  pid_receive = request.form["pid_give"]
  comment_receive = request.form["comment_give"]

  # Flask에서 Ajax에서 보내준 문자열 데이터를 parsing하여 JSONArray로 변환
  selectedGKey = json.loads(request.form["selectedGKey"]) 
  selectedBKey = json.loads(request.form["selectedBKey"])

  # DB에서 사용자 정보 가져오기
  user_info = db.user.find_one({"Id": pid_receive})
  if not user_info:
    return jsonify({"result": 'error'})

  # print(user_info)
  # Comment 업데이트 또는 추가
  if type(user_info['Comment']) != None:
    # DB에 comment가 저장돼 있으면 append
    user_info['Comment'].append(comment_receive)
  else:
    # DB에 comment가 없으면 새로운 리스트 생성
    user_info['Comment'] = [comment_receive]


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
  Id = request.form['id']
  Pw = request.form['pw']
  PwConf = request.form['pwConf']
  Name = request.form['name']
  Nickname = request.form['nickname']
  Myself = request.form['myself']
  Img = request.files['img']

  try:
    len(db.user.find({"Id": Id})) == 0 
  except:
    return jsonify({"result": "id_fail"})

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
    "Img":[{'filename': filename, 'path': file_path}],
    "Gkeyword": [{'성실함':0},{'친화적':0},{'꼼꼼함':0},{'끈기있는':0}],
    "Bkeyword": [{'불성실함':0},{'비판적':0},{'비협조적':0},{'의지가 약한':0}],
    "Writed": " "
  }
  db.user.insert_one(doc)
  
  return jsonify({"result": "success"})
  

######### ! 메인 페이지
@app.route("/")
def home():
  return render_template('index.html')

@app.route("/user/login")
def logInPage():
  return render_template('logIn.html')

@app.route("/user/signup")
def signUpPage():
  return render_template('signUp.html')

######### ! 메인페이지 (유저목록)
@app.route("/main/list")
def mainPage():
    searched_data = list(db.user.find({}))
    new_data = []

    for data in searched_data:
        gkeywords = [', '.join(list(d.keys())) for d in data['Gkeyword']]
        new_data.append({"Name": data["Name"], "Gkeyword": gkeywords[:3]})

    return render_template('mainPage.html', new_data=new_data)

######### ! 유저페이지 
@app.route("/user/<user_name>/comment")
def userPage(user_name):
  student = db.user.find({"Name": user_name})

  if student:
    return render_template('userPage.html', student=student)
  else :
    return "교육생 정보를 찾을 수 없습니다.", 404

@app.route("/user/writing")
def writePage():
  return render_template('writing.html')

######### ! 검색
@app.route('/main/search', methods=['post'])
def searchingPage():
    user_name = request.form['name']
    searched_data = list(db.user.find({"Name": user_name}))
    new_data = []

    for data in searched_data:
        gkeywords = [', '.join(list(d.keys())) for d in data['Gkeyword']]
        new_data.append({"Name": data["Name"], "Gkeyword": gkeywords[:3]})

    return render_template('mainPage.html', new_data=new_data)      

# 카테고리 정렬: 가나다순
@app.route('/user/feature/listsort1', methods=['post'])
def listsort1():
  searched_data = list(db.user.find({}).sort('Name', 1))
  new_data = []
  for data in searched_data:
    gkeywords = [', '.join(list(d.keys())) for d in data['Gkeyword']]
    print(gkeywords)
    new_data.append({"Name": data["Name"], "Gkeyword": gkeywords[:3]})
    print(new_data)
  return render_template('mainPage.html', new_data=new_data)

# 한 줄평의 개수를 기준으로 정렬
@app.route('/user/feature/listsort2', methods=['post'])
def listsort2():
    searched_data = list(db.user.find({}))
    sorted_data = sorted(searched_data, key=lambda x: len(x.get('Comment', [])), reverse=True)
    new_data = []
    for data in sorted_data:
        gkeywords = [', '.join(list(d.keys())) for d in data['Gkeyword']]
        new_data.append({"Name": data["Name"], "Gkeyword": gkeywords[:3]})
    return render_template('mainPage.html', new_data=new_data)

# ! Mac 환경에선 port 번호 5001, 배포 시에는 5000으로 수정
if __name__ == "__main__":
  app.run('0.0.0.0', port=5001, debug=True)
