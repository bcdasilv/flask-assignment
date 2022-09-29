from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import random
import string
from model_mongodb_refactored import User


app = Flask(__name__)

#CORS stands for Cross Origin Requests.
CORS(app) #Here we'll allow requests coming from any domain. Not recommended for production environment.

users = { 
    'users_list' :
    [
        {  
            'id' : 'xyz789',
            'name' : 'Charlie',
            'job': 'Janitor',
        },
        {
            'id' : 'abc123',            
            'name': 'Mac',
            'job': 'Bouncer',
        },
        {
            'id' : 'ppp222',            
            'name': 'Mac',
            'job': 'Professor',
        },        
        {
            'id' : 'yat999',            
            'name': 'Dee',
            'job': 'Aspring actress',
        },
        {
             'id' : 'zap555',           
            'name': 'Dennis',
            'job': 'Bartender',
        }
    ]
}

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        search_username = request.args.get('name')
        search_job = request.args.get('job')
        users = find_users(search_username, search_job)
        return {"users_list": users}
    elif request.method == 'POST':
        userToAdd = request.get_json()
        newUser = User(userToAdd)
        if newUser.save():
            resp = jsonify(newUser), 201
        else :
            resp = jsonify({"error": "Object insertion error"}), 422
        return resp

@app.route('/users/<id>', methods=['GET', 'DELETE', 'PUT'])
def get_user(id):
    user = User({"_id":id})
    if request.method == 'GET':
        if user.reload() :
            return user
    elif request.method == 'DELETE':
        if (user.remove() == 1):
            resp = jsonify(),204
            return resp            
    elif request.method == 'PUT':
        fields = request.get_json()
        if user.update_fields(fields) == 1 :
            resp = jsonify(user), 201
            return resp
    return jsonify({"error": "User not found"}), 404 

def find_users(username, job):
    if username and job :
        return User().find_by_name_job(username, job)
    elif username :
        return User().find_by_name(username)
    else :
        return User().find_all()
    