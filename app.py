from flask import Flask
from flask_session import Session
import sys
import collections
from routes import router
from models import db


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


@app.route("/home")
def home():
    return "You r home"

if (__name__ == "__main__"):
    app.run(debug=True, port=5000)
