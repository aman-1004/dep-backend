from flask import request, session, Blueprint, Response
router = Blueprint("protected-router", __name__) 
from endpoints import router as endpoints_router


@router.before_request
def before():
    if (session.get('userInfo', None) is None):
        return "You are not authorized", 401 
    # print(session)


@router.route('/')
def inf():
    return "You are logged in"


@router.route('/logout')
def logout():
    session.clear()
    return "Logout successful", 200


router.register_blueprint(endpoints_router)
