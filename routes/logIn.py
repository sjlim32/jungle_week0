from flask import Blueprint, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.jungle_week0

logIn_bp = Blueprint('logIn', __name__, url_prefix="/user")

@logIn_bp.route("/login")
def logInPage():
  return render_template('/logIn.html')

# 로그인 페이지에서의 로그인 기능
@logIn_bp.route('/feature/login', methods=['POST'])
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