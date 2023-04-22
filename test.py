from models import User, Role, LTCInfo, PersonInvolvedLTC, Comment, db
from tests.user1 import user1,users
from tests.ltcinfo1 import ltcInfos
from tests.testRole import role1
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import json


from app import app

# db.init_app(app)

def createDummyDataUser():
    for user in users:
        db.session.add(newUser(user))

def createDummyLTCInfo():
    for ltcInfo in ltcInfos:
        db.session.add(newLTC(ltcInfo))


def newUser(user):
    a = User(user)
    print(a)
    return a

def newRole(role):
    a = Role(**role)
    print(a)
    return a

# ltc = ltcInfos[0]

def newLTC(ltc):
    a = LTCInfo(ltc)
    print(a)
    return a

def checkEmail(emailId):
    foundUser = User.query.filter(User.emailId == emailId).first()
    return foundUser

# commit(addUser(user1))

def main():
    with app.app_context():
        with open("tests/testLtc.json", 'r') as file:
            ltcInfo = json.load(file)
            info = LTCInfo(ltcInfo)
            print(info)
            # print(ltcInfo)


# ctx = app.app_context
# with ctx():
#     # db.create_all()
#     main()
#     # db.session.commit()


main()
