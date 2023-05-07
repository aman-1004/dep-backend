import mimetypes
import uuid
import os
from flask import Blueprint, session, request, send_file
import json
import random
from protected_routes import router as protected_router
# from checkEmail import check
from functions import checkEmail
from helper import randomGen, sendOTP

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
                "roleId": userInfo.roleId,
                "designation": userInfo.designation,
                "role": userInfo.role.json(),
                }, 200
    
    return {}, 401



@protected_router.route('/getSignImage', methods=["POST"])
def getSignImage():
    fileName = session.get('userInfo').signUrl
    base_path = os.path.join(os.path.dirname(__file__), 'uploads')
    filePath = f"{base_path}/{fileName}"
    return send_file(filePath) 


@protected_router.route('/logout', methods=['POST'])
def logOut():
    session.pop('userInfo')
    return "", 200


@router.route('/uploadReceipt', methods=["POST"])
def uploadReceipt():
    for file in request.files.getlist('file'):
        fileName = uuid.uuid4().hex + mimetypes.guess_extension(file.mimetype)
        base_path = os.path.join(os.path.dirname(__file__), 'receipts')
        filePath = f"{base_path}/{fileName}"
        print(file.save(filePath))
    return "what"



@router.route("/loginOTP", methods=["POST"])
def loginOTP():
    print(request.form)
    if(request.is_json):
        emailId = json.loads(request.data).get('emailId')
    else:
        emailId = request.form.get('emailId', None)
    print('emailId is', emailId)
    if (emailId):
        otp: int  = randomGen(4)
        sendOTP(emailId, otp)
        session['otp'] = otp
        userInfo = checkEmail(emailId)
        if(userInfo):
            sendOTP(email=emailId, otp=otp)
            return "User Found", 200
        return "User Not Found", 401