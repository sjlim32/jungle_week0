from flask import Blueprint, render_template, request, json, jsonify
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.jungle_week0

getInfo_bp = Blueprint('getinfo', __name__, url_prefix="/user/feature")

# 작성하고 아래로 옮기자
# 교육생의 정보를 제공하는 API
@getInfo_bp.route('/getinfo', methods=['POST'])
def getInfo():
  
  pname_receive = request.form["pname_give"]
  info = db.user.find_one({"Name": pname_receive})

  # JSON 형식 중 ObjectId는 BSON 타입이라 ajax에 반환될 때 직렬화해주어야 한다.
  if info:
    info["_id"] = str(info["_id"])
  
  return jsonify({"result": "success", "user_info": info})

# 교육생의 장단점 키워드를 정렬
@getInfo_bp.route('/getkey', methods=['POST'])
def getKey():
  pname_receive = request.form["pname_give"]
  info = db.user.find_one({"Name": pname_receive})
  
  GKey = info["Gkeyword"]
  sorted_Gkey = sorted(GKey, key=lambda x: next(iter(x.values())), reverse=True) # GPT

  BKey = info["Bkeyword"]
  sorted_Bkey = sorted(BKey, key=lambda x: next(iter(x.values())), reverse=True)
  
  Comments = info["Comment"]
  IsShow_key = next(iter(sorted_Bkey[0]))
  IsShow = sorted_Bkey[0][IsShow_key]
  
  IsWrited = info["Writed"]
  Nick = info["Nickname"]

  return jsonify({"result": "success", "GKey": sorted_Gkey, "BKey": sorted_Bkey,
                  "Comment": Comments, "IsShow": IsShow, "IsWrited": IsWrited, "Nickname": Nick }) 

# 등록 페이지에 저장한 데이터를 DB에 저장
@getInfo_bp.route('/getdata', methods=['POST'])
def getData():
  pname_receive = request.form["pname_give"]
  id_receive = request.form["id_give"]
  comment_receive = request.form["comment_give"]

  # Flask에서 Ajax에서 보내준 문자열 데이터를 parsing하여 JSONArray로 변환
  selectedGKey = json.loads(request.form["selectedGKey"]) 
  selectedBKey = json.loads(request.form["selectedBKey"])

  # DB에서 사용자 정보 가져오기
  user_info = db.user.find_one({"Name": pname_receive})

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

  # print(user_info['Writed'])
  
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
  db.user.update_one({"Name": pname_receive}, {"$set": user_info})

  return jsonify({"result": "success"}) 