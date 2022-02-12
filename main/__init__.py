from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager
basedir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
login_manager=LoginManager(app)
login_manager.init_app(app)
login_manager.login_view="user.login"


app.config["SECRET_KEY"]="mysecretkey"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+os.path.join(basedir,"database.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)
Migrate(app,db)

from main.core.views import core
from main.user.views import user
from main.blog.views import blog
from main.error.views import error

app.register_blueprint(core)
app.register_blueprint(user)
app.register_blueprint(blog)
app.register_blueprint(error)

