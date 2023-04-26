from models import User, Role, LTCInfo, PersonInvolvedLTC, Comment, db
from tests.user1 import user1,users,hods
from tests.ltcinfo1 import ltcInfos
from tests.testRole import role1
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import json
from app import app

def createDummyDataUser():
    ppl = hods 
    for user in ppl:
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


def createNewRole():
    json = {
        "id": 1,
        "designation": "",
        "payLevel": 8,
        "stageCurrent": 1,
        "nextStage": 2,
        "prevStage": 0 
    }

    db.session.add(newRole(json))
    db.session.commit()



def main():
    db.create_all()
    createNewRole() 
    # print(User.query.filter(User.roleId!=0).first().role)


with app.app_context():
    main()