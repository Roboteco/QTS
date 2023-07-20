from sqlalchemy import create_engine
from flask_jwt_extended import (
    create_access_token,
    decode_token,
    )
from .models import AccountDB, RolesUsersDB, db
from app import app
import hashlib

from app.libs.any_func import getRandomString

ACCOUNT_UNKNOWN = 'Uunknown'
ROLE_MABAGERID = 1


class Account():
    userID = 0
    name = ACCOUNT_UNKNOWN

    def __init__(self, userID):
        self.userID = userID
        if userID != 0:
            row = db.session.query(AccountDB).filter(AccountDB.id == userID, AccountDB.status == 1).first()
            if row is not None:
                self.name = row.name
                self.email = row.email

    def exist(self, payload):
        row = db.session.query(AccountDB).filter(AccountDB.email == payload['login']).first()
        return False if row is None else True
    
    def create(self, payload):
        account = AccountDB(name = payload['name'], email = payload['login'], password = hashlib.sha1(payload['password'].encode()).hexdigest(), status=1)
        db.session.add(account)
        db.session.commit()

        rolesusers = RolesUsersDB(userID = account.id, roleID=ROLE_MABAGERID)
        db.session.add(rolesusers)
        db.session.commit()

        jwt = self.getToken(account.id, [ROLE_MABAGERID])
        return {'jwt': jwt}


    def getToken(self, accountID, roles):
        useridentity = {}
        useridentity['a1'] = getRandomString()
        useridentity['accountID'] = accountID
        useridentity['roles'] = roles
        useridentity['a2'] = getRandomString()
        return create_access_token(identity=useridentity, expires_delta=False)

    def getRoles(self):
        rows = db.session.query(RolesUsersDB).filter(RolesUsersDB.userID == self.userID).all()
        self.roles = []
        for row in rows:
            self.roles.append(row.roleID)

    def checkAccount(self, payload):
        row = db.session.query(AccountDB).filter(AccountDB.email == payload['login'],
                                                 AccountDB.password == hashlib.sha1(payload['password'].encode()).hexdigest(), 
                                                 AccountDB.status == 1).first()

        if row != None:
            self.userID = row.id
            self.roles = self.getRoles()
            jwt = self.getToken(row.id, self.roles)
            accountData = {
                'id': row.id,
                'name': row.name,
                'email': row.email,
                'jwt': jwt
            }
            return accountData
        else:
            return None
        
    def getAccountData(self):
        row = db.session.query(AccountDB).filter(AccountDB.id == self.userID,
                                                 AccountDB.status == 1).first()

        if row != None:
            self.roles = self.getRoles()
            jwt = self.getToken(row.id, self.roles)
            accountData = {
                'id': row.id,
                'name': row.name,
                'email': row.email,
                'jwt': jwt
            }
            return accountData
        else:
            return None
