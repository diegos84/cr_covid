# Create __init__ file to tell Python that this application and it's file directory is a package. Run.py will run this package's app variable

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from application.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'primary'

mail = Mail(app)

# Routes must be imported at the end of the file to prevent circular import errors (routes imports app from this file)
from application import routes