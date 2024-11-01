from flask import Blueprint, flash, redirect, url_for, render_template, request, jsonify
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError
from app import db, app
from app.models.event import SubEvent, UnciEvent
from app.models.user import UserProfile
from app.controllers.decorators.roles import admin_or_above, colab_or_above
import jwt


sub_event_route = Blueprint('sub_event', __name__)


""" 
    * /nome_evento/novo_sub_evento (get e post): cria um novo sub_evento (admin_or_above)
    * /nome_evento/sub_evento (get): carrega as informações de um sub_evento
    * /nome_evento/sub_evento/editar (get e put): edita as informações de um sub evento (admin_or_above)
    * /nome_evento/sub_evento/delete (delete): deletar um sub_evento (talvez só suspender)

    * /nome_evento/sub_evento/scanner (get e post): carrega a camera para escanear o qrcode

""" 
@sub_event_route.route('/<event_id>/<subevent_id>')
def sub_event_home(event_id, subevent_id):
    try:
        if not UnciEvent.query.filter_by(id=event_id).first():
            flash("Nenhum evento com esse ID foi encontrado!")
            return redirect(url_for('home'))

        if not SubEvent.query.filter_by(id=subevent_id).first():
            flash('Sub Evento não encontrado!')
            return redirect(url_for('event.home'))
    
        sub_event = SubEvent.query.filter_by(id=subevent_id).first()

    except SQLAlchemyError:
        flash("ocorreu um erro ao acessar o sub evento...")

    return render_template('sub_event/info.html', sub_event=sub_event, event_id=event_id)


@sub_event_route.route('/<event_id>/novo', methods=['GET','POST'])
@login_required
@admin_or_above
def sub_event_new(event_id):
    if request.method == 'POST':
        try:
            sub_event = SubEvent(event_id=event_id,
                                 title=request.form.get('title'),
                                 desc=request.form.get('desc'),
                                 slug=request.form.get('slug'),
                                 start=request.form.get('start'),
                                 end=request.form.get('end'),
                                 classroom=request.form.get('classroom'))
            
            if SubEvent.query.filter_by(slug=sub_event.slug).first():
                flash('Essa slug já está registrada!')
                # Essa template só será utilizada quando um erro ocorreu ou uma slug já existir (talvez criar uma api no futuro pra verificar isso já no formulário)
                return render_template('sub_event/admin/erro_new.html', sub_event=sub_event)
            
            db.session.add(sub_event)
            db.session.commit()
            
        except SQLAlchemyError:
            flash(f'Ocorreu um erro ao tentar criar um novo sub_evento')
            return render_template('sub_event/admin/erro_new.html', sub_event=sub_event)

    return render_template("sub_event/admin/new.html")


@sub_event_route.route('/<event_id>/<subevent_id>/editar', methods=['GET', 'PUT'])
@login_required
@admin_or_above
def sub_event_edit(event_id, subevent_id):
    if request.method == 'PUT':
        try:
            sub_event = SubEvent.query.filter_by(id=subevent_id).first()
            
            if SubEvent.query.filter_by(slug=request.form.get('slug')).first():
                if not sub_event.slug != request.form.get('slug'):
                    flash('Essa slug já está registrada!')
                    # Essa template só será utilizada quando um erro ocorreu ou uma slug já existir (talvez criar uma api no futuro pra verificar isso já no formulário)
                    return render_template('sub_event/admin/erro_edit.html', sub_event=sub_event)
            
            sub_event.title = request.fom.get('title')
            sub_event.desc = request.fom.get('desc')
            sub_event.slug = request.fom.get('slug')
            sub_event.start = request.fom.get('start')
            sub_event.end = request.fom.get('end')
            sub_event.classroom = request.fom.get('classroom')

            db.session.commit()
            
        except SQLAlchemyError:
            flash(f'Ocorreu um erro ao tentar atualizar as informações do sub_evento')
            return render_template('sub_event/admin/erro_new.html', sub_event=sub_event)
        
        flash("Atualizações salvas com sucesso!")
        return redirect(url_for("sub_event.sub_event_home", event_id=event_id, subevent_id=subevent_id))

    try:
        if not SubEvent.query.filter_by(id=subevent_id, event_id=event_id).first():
            flash("Sub evento não encontrado!")
            return redirect(url_for('event.event_home', event_id=event_id))
        
        sub_event = SubEvent.query.filter_by(id=subevent_id, event_id=event_id).first()

    except SQLAlchemyError:
        flash("Ocorreu um erro ao acessar as informações do sub evento!")
        return redirect(url_for('event.event_home', event_id=event_id))

    return render_template("sub_event/admin/new.html", sub_event=sub_event)


@sub_event_route.route('/<event_id>/<subevent_id>/delete', methods=['GET', 'DELETE'])
@login_required
@admin_or_above
def sub_event_delete(event_id, subevent_id):
    if request.method == 'DELETE':
        try:
            sub_event = SubEvent.query.filter_by(id=subevent_id, event_id=event_id).first()
            if not sub_event:
                flash("Sub evento não encontrado!")
                return redirect(url_for("event.event_home", event_id=event_id))

            db.session.delete(sub_event)
            db.session.commit()
            
        except SQLAlchemyError:
            flash(f'Ocorreu um erro ao tentar excluir um sub_evento!')
            return redirect(url_for('event.event_home', event_id=event_id))
        
        flash("Sub evento excluido com sucesso!")
        return redirect(url_for("sub_event.event_home", event_id=event_id))

    try:
        sub_event = SubEvent.query.filter_by(id=subevent_id, event_id=event_id).first()

        if not SubEvent.query.filter_by(id=subevent_id, event_id=event_id).first():
            flash("Sub evento não encontrado!")
            return redirect(url_for('event.event_home', event_id=event_id))

    except SQLAlchemyError:
        flash("Ocorreu um erro ao acessar as informações do sub evento!")
        return redirect(url_for('event.event_home', event_id=event_id))

    return render_template('sub_event/admin/delete.html', sub_event=sub_event)


# @sub_event_route.route('/<event_id>/subevent_id>/scanner', methods=['GET','POST'])
@sub_event_route.route('/scanner', methods=['GET','POST'], defaults={'jwt_info': None})
@sub_event_route.route('/scanner/<jwt_info>', methods=['GET','POST'])
@login_required
@colab_or_above
def scanner(jwt_info):
    if request.method == 'POST':
        pass
    
    if jwt_info:
        decode = jwt.decode(jwt=jwt_info, key=app.config.get('SECRET_KEY'), algorithms='HS256')
        try:
            user_profile = UserProfile.query.filter_by(user_id=decode['id']).first()
        except SQLAlchemyError:
            return jsonify(error='Ocorreu um erro ao recuperar informações do usuário')
        if not user_profile:
            return jsonify(error='Nenhum usuário localizado com ese Qr Code!')
        
        return jsonify(success=True,
            user_id=user_profile.user_id,
            name=user_profile.get_fullname(),
            email=user_profile.get_email(),
        )
    return render_template('sub_event/scanner.html')
