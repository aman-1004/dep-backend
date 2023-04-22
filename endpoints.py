from flask import request, session, Blueprint
from functions import createNewLTCApplication
from nonApplicantEndpoints import router as nonApplicantRouter
from models import LTCInfo
import json


router = Blueprint("endpoints", __name__ )
router.register_blueprint(nonApplicantRouter)


@router.route('/createNewLTCApplications', methods=['POST'])
def createNewLTCApplicationHandle():
    print(request.is_json)
    ltcInfo = request.json
    print('ltcInfo is', ltcInfo)
    userInfo = session.get('userInfo')
    createNewLTCApplication(userInfo, ltcInfo)
    return "Done", 401


@router.route('/listLiveLTCApplications', methods=['POST', 'GET'])
def listLiveLTCApplication():
    userInfo = session.get('userInfo')
    ltcInfos = [ltc.json() for ltc in LTCInfo.query.all()]
    
    return ltcInfos

@router.route('/viewLTCApplication')
def viewLTCApplication():
    ltcFormId = request.form.get('ltcFormId')
    ltcInfo = LTCInfo.query.filter_by(id=ltcFormId).first()
    return ltcInfo

@router.route('/addCommentLTCForm')
def addCommentLTCForm():
    comment = request.form.get('comment')
    ltcFormId = request.form.get('ltcFormId')
    ltcInfo = LTCInfo.query.filter_by(id=ltcFormId).first()
    ltcInfo.comments.append(comment)
