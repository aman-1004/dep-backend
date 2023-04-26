from flask import request, session, Blueprint
from functions import createNewLTCApplication, listLiveApplications
from nonApplicantEndpoints import router as nonApplicantRouter
from models import LTCInfo
import json
from typing import List

router = Blueprint("endpoints", __name__ )
router.register_blueprint(nonApplicantRouter)

#need checking
@router.route('/createNewLTCApplications', methods=['POST'])
def createNewLTCApplicationHandle():
    ltcInfo = request.json
    userInfo = session.get('userInfo')
    print(userInfo)
    createNewLTCApplication(userInfo, ltcInfo)
    return "Done", 200 


#working fine
@router.route('/listLiveLTCApplications', methods=['POST', 'GET'])
def listLiveLTCApplicationHandle():
    userInfo = session.get('userInfo')
    ltcInfos = [ltc.json() for ltc in listLiveApplications(userInfo)]
    return ltcInfos

#working fine
@router.route('/getLTCInfo', methods=['POST'])
def getLTCInfo():
    ltcId = request.json.get('ltcId')
    ltcInfo = LTCInfo.query.filter_by(id=ltcId).first()
    print(ltcInfo.json())
    return ltcInfo.json(), 200 


