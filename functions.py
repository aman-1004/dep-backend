from models import User, LTCInfo, db


def checkEmail(emailId):
    foundUser = User.query.filter(User.emailId == emailId).first()
    return foundUser

def createNewLTCApplication(userInfo, formInfo):
    formInfo['userId'] = userInfo.id
    info = LTCInfo(formInfo)
    db.session.add(info)
    db.session.commit()
    print("JSON LTCINFO", info.json())
    pass

def listLiveApplications(userInfo):
    liveLtc = filter(lambda ltc: ltc.stageCurrent != 1, User.query.filter(User.id==userInfo.id).first().ltcInfos)
    return list(liveLtc)


def listLiveTAApplications(userInfo):
    # add Stage current here
    liveTa = filter(lambda ta: True, User.query.filter(User.id==userInfo.id).first().taInfos)
    return list(liveTa)
