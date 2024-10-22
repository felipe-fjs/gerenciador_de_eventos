from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User, UserProfile, UserType
from app import bcrypt, db, login_manager
from flask_login import login_required, logout_user, login_user


account_route = Blueprint('account', __name__)


def send_email_confirmation():
    pass


@login_manager.user_loader
def get_user(id):
    return User.query.filter_by(id=id).first()


@account_route.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST': 
        if User.query.filter_by(email=request.form.get('email')).first():
            flash('Email já cadastrado!')
            return redirect(url_for('account.signup'))
        
        try:
            new_user = User(email=request.form.get('email'), 
                            pwd=bcrypt.generate_password_hash(request.form.get('pwd')).decode('utf-8'))
            db.session.add(new_user)
            db.session.flush()
            print(f"ID DO USUÀRIO: {new_user.id}")
            new_user_profile = UserProfile(user_id=new_user.id, 
                                        first_name=request.form.get('first-name'),
                                        last_name=request.form.get('last-name'),
                                        user_type=1,
                                        curso=request.form.get('curso'),
                                            )
            db.session.add(new_user_profile)
            db.session.commit()
        except SQLAlchemyError as error:
            flash(f'Ocorreu um erro ao criar sua conta! {error}')
            db.session.rollback()
            return redirect(url_for('account.signup'))

        # parte para envio de email, tentar aplicar de forma assincrona ou fila de tarefas (rabbit ou algo do tipo)
        return redirect(url_for('account.login'))

    try:
        user_types = UserType.query.all()
    except SQLAlchemyError:
        user_types= "Não foi possivel recureperar os tipos. Editar no perfil depois!"

    return render_template("account/signup.html", user_types=user_types)


@account_route.route('/login', methods=['GET', 'POST'])
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
        login_user(user)
    
        return redirect(url_for('home')) # colocar redirect para home dos eventos
        
    return render_template('account/login.html')


@account_route.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Você foi deslogado com sucesso!")
    return redirect(url_for('account.login'))


@account_route.route('/solicitar-nova-senha')
def reset_pwd():
    pass


@account_route.route('/nova-senha')
def new_pwd():
    pass


@account_route.route('/qrcode')
@login_required
def qrcode():
    pass