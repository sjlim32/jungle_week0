from flask import Blueprint, render_template
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.jungle_week0

main_bp = Blueprint('main', __name__, url_prefix="/main")

# ? 메인페이지 (유저목록)
@main_bp.route("/list")
def mainPage():
    searched_data = list(db.user.find({}))
    new_data = []

    for data in searched_data:
        gkeywords = [', '.join(list(d.keys())) for d in data['Gkeyword']]
        new_data.append({"Name": data["Name"], "Gkeyword": gkeywords[:3]})

    return render_template('mainPage.html', new_data=new_data)

# ? 메인페이지 (검색)
@main_bp.route('/search', methods=['post'])
def searchingPage():
    user_name = request.form['name']
    searched_data = list(db.user.find({"Name": user_name}))
    new_data = []

    for data in searched_data:
        gkeywords = [', '.join(list(d.keys())) for d in data['Gkeyword']]
        new_data.append({"Name": data["Name"], "Gkeyword": gkeywords[:3]})

    return render_template('mainPage.html', new_data=new_data)      

# 카테고리 정렬: 가나다순
@main_bp.route('/user/feature/listsort1', methods=['post'])
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
@main_bp.route('/user/feature/listsort2', methods=['post'])
def listsort2():
    searched_data = list(db.user.find({}))
    sorted_data = sorted(searched_data, key=lambda x: len(x.get('Comment', [])), reverse=True)
    new_data = []
    for data in sorted_data:
        gkeywords = [', '.join(list(d.keys())) for d in data['Gkeyword']]
        new_data.append({"Name": data["Name"], "Gkeyword": gkeywords[:3]})
    return render_template('mainPage.html', new_data=new_data)    