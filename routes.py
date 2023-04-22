from flask import Blueprint, session, request
import json
import random
from protected_routes import router as protected_router
# from checkEmail import check
from functions import checkEmail


router = Blueprint("router", __name__)
# router.register_blueprint(protected_router, url_prefix='/auth')
router.register_blueprint(protected_router)



@router.route("/info", methods=["GET"])
def info():
    return {'info': '19:54:20'}


@router.route("/login", methods=["POST"])
def login():
    print(request.form)
    if(request.is_json):
        emailId = json.loads(request.data).get('emailId')
    else:
        emailId = request.form.get('emailId', None)
    print('emailId is', emailId)
    if (emailId):
        userInfo = checkEmail(emailId)
        if (userInfo):
            session['userInfo'] = userInfo
        return getUserInfo() 
    else:
        return {}, 401


@protected_router.route('/getUserInfo', methods=["POST", "GET"])
def getUserInfo():
    userInfo = session.get('userInfo')
    if(userInfo):
        return {
                "firstName": userInfo.firstName,
                "lastName": userInfo.lastName,
                "emailId": userInfo.emailId,
                "dateOfJoining": userInfo.dateOfJoining,
                "department": userInfo.department,
                "isApplicant": True if userInfo.roleId == 0 else False,
                }, 200
    
    return {}, 401


