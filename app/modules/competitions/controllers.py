from ast import literal_eval
from werkzeug.utils import secure_filename
import base64
import os
import io

from flask import (
    Blueprint,
    request,
    send_file,
    make_response,
)

from flask_jwt_extended import (
    jwt_required, 
    get_current_user
)

from app import app
from app import jwt
from .competition import Competition

module = Blueprint('competitions', __name__)


@module.route('/all', methods=['GET'])
@jwt_required()
def compListAll():
    userJWT_data = get_current_user()

    comp = Competition(0)
    compListAll = comp.compListAll(userJWT_data['accountID'])

    return {'list': compListAll}

@module.route('/update', methods=['POST'])
@jwt_required()
def update():
    userJWT_data = get_current_user()
    try:
        Body = literal_eval(request.data.decode('utf8').replace('null', 'None'))
    except:
        return make_response('{"error" : "Body format - not correct"}', 422) 

    comp = Competition(0)
    compID = comp.update(userJWT_data['accountID'], Body)
    return {'compID': compID}



@module.route('/types', methods=['GET'])
@jwt_required()
def compTypes():
    comp = Competition(0)
    compTypes = comp.getCompTypes()

    return {'compTypes': compTypes}

@module.route('/img_logo', methods=['POST'])
@jwt_required()
def imgLogo():
    loadedFile = request.files['file']
    print(loadedFile)
    source_filename = secure_filename(loadedFile.filename)
    loadedFile.save(source_filename)
    with open(source_filename, 'rb') as f:
        data = f.read()
        f.close()
    os.remove(source_filename)

    comp = Competition(0)
    imgID = comp.uploadLogoImg(data)

    return {'imgID': imgID}

@module.route('/imp_logo', methods=['GET'])
@jwt_required()
def getLogoLib():
    # строим url для скачивания картинки
    urls = request.url.split('/')
    urls.pop()
    urls.append('logo')
    url = '/'.join(urls)

    # формируем список логотипов
    comp = Competition(0)
    logoLib = comp.getLogoImg(url)

    return {'logoLib':logoLib}

@module.route('/logo/<int:logoID>', methods=['GET'])
def getLogo(logoID):

    # формируем список логотипов
    comp = Competition(0)
    logoBody = comp.getLogoBodyById(logoID)

    return send_file(io.BytesIO(logoBody), str(logoID)+'.jpg')


@module.route('/logo/delete/<int:logoID>', methods=['POST'])
@jwt_required()
def imgLogo_delete(logoID):
    comp = Competition(0)
    comp.deleteLogo(logoID)

    return {}


