from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
from bson import ObjectId
from werkzeug.utils import secure_filename
import os
from jinja2 import Template
from pymongo import MongoClient
from routes import getInfo_bp, logIn_bp, main_bp
import re, json, os, uuid

app = Flask(__name__)

"""
DB 연결, EC2 server MongoDB용 // 'mongodb://설정한 아이디:비밀번호@내AWS아이피'
배포용으로 변경하면 localhost들도 서버용으로 변경해야 함.
DB주소 수정해야 할 곳(localhost->mongodb://admin:w00mini@43.201.26.201) - logIn.py, getInfo.py
경로 수정해야 할 곳(href에서 주소 앞 43.201.26.201 붙이기)  Signup.html, logIn.html
"""
# client = MongoClient('mongodb://admin:w00mini@43.201.26.201', 27017)
# * DB 연결, local용
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
  try:
    Id = request.form['id']
    Pw = request.form['pw']
    PwConf = request.form['pwConf']
    Name = request.form['name']
    Nickname = request.form['nickname']
    Myself = request.form['myself']
    Img = request.files['img']
  except:
    return jsonify({"result": "fail"})

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
    "Comment":[],
    "Img":{'filename': filename, 'path': file_path},
    "Gkeyword": [{'성실함':0},{'친근함':0},{'긍정맨':0},{'리더쉽':0},{'노력파':0},{'꾀돌이':0},{'엉뚱함':0},{'청결':0},{'부지런':0},{'솔직담백':0}, {'이타적':0}, {'활발':0},{'재치만점':0},{'감성적':0}, {'완벽주의':0}],
    "Bkeyword": [{'게으름':-2},{'다혈질':-2},{'이기적':-2},{'거만':-2}
    ,{'고지식':-2},{'수동적':-2},{'욕쟁이':-2},{'부정파':-2},{'새가슴':-2},{'황소고집':-2},{'더러움':-2},{'잠만보':-2}, {'벌구':-2}, {'건망증':-2},{'욕심쟁이':-2}],
    "Writed": [Name]
  }
  db.user.insert_one(doc)
  
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
