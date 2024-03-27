from flask import Flask, current_app
from app.models import *
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.freshbooks.client_tests import *

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
app.app_context().push()

from app import routes, client_routes, community_routes, ad_routes, classifieds_routes
from app.models import client_models, user_models, community_models, ad_models