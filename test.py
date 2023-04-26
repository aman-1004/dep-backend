from models import User, Role, LTCInfo, PersonInvolvedLTC, Comment, db
from tests.user1 import user1,users
from tests.ltcinfo1 import ltcInfos
from tests.testRole import role1
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import json
from functions import listLiveApplications

from app import app

# db.init_app(app)
# commit(addUser(user1))

def main():
    with app.app_context():
    #     print(User.query.filter(User.firstName=='Aman').first().ltcInfos)
        deleteLtcForms()


def deleteLtcForms():
    for ltc in LTCInfo.query.all():
        print(db.session.delete(ltc))
    db.session.commit()

    print([ltc.json() for ltc in LTCInfo.query.all()])


main()