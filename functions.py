from models import User, LTCInfo, db, Notification, Receipt
from flask import request
import uuid, mimetypes, json, os

def checkEmail(emailId):
    foundUser = User.query.filter(User.emailId == emailId).first()
    return foundUser

def createNewLTCApplication(userInfo, formInfo):
    formInfo['userId'] = userInfo.id
    info = LTCInfo(formInfo)
    for file in request.files.getlist('file'):
        fileName = uuid.uuid4().hex + mimetypes.guess_extension(file.mimetype)
        base_path = os.path.join(os.path.dirname(__file__), 'receipts')
        filePath = f"{base_path}/{fileName}"
        info.receipts.append(Receipt(filePath))
        print(file.save(filePath))

    db.session.add(info)
    db.session.commit()
    print("JSON LTCINFO", info.json())
    return info

def listLiveApplications(userInfo):
    liveLtc = filter(lambda ltc: ltc.stageCurrent != 1 and ltc.stageCurrent <= 100, User.query.filter(User.id==userInfo.id).first().ltcInfos)
    return list(liveLtc)


def listLiveTAApplications(userInfo):
    # add Stage current here
    liveTa = filter(lambda ta: True, User.query.filter(User.id==userInfo.id).first().taInfos)
    return list(liveTa)


def addNotification(userId, message):
    user = User.query.filter(User.id == userId).first()
    user.notifications.append(Notification(message))
    db.session.commit()