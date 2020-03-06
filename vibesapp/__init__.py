from flask import Flask, g
from sqlalchemy import create_engine, MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message
# flask-sqlacodegen --flask --outfile models.py sqlite:///D:\\graduation\\New\\done\\vibesapp\\vibes.db

# engine = create_engine('sqlite:///D:\\graduation\\folder\\done\\vibesapp\\vibes.db')
# metadata = MetaData()
# metadata.create_all(engine)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'vibes.db')
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
# app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
# app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.debug = True
db = SQLAlchemy(app)
db.app = app
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)

from vibesapp import routes, models
