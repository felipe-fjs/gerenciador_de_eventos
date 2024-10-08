from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from CONFIG import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/gerenciador_de_eventos'

@app.route('/')
def home():
    return "<h1>Ola</h1>"


db = SQLAlchemy(app)
migrate = Migrate(app, db)

