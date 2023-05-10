from models import User, Role, LTCInfo, PersonInvolvedLTC, Comment, db, TAInfo
from tests.user1 import user1,users
from tests.ltcinfo1 import ltcInfos
from tests.testRole import role1
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import json
from datetime import datetime
from helper import remindStakeholder
# from functions import listLiveApplications

from app import app

# db.init_app(app)
# commit(addUser(user1))

def main():
    with app.app_context():
        a = [j for j in LTCInfo.query.filter(LTCInfo.stageCurrent != 0 and LTCInfo.stageCurrent < 100).all()]
        f = filter(lambda j: (datetime.now() - j.lastForwardDate).days > 3, a)
        forms = [{'firstName': x.user.firstName, 'lastName': x.user.lastName, 'delay': (datetime.now() - x.lastForwardDate).days, 'stageCurrent': x.stageCurrent, 'id': x.id} for x in f]

        for form in forms:
            role = Role.query.filter(Role.stageCurrent == form['stageCurrent']).first()
            emails = [user.emailId for user in User.query.filter(User.roleId == role.id)]
            for email in emails:
                form['email'] = email
                print(form)
                remindStakeholder(form)

with app.app_context():
    main()
