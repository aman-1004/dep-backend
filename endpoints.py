from flask import request, session, Blueprint
from functions import createNewLTCApplication, listLiveApplications, listLiveTAApplications
from nonApplicantEndpoints import router as nonApplicantRouter
from models import LTCInfo, TAInfo, db
import json
from typing import List

router = Blueprint("endpoints", __name__)
router.register_blueprint(nonApplicantRouter)

# need checking


@router.route('/createNewLTCApplications', methods=['POST'])
def createNewLTCApplicationHandle():
    ltcInfo = request.json
    userInfo = session.get('userInfo')
    print(userInfo)
    createNewLTCApplication(userInfo, ltcInfo)
    return "Done", 200


# working fine
@router.route('/listLiveLTCApplications', methods=['POST', 'GET'])
def listLiveLTCApplicationHandle():
    userInfo = session.get('userInfo')
    ltcInfos = [ltc.json() for ltc in listLiveApplications(userInfo)]
    return ltcInfos

# working fine


@router.route('/getLTCInfo', methods=['POST'])
def getLTCInfo():
    ltcId = request.json.get('ltcId')
    ltcInfo = LTCInfo.query.filter_by(id=ltcId).first()
    print(ltcInfo.json())
    # return ltcInfo.json(), 200
    return 200


@router.route('/createNewTAApplication', methods=['POST'])
def createNewTAAApplicationHandle():
    journeyDetails = request.json.get('journeyDetails')
    userInfo = session.get('userInfo')
    ltcId = request.json.get('ltcId')
    taInfo = TAInfo(userId=userInfo.id,
                    ltcId=ltcId,
                    journeyDetails=journeyDetails)
    db.session.add(taInfo)
    db.session.commit()
    print(taInfo.json())
    # print(taInfo.json())
    return "Done", 200


@router.route('/listLiveTAApplications', methods=['POST'])
def listLiveTAApplicationsHandle():
    userInfo = session.get('userInfo')
    taInfos = [ta.json() for ta in listLiveTAApplications(userInfo)]
    return taInfos
    pass


@router.route('/getTAInfo', methods=['POST'])
def getTAInfo():
    taId = request.json.get('taId')
    taInfo = TAInfo.query.filter_by(id=taId).first()
    print(taInfo.json())
    # return taInfo.json(), 200
    return 2