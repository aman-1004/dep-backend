from flask import request, session, Blueprint
from functions import createNewLTCApplication
from models import LTCInfo


router =  Blueprint("nonApplicantEndpoints", __name__)


@router.before_request
def before():
    if (isApplicant(session.get('userInfo').get('roles', {}).get('stageCurrent'))):
        return "You are not authorized", 401


def isApplicant(stageCurrent):
    return stageCurrent == 0


@router.route('/listPending', methods=['POST'])
def listPending():
    handlerInfo = session.get('userInfo')
    return getPendingByStage(handlerInfo.roles.stageCurrent)


def getPendingByStage(stageCurrent):
    ltcInfos = LTCInfo.query.filter_by(stageCurrent=stageCurrent).all()
    return ltcInfos


