# 6C/19090089/Miftakhul Mubarrok 
# 6C/19090089/Utari Cahyaningsih

import os, random, string

from flask import Flask
from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "user.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Bearer')

class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
  password = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
  token = db.Column(db.String(225), unique=True, nullable=True, primary_key=False)

@app.route("/addUser", methods=["POST"])
def add_user():
  username = request.form['username']
  password = request.form['password']

  newUser = User(username=username, password=password)

  db.session.add(newUser)
  db.session.commit()
  return jsonify({
    'msg': 'Berhasil menambahkan user baru',
    'username': username,
    'password': password,
    'status': 200
  })
  
# tulis command CURL utk request end point ini lengkap dengan data body jsonnya
@app.route("/api/v1/login", methods=["POST"])
def login():
  username = request.form['username']
  password = request.form['password']

  user = User.query.filter_by(username = username, password = password)

  if user:
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    User.query.filter_by(username=username, password=password).update({'token': token})
    db.session.commit()

    return jsonify({
    'msg': 'Login telah berhasil, selamat datang kembali',
    'username': username,
    'password': password,
    'status': 200
    })
  
  else:
    return jsonify({
      'msg': 'Login gagal',
      'status': 401,
    })

# tulis command line CURL utk request end point ini lengkap dengan data body jsonnya
@app.route("/api/v2/users/info", methods=["POST"])
def info():
  token = request.values.get('token')
  user = User.query.filter_by(token=token).first()
  if user:
    return jsonify({
      'msg': 'get data user telah berhasil',
      'username': user.username,
      'status': 200
    })
  else:
    return jsonify({
      'msg': 'token tidak valid'
    })

if __name__ == '__main__':
  app.run(debug = True, port=8080)