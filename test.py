from models import User, Role, LTCInfo, PersonInvolvedLTC, Comment, db, TAInfo
from tests.user1 import user1,users
from tests.ltcinfo1 import ltcInfos
from tests.testRole import role1
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import json
from datetime import datetime
from helper import remindStakeholder
from functions import sendReminders

from app import app

# db.init_app(app)
# commit(addUser(user1))

def main():
    with app.app_context():
        sendReminders()
with app.app_context():
    main()
