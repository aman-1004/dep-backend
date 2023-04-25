from models import User, LTCInfo


def checkEmail(emailId):
    foundUser = User.query.filter(User.emailId == emailId).first()
    return foundUser

def createNewLTCApplication(userInfo, formInfo):
    formInfo['userId'] = userInfo.id
    info = LTCInfo(formInfo)
    print("JSON LTCINFO", info.json())
    pass

def listLiveApplications(userInfo):
    liveLtc = filter(lambda ltc: ltc.stageCurrent != 1, User.query.filter(User.id==1).first().ltcInfos)
    return list(liveLtc)

def sectionForward(ltcInfo, stage):
    ltcInfo.stageCurrent = stage
    ltcInfo.stageRedirect = None


def sectionReject(ltcInfo):
    ltcInfo.stageCurrent = -1  # assuming reject stage is -1. make changes if any in future
    ltcInfo.stageRedirect = None


def sectionReview(ltcInfo, stageRedirect):
    ltcInfo.stageCurrent = 0
    ltcInfo.stageRedirect = stageRedirect

