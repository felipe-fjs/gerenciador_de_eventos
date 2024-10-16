from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User, UserProfile
from app import bcrypt, db

account_route = Blueprint('account', __name__)


def send_email_confirmation():
    pass


@account_route.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST': 
        if User.query.filter_by(email=request.form.get('email')).first():
            flash('Email já cadastrado!')
            return redirect(url_for('account.signup'))
        
        new_user = User(email=request.form.get('email'), 
                        pwd=bcrypt.generate_password_hash(request.form.get('pwd')).decode('utf-8'))
        try:
            with db:
                db.session.add(new_user)
                db.session.commit()
        except SQLAlchemyError as error:
            flash(f'Ocorreu um erro ao criar sua conta! {error}')
            db.session.rollback()
            return redirect(url_for('account.signup'))

        # trecho para a criação do profile do usuário
        new_user_profile = UserProfile(user_id=new_user.id, 
                                       first_name=request.form.get('fist-name'),
                                       last_name=request.form.get('last-name'),
                                       unci_student=request.form.get('unci_student'),
                                       matricula=request.form.get('matricula'),
                                       curso=request.form.get('curso'),
                                        )
        try:
            db.session.add(new_user_profile)
            db.session.commit()
        except SQLAlchemyError:
            flash("ERRO AO CRIAR PERFIL DE USUÁRIO")
            return redirect(url_for('account.login'))

        # parte para envio de email, tentar aplicar de forma assincrona ou fila de tarefas (rabbit ou algo do tipo)

    return render_template("account/signup.html")


@account_route.route('/login')
def login():
    if request.method == 'POST':
        if not User.query.filter_by(email=request.form.get('email')).first():
            flash('Email não cadastrado!')
            return redirect(url_for('account.login'))

        user = User.query.filter_by(email=request.form.get('email')).first()
        if not user.verify_pwd(request.form.get('pwd')):
            flash('Senha incorreta!')
            return redirect(url_for('account.login'))
        
        # logar usuário
        return redirect(url_for('home')) # colocar redirect para home dos eventos
        
    return render_template('')


@account_route.route('/solicitar-nova-senha')
def reset_pwd():
    pass


@account_route.route('/nova-senha')
def new_pwd():
    pass

