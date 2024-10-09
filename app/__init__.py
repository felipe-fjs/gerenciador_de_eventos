from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from CONFIG import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/gerenciador_de_eventos'


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models.user import User, UserProfile
from app.models.colab import ColabRole, Colab, EventColab
from app.models.event import UnciEvent, SubEvent
