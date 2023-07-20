import json
import base64
from ast import literal_eval
from .models import CompTypesDB, LogoLib, CompetitionsDB, db

COMP_UNKNOWN = 'Uunknown'

class Competition():
  compID = 0
  name = COMP_UNKNOWN
  accountID = 0

  def __init__(self, compID):
    self.compID = compID

  def getCompetitions(self, folderID):
    print('==>', folderID)
    comps = []
    rows = db.session.query(CompetitionsDB).filter(CompetitionsDB.typeID == folderID, CompetitionsDB.ownerID == self.accountID, CompetitionsDB.status == 1).all()
    for row in rows:
      comps.append({
        'id': row.id,
        'title': row.title,
        'properties': base64.b64decode(row.properties).decode('utf-8')
      })
    return comps


  def getCompTypesByFolderID(self, folderID, addCompetition):
    compTypes = []
    rows = db.session.query(CompTypesDB).filter(CompTypesDB.folderID == folderID, CompTypesDB.status == 1).all()
    for row in rows:
      item ={
        'id': row.id,
        'title': row.title,
        'subfolders': self.getCompTypesByFolderID(row.id, addCompetition)
      }
      if addCompetition:
        item['compettions'] = self.getCompetitions(row.id)
      compTypes.append(item)

    return compTypes

  def compListAll(self, accountID):
    self.accountID = accountID
    compAll = self.getCompTypes(True)
    print(compAll)
    return compAll


  def getCompTypes(self, addCompetition = False):
    return self.getCompTypesByFolderID(0, addCompetition)
  
  def uploadLogoImg(self, data):
    logo = LogoLib(body = data, status=1)
    db.session.add(logo)
    db.session.commit()
    
    return logo.id
  
  def getLogoImg(self, baseURL):
    logoLib = []
    rows = db.session.query(LogoLib).filter(LogoLib.status == 1).all()
    for row in rows:
      item ={
        'id': row.id,
        'url': baseURL+'/'+str(row.id)
      }
      logoLib.append(item)

    return logoLib

  def getLogoBodyById(self, logoID):
    row = db.session.query(LogoLib).filter(LogoLib.id == logoID).first()
    return row.body
  
  def deleteLogo(self, logoID):
    db.session.query(LogoLib).filter(LogoLib.id == logoID).update({ 'status': 0})
    db.session.commit()

  def update(self, accountID,  compData):
    if compData['id'] == 0:
      properties = base64.b64encode(json.dumps(compData).encode('utf-8')).decode('utf-8')
      competition = CompetitionsDB(ownerID = accountID, title = compData['name'], typeID = compData['type'], properties = properties, status=1)
      db.session.add(competition)
      db.session.commit()

    else:
      print('exist')

    return competition.id