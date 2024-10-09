from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.exc import OperationalError
from app.models.user import User, UserProfile
from app import bcrypt, db

account_route = Blueprint('account', __name__)


@account_route.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST': 
        if User.query.filter_by(email=request.form.get('email')).first():
            flash('Email já cadastrado!')
            return redirect(url_for('account.signup'))
        
        new_user = User(email=request.form.get('email'), 
                        pwd=bcrypt.generate_password_hash(request.form.get('pwd')))
        try:
            with db:
                db.session.add(new_user)
                db.session.commit()
        except OperationalError as error:
            flash(f'Ocorreu um erro ao criar sua conta! {error}')
            return redirect(url_for('account.signup'))

        # trecho para a criação do profile do usuário
        
        new_user_profile = UserProfile(user_id=new_user.id, first_name=request.form.get('fist-name'))
        
        


    return render_template("account/signup.html")


@account_route.route('/login')
def login():
    pass


@account_route.route('/solicitar-nova-senha')
def reset_pwd():
    pass


@account_route.route('/nova-senha')
def new_pwd():
    pass

