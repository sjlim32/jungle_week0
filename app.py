from flask import Flask

from flask import Flask, render_template

app = Flask(__name__)

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

# ! Mac 환경에선 port 번호 5001, 배포 시에는 5000으로 수정
if __name__ == "__main__":
  app.run('0.0.0.0', port=5001, debug=True)
