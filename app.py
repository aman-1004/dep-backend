from flask import Flask
from flask_session import Session
import sys
import collections
from routes import router
from models import db, User, Role
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Widget

if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    from collections.abc import MutableSet
    collections.MutableSet = collections.abc.MutableSet
else:
    from collections import MutableSet

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)
app.register_blueprint(router)
admin = Admin(app)

@app.route("/home")
def home():
    return "You r home"


class UserView(ModelView):
    column_list = ('id', 'firstName', 'lastName', 'emailId', 'hometown', 'designation', 'payLevel', 'roleId', 'role', 'dateOfJoining', 'department', 'ltcInfos')
    form_columns = ('id', 'firstName', 'lastName', 'emailId', 'hometown', 'designation', 'payLevel', 'role', 'dateOfJoining', 'department', 'ltcInfos')


class RoleView(ModelView):
    column_list = ('id', 'roleName', 'stageCurrent', 'nextStage', 'prevStage')
    form_columns = ('id', 'roleName', 'stageCurrent', 'nextStage', 'prevStage')

admin.add_view(UserView(User, db.session))
admin.add_view(RoleView(Role, db.session))


if (__name__ == "__main__"):
    app.run(debug=True, port=5000)
