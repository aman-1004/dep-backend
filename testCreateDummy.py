from models import User, Role, LTCInfo, PersonInvolvedLTC, Comment, db
from tests.user1 import user1,users
from tests.ltcinfo1 import ltcInfos
from tests.testRole import role1
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import json
from app import app

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


def createNewRole():
    json = {
        "id": 0,
        "designation": "Assistant Professor",
        "payLevel": 8,
        "stageCurrent": 0,
        "nextStage": 1,
        "prevStage": None
    }

    return newRole(json)



def main():
    db.create_all()
    db.session.add(createNewRole())
    db.session.commit()

with app.app_context():
    main()