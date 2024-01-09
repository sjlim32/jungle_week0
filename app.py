from flask import Flask

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
  return render_template('index.html')

# ! Mac 환경에선 port 번호 5001, 배포 시에는 5000으로 수정
if __name__ == "__main__":
  app.run('0.0.0.0', port=5001, debug=True)
