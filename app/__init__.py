from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
#import flask_excel as excel
from flask_jwt_extended import (JWTManager, jwt_required, )
from .libs.any_func import getRandomString


# создание экземпляра приложения
app = Flask(__name__, static_folder='static/dist')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/boxing'
app.config['SECRET_KEY'] = 'DFGDYUDHGDHGDHFFDREDFDFAS56743qGDFSdghfgrweryurth4675673534fhgdD'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

# инициализирует расширения
db = SQLAlchemy(app)

# import views - корень 
from . import views

# инициализация Excel 
#excel.init_excel(app)


# инициализация JWT
app.config['JWT_SECRET_KEY'] = '420S14Q53SYG3KI8LZKDOH8DJP2GCFCX2D3ZDUZS3KOYER8J84MU42U611AY959V48RZSLA4T37XCXXDTRJ9MOC75457IZLM49S6F7KB5VHRAE8TQYMMONZ7LOQTC1KRN1PZAEFAV1Q73SPY7A708XFC4A334NY8HPURWG70ZSHML4M00X8V27ROR7XBUZRYJFEQSCWHXR0SN9JINYLV7ESHOF2L44D4GG08D5MHK9L3BIQUPALIDGYKKMK7YMAW'
jwt = JWTManager(app)

app.config['UPLOAD_FOLDER'] = 'uploads'

# создание первого пользователя вручную!!!
#user = User(0, 1)
#print(user.createRoot()) #создание root системы
#print(user.createSuper()) #создание super platform

#подключаем модули

import app.modules.account.controllers as account
app.register_blueprint(account.module, url_prefix='/api/v1/account')

import app.modules.competitions.controllers as competitions
app.register_blueprint(competitions.module, url_prefix='/api/v1/competitions')

