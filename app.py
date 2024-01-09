from flask import Flask
from flask import Flask, jsonify, render_template
from pymongo import MongoClient
from requests import request


app = Flask(__name__)
# mongoDB 추가
client = MongoClient("localhost", 27017)
db = client.dbjungle

@app.route("/")
def home():
  return render_template('index.html')

@app.route('/ismember', methods=['POST'])
def post_ismember():
  # 클라이언트로부터 데이터를 받기
  id_receive = request.form['id_give']
  pw_receive = request.form['pw_give']
  
  id = db.hanjul.find_one({"id": id_receive})
  pw = db.hanjul.find_one({"pw": pw_receive})
  if id == '':
    if pw == pw_receive:
      return jsonify({"result": "success"})
    else: 
      return jsonify({"result": "pw_fail"})
  else:
    return jsonify({"result": "id_fail"})

@app.route("/user/login")
def logInPage():
  return render_template('logIn.html')

@app.route("/user/signup")
def signUpPage():
  return render_template('signUp.html')

@app.route("/main/list")
def mainPage():
  return render_template('mainPage')

# ! Mac 환경에선 port 번호 5001, 배포 시에는 5000으로 수정
if __name__ == "__main__":
  app.run('0.0.0.0', port=5001, debug=True)
