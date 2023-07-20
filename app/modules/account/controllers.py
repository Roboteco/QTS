from ast import literal_eval
import base64
import time

from flask import (
    Blueprint,
    request,
    make_response,
)

from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity,
    get_current_user
)

from flask_cors import cross_origin

from app import app
from app import jwt

module = Blueprint('account', __name__)
from .account import Account,  ACCOUNT_UNKNOWN



@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    # параметры текущего пользовтаеля - не удалять!
    return jwt_data['sub']

# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    if not 'accountID' in jwt_payload['sub']:
        return True
    if not 'roles' in jwt_payload['sub']:
        return True
    account = Account(jwt_payload['sub']['accountID'])
    if account.name == ACCOUNT_UNKNOWN:
        return True
    return False # False означает, что токен хороший

@module.route('/signup', methods=['POST'])
def signup():
    try:
        Body = literal_eval(request.data.decode('utf8'))
        payload = {}
        payload['name'] = base64.b64decode(Body['name']).decode('utf-8')
        payload['login'] = base64.b64decode(Body['email']).decode('utf-8')
        payload['password'] = base64.b64decode(Body['password']).decode('utf-8')
    except:
        return make_response('{"error" : "JSON data corrupt"}', 422) 

    account = Account(0)
    if account.exist(payload):
        return make_response('{"error" : "Такой аккаунт уже существует"}', 422) 
    
    responseData = account.create(payload)

    return responseData

@module.route('/signin', methods=['POST'])
def signin():
    try:
        Body = literal_eval(request.data.decode('utf8'))
        payload = {}
        payload['login'] = base64.b64decode(Body['email']).decode('utf-8')
        payload['password'] = base64.b64decode(Body['password']).decode('utf-8')
    except:
        return make_response('{"error" : "JSON data corrupt"}', 422) 

    account = Account(0)
    accountData = account.checkAccount(payload)
    if accountData == None:
        return make_response('{"error" : "Аккаунт не найден"}', 401) 

    return accountData

@module.route('/validateJWT/<string:jwt>', methods=['GET'])
@jwt_required()
def validateJWT(jwt):
    userJWT_data = get_current_user()
    account = Account(userJWT_data['accountID'])
    accountData = account.getAccountData()
    if accountData == None:
        return make_response('{"error" : "Аккаунт не найден"}', 401) 

    return accountData


    #print(userJWT_data)
    return {}
    '''
    try:
        Body = literal_eval(request.data.decode('utf8'))
        payload = {}
        payload['login'] = base64.b64decode(Body['email']).decode('utf-8')
        payload['password'] = base64.b64decode(Body['password']).decode('utf-8')
    except:
        return make_response('{"error" : "JSON data corrupt"}', 422) 

    account = Account(0)
    accountData = account.getAccountData(payload)
    if accountData == None:
        return make_response('{"error" : "Аккаунт не найден"}', 401) 

    return accountData
'''