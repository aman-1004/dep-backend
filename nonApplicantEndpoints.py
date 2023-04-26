from flask import request, session, Blueprint
from functions import createNewLTCApplication
from models import LTCInfo, Comment, User, db
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

@router.route('/submitEstabData')
def submitEstabData():
    return submitHodData()


@router.route('/submitAccountsData')
def submitAccountsData():
    return submitHodData()


@router.route('/submitAuditData')
def submitAuditData():
    return submitHodData()


@router.route('/submitDeanData')
def submitDeanData():
    return submitHodData()

@router.route('/submitRegistrarData')
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