from flask import request, session, Blueprint
from functions import createNewLTCApplication, listLiveApplications, listLiveTAApplications, listDoneLTCApplications
from nonApplicantEndpoints import router as nonApplicantRouter
from models import LTCInfo, TAInfo, db, Notification, User, Receipt
import uuid, mimetypes, json, os
from typing import List

router = Blueprint("endpoints", __name__)
router.register_blueprint(nonApplicantRouter)

# need checking

def uploadReceipts(ltc):
    return "what"

@router.route('/createNewLTCApplications', methods=['POST'])
def createNewLTCApplicationHandle():
    ltcInfo = json.loads(request.form['json'])
    userInfo = session.get('userInfo')
    print(userInfo)
    ltc = createNewLTCApplication(userInfo, ltcInfo)
    return "Done", 200

@router.route('/createNewTAApplication', methods=['POST'])
def createNewTAAApplicationHandle():
    json_data = json.loads(request.form['json'])
    journeyDetails = json_data.get('journeyDetails')
    userInfo = session.get('userInfo')
    ltcId = json_data.get('ltcId')
    LTCInfo.query.filter(LTCInfo.id == ltcId).first().role.stageCurrent = 101
    taInfo = TAInfo(userId=userInfo.id,
                    ltcId=ltcId,
                    journeyDetails=journeyDetails)

    for file in request.files.getlist('file'):
        fileName = uuid.uuid4().hex + mimetypes.guess_extension(file.mimetype)
        base_path = os.path.join(os.path.dirname(__file__), 'receipts')
        filePath = f"{base_path}/{fileName}"
        taInfo.receipts.append(Receipt(filePath))
        print(file.save(filePath))

    db.session.add(taInfo)
    db.session.commit()
    print(taInfo.json())
    # print(taInfo.json())
    return "Done", 200

# working fine
@router.route('/listLiveLTCApplications', methods=['POST', 'GET'])
def listLiveLTCApplicationHandle():
    userInfo = session.get('userInfo')
    ltcInfos = [ltc.json() for ltc in listLiveApplications(userInfo)]
    return ltcInfos

# working fine
@router.route('/listDoneLTCApplications', methods=['POST'])
def listDoneLTCApplicationsHandle():
    userInfo = session.get('userInfo')
    taInfos = [ta.json() for ta in listDoneLTCApplications(userInfo)]
    return taInfos
    pass

@router.route('/getLTCInfo', methods=['POST'])
def getLTCInfo():
    ltcId = request.json.get('ltcId')
    ltcInfo = LTCInfo.query.filter_by(id=ltcId).first()
    if(ltcInfo):
        print(ltcInfo.json())
        return ltcInfo.json(), 200
    # return ltcInfo.json(), 200
    return {}, 400



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
    print(taId)
    print(taInfo.json())
    if(taInfo):
        print(taInfo.json())
        return taInfo.json(), 200
    return {}, 401


@router.route('/getNotifications', methods=["POST"])
def getNotifications():
    user = User.query.filter(User.id==session.get('userInfo').id).first()
    if(user):
        notifications = user.notifications
        return list(reversed([n.json() for n in notifications]))
    return [], 401

@router.route('/listLTCOfficeOrders', methods=['POST'])
def listLTCOfficeOrder():
    handlerInfo = session.get('userInfo')
    if(handlerInfo.id ==0): 
        list(reversed([j.json() for j in LTCInfo.query.filter(LTCInfo.userId == handlerInfo.id, LTCInfo.stageCurrent >= 100).all()]))
    return list(reversed([j.json() for j in LTCInfo.query.filter(LTCInfo.stageCurrent >= 100).all()]))



@router.route('/listTAOfficeOrders', methods=['POST'])
def listTAOfficeOrder():
    handlerInfo = session.get('userInfo')
    if(handlerInfo.id ==0): 
        list(reversed([j.json() for j in TAInfo.query.filter(TAInfo.userId == handlerInfo.id, TAInfo.stageCurrent >= 100).all()]))
    return list(reversed([j.json() for j in TAInfo.query.filter(TAInfo.stageCurrent >= 100).all()]))