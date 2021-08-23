from flask import Flask, request, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

from sqlalchemy.sql.elements import Null

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def hello_world():
    return jsonify({
            'status':  1 ,
            'message' : 'API services running at all endpoints'
    })
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# User Class/Model
class User(db.Model):
  __tablename__ = 'User'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), unique=True)
  email = db.Column(db.String(200))
  phone = db.Column(db.String(20))
  password = db.Column(db.String(30))

  def __init__(self, username, email, phone, password):
    self.username = username
    self.email = email
    self.phone = phone
    self.password = password

# User Schema
class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'username', 'email', 'district', 'phone' , 'password')

# Init schema
user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)

@app.route('/signup', methods=['POST'])
def signup():
  username = request.json['username']
  username2 = email2 = User.query.get(username)
  if username==username2:
    return jsonify(
    success= 0 ,
    error_message = "Username Already Exists")
  else:
    email = request.json['email']
    email2 = User.query.get(email)
    if email==email2:
        return jsonify(
        success= 0 ,
        error_message = "Email Already Exists")
    else:
        phone = request.json['phone']
        password = request.json['password']
        new_user = User(username, email, phone , password)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user)

  
@app.route('/allusers', methods=['GET'])
def allusers():
  all_users = User.query.all()
  result = users_schema.dump(all_users)
  return jsonify(result.data)
# Get Single User
#id
@app.route('/user/id/<id>', methods=['GET'])
def get_userid(id):
  user = User.query.get(id)
  return user_schema.jsonify(user)
#email
@app.route('/user/email/<email>', methods=['GET'])
def get_useremail(email):
  user = User.query.get(email)
  return user_schema.jsonify(user)
#username
@app.route('/user/username/<username>', methods=['GET'])
def get_userusername(username):
  user = User.query.get(username)
  return user_schema.jsonify(user)
#update user
@app.route('/user/id/<id>', methods=['PUT'])
def update_userid(id):
  user = User.query.get(id)
  username = request.json['username']
  email = request.json['email']
  phone = request.json['phone']
  user.username = username
  user.email = email
  user.phone = phone
  db.session.commit()
  return user_schema.jsonify(user)

#email
@app.route('/user/email/<email>', methods=['PUT'])
def update_useremail(email):
  user = User.query.get(email)
  username = request.json['username']
  email = request.json['email']
  phone = request.json['phone']
  user.username = username
  user.email = email
  user.phone = phone
  db.session.commit()
  return user_schema.jsonify(user)

#phone
#email
@app.route('/user/phone/<phone>', methods=['PUT'])
def update_userphone(phone):
  user = User.query.get(phone)
  username = request.json['username']
  email = request.json['email']
  phone = request.json['phone']
  user.username = username
  user.email = email
  user.phone = phone
  db.session.commit()
  return user_schema.jsonify(user)
def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True
@app.route('/login', methods=['POST'])
def login():
  email = request.json['email']
  password = request.json ['password']
  if isBlank(email) or isBlank(password):
      return jsonify(unsucessful= 201,
            reason ="S0me Fileds Empty")
  else:
    existemail = db.session.query(User.email).filter_by(email=email).first()
    if existemail is not None:
        existpassword = db.session.query(User.password).filter_by(password=password).first()
        if existpassword is not None:
            return jsonify(sucessful =200,
                    data ={'username' :User.username,
                    'phone': User.phone,
                    'district': User.district})
        else:
                return jsonify(unsucessful= 201,
                reason ="wrong password")
    else:
            return jsonify(unsucessful= 201,
            data ="wrong email")
    





if __name__ == '__main__':
    app.run()