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
        id=1
        user = User.query.filter(User.id==id).first()
        roles = Role.query.all()
        print(roles)

main()