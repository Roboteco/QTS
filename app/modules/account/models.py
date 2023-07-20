from app import db

class AccountDB(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(236), nullable=True)
    email = db.Column(db.String(236), nullable=True)
    password = db.Column(db.String(236), nullable=True)
    status = db.Column(db.Integer, default=1)

    def __str__(self):
        return self.name

class RolesUsersDB(db.Model):
    __tablename__ = 'rolesusers'

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    roleID = db.Column(db.Integer)
