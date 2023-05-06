from flask import request, session, Blueprint
from functions import createNewLTCApplication
from models import LTCInfo, Comment, User, db, TAInfo
from datetime import datetime

router =  Blueprint("nonApplicantEndpoints", __name__)

def isApplicant(stageCurrent):
    return stageCurrent == 0

def getPendingByStage(stageCurrent):
    ltcInfos = LTCInfo.query.filter_by(stageCurrent=stageCurrent).all()
    return [ltc.json() for ltc in ltcInfos]


@router.before_request
def before():
    if (isApplicant(session.get('userInfo').role.stageCurrent)):
        return "You are not authorized", 401


@router.route('/listPendingLTCApplication', methods=['POST'])
def listPendingLTCApplication():
    handlerInfo = session.get('userInfo')
    return getPendingByStage(handlerInfo.role.stageCurrent)


def addCommentLTCForm(comment: str, ltcInfo: LTCInfo, handlerId):
    ltcInfo.comments.append(Comment(**{"comment": comment, 
                                       "handlerId": handlerId, 
                                       "created_at": datetime.now()}))


@router.route('/submitHodData', methods=["POST"])
def submitHodData():
    handlerInfo: User = session.get('userInfo')
    # print(request.json)
    comment: str = request.json.get('comment')
    status: str = request.json.get('status')
    ltcFormId: int = request.json.get('formId')
    print([comment, status, ltcFormId])
    ltcInfo: LTCInfo = LTCInfo.query.filter_by(id=ltcFormId).first()
    addCommentLTCForm(comment, ltcInfo, handlerId=handlerInfo.id)
    if(status == 'ACCEPT'):
        ltcInfo.stageCurrent = handlerInfo.role.nextStage
    else:    
        ltcInfo.stageCurrent = handlerInfo.role.prevStage
    
    # print([comment.json() for comment in ltcInfo.comments])
    # # print(ltcInfo.json())
    db.session.commit()

    return "200", 200 

@router.route('/submitEstabData', methods=['POST'])
def submitEstabData():
    print("Inside Estab Function")
    print(request.json)
    return submitHodData()


@router.route('/submitAccountsData', methods=['POST'])
def submitAccountsData():
    return submitHodData()


@router.route('/submitAuditData', methods=['POST'])
def submitAuditData():
    return submitHodData()


@router.route('/submitDeanData', methods=['POST'])
def submitDeanData():
    return submitHodData()

@router.route('/submitRegistrarData', methods=['POST'])
def submitRegistrarData():
    return submitHodData()


@router.route('/getComments', methods=['POST'])
def getComments():
    ltcFormId = request.json.get('ltcId')
    # print('ltcId', ltcId)
    # ltcInfo = LTCInfo.query.filter(LTCInfo.id==ltcId).first()
    ltcInfo: LTCInfo = LTCInfo.query.filter_by(id=ltcFormId).first()
    
    return [comment.json() for comment in ltcInfo.comments]
    # return {}


def getPendingTAByStage(stageCurrent):
    taInfos = TAInfo.query.filter_by(stageCurrent=stageCurrent).all()
    print([ta.json() for ta in taInfos])
    return [ta.json() for ta in taInfos]


@router.route('/listPendingTAApplication', methods=['POST'])
def listPendingTAApplication():
    handlerInfo = session.get('userInfo')
    return getPendingTAByStage(handlerInfo.role.stageCurrent)


def addCommentLTCForm(comment: str, ltcInfo: LTCInfo, handlerId):
    ltcInfo.comments.append(Comment(**{"comment": comment, 
                                       "handlerId": handlerId, 
                                       "created_at": datetime.now()}))

def addCommentTAForm(comment: str, taInfo: TAInfo, handlerId):
    taInfo.comments.append(Comment(**{"comment": comment, 
                                       "handlerId": handlerId, 
                                       "created_at": datetime.now()}))

@router.route('/submitTAHodData', methods=["POST"])
def submitTAHodData():
    handlerInfo: User = session.get('userInfo')
    # print(request.json)
    comment: str = request.json.get('comment')
    status: str = request.json.get('status')
    taFormId: int = request.json.get('formId')
    taInfo: TAInfo = TAInfo.query.filter_by(id=taFormId).first()
    addCommentTAForm(comment, taInfo, handlerId=handlerInfo.id)
    if(status == 'ACCEPT'):
        taInfo.stageCurrent = handlerInfo.role.nextStage
    else:    
        taInfo.stageCurrent = handlerInfo.role.prevStage
    
    # print([comment.json() for comment in ltcInfo.comments])
    # # print(ltcInfo.json())
    db.session.commit()

    return "200", 200 


@router.route('/submitTAEstabData', methods=['POST'])
def submitTAEstabData():
    return submitTAHodData()


@router.route('/submitTAAccountsData', methods=['POST'])
def submitTAAccountsData():
    return submitTAHodData()


@router.route('/submitTAAuditData', methods=['POST'])
def submitTAAuditData():
    return submitTAHodData()


@router.route('/submitTADeanData', methods=['POST'])
def submitTADeanData():
    return submitTAHodData()

@router.route('/submitTARegistrarData', methods=['POST'])
def submitTARegistrarData():
    return submitTAHodData()


@router.route('/getTAComments', methods=['POST'])
def getTAComments():
    taFormId = request.json.get('taId')
    # print('ltcId', ltcId)
    # ltcInfo = LTCInfo.query.filter(LTCInfo.id==ltcId).first()
    taInfo: TAInfo = TAInfo.query.filter_by(id=taFormId).first()
    
    return [comment.json() for comment in taInfo.comments]
    # return {}