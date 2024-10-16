from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from CONFIG import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/gerenciador_de_eventos'


db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

from app.models.user import User, UserType, UserProfile
from app.models.colab import ColabRole, Colab, EventColab
from app.models.event import UnciEvent, SubEvent

from app.controllers.account import account_route
app.register_blueprint(account_route, url_prefix='/account')
