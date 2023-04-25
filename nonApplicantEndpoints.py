from flask import request, session, Blueprint
from functions import createNewLTCApplication
from models import LTCInfo, Comment, User
from datetime import datetime

router =  Blueprint("nonApplicantEndpoints", __name__)

def isApplicant(stageCurrent):
    return stageCurrent == 0

def getPendingByStage(stageCurrent):
    ltcInfos = LTCInfo.query.filter_by(stageCurrent=stageCurrent).all()
    return [ltc.json() for ltc in ltcInfos]


@router.before_request
def before():
    if (isApplicant(session.get('userInfo').get('roles', {}).get('stageCurrent'))):
        return "You are not authorized", 401


@router.route('/listPendingLTCApplication', methods=['POST'])
def listPendingLTCApplication():
    handlerInfo = session.get('userInfo')
    return getPendingByStage(handlerInfo.roles.stageCurrent)


def addCommentLTCForm(comment: str, ltcInfo: LTCInfo):
    ltcInfo.comments.append(Comment(**{"comment": comment, 
                                       "stage": ltcInfo.stageCurrent, 
                                       "created_at": datetime.now()}))


@router.route('/submitHodData')
def submitHodData():
    handlerInfo: User = session.get('userInfo')
    comment: str = request.form.get('comment')
    status: str = request.form.get('status')
    ltcFormId: int = request.form.get('formId')
    ltcInfo: LTCInfo = LTCInfo.query.filter_by(id=ltcFormId).first()
    addCommentLTCForm(comment, ltcInfo)
    if(status == 'ACCEPT'):
        ltcInfo.stageCurrent = handlerInfo.role.nextStage
    else:    
        ltcInfo.stageCurrent = handlerInfo.role.prevStage

    return "200"

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


