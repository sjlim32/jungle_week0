from flask import Flask

from flask import Flask, render_template, request

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.jungle_week0

app = Flask(__name__)

# 회원가입
@app.route('/user/singup', methods=['get'])
def singup():
  Name = request.args.get('Name')
  Id = request.args.get('Id')
  Pw = request.args.get('Pw')
  Nickname = request.args.get('Nickname')
  Myself = request.args.get('Myself')
  Img = request.args.get('Img')
  doc ={
    "Name":Name,
    "Id":Id,
    "Pw":Pw,
    "Nickname":Nickname,
    "Myself":Myself,
    "Comment":" ",
    "Img":Img,
    "Gkeyword": [{'키워드1':0},{'키워드2':0}],
    "Bkeyword": [{'키워드3':0},{'키워드4':0}],
    "Writed": " "
  }
  db.user.insert_one(doc)

  # 키워드, 코멘트 넣기
# @app.route('/user/comment', methods=['post']) 
# def comment(Id):
#   input_gkeyword = request.args.get('Gkeyword')
#   input_bkeyword = request.args.get('Bkeyword')
#   input_comment = request.args.get('Comment')
#   db.users.update_one({'name':Id},{'$set':{'Comment':input_comment}})

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
  return render_template('mainPage')

# ! Mac 환경에선 port 번호 5001, 배포 시에는 5000으로 수정
if __name__ == "__main__":
  app.run('0.0.0.0', port=5001, debug=True)
