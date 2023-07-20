from app import db

class CompTypesDB(db.Model):
    __tablename__ = 'comptypes'

    id = db.Column(db.Integer, primary_key=True)
    folderID = db.Column(db.Integer)
    title = db.Column(db.String(255))
    status = db.Column(db.Integer, default=1)

    def __str__(self):
        return self.title
    
class LogoLib(db.Model):
    __tablename__ = 'logo_lib'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.LargeBinary)
    status = db.Column(db.Integer, default=1)

class CompetitionsDB(db.Model):
    __tablename__ = 'competitions'

    id = db.Column(db.Integer, primary_key=True)
    ownerID = db.Column(db.Integer, default=0)
    title = db.Column(db.String(255))
    typeID = db.Column(db.Integer, default=0)
    properties = db.Column(db.Text)
    status = db.Column(db.Integer, default=1)