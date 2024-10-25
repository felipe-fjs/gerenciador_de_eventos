from app import app, db
from flask import Blueprint, flash, redirect, url_for, render_template, request, jsonify
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError
from app.models.event import UnciEvent, SubEvent
from app.controllers.decorators.roles import admin_or_above, coor_required, there_is_coor, there_is_colab, colab_role
from datetime import datetime

event_route = Blueprint('event', __name__)

""" 
OK    * /inicio (get) : carrega os eventos que estão ativos 

OK    * /novo_evento (get e post): criar um novo evento [coor_required ou feito à mão no mysql]
OK    * /nome_evento (get): carrega as informações do evento
OK    * /nome_evento/editar (get e put): edita as informações DO EVENTO EM SI
OK    * /nome_evento/deletar (delete): realiza a exclusão (ou suspensão) de um evento  [talvez deixe para ser feito pelos técnicos]

"""
def is_admin_or_coor(event_id):
    if there_is_coor() or (there_is_colab(event_id) and colab_role() == 3):
        return True

@app.route('/')
@app.route('/inicio')
def home():
    try:
        events = UnciEvent.query.all()
        events_active = []
        for event in events:
            if event.end >= datetime.now():
                events_active.append(event)
        if not events_active:
            flash('Nenhum evento ativo!')

    except SQLAlchemyError:
        flash('Ocorreu um erro ao acessar os eventos...')

    return render_template('event/home.html', events=events_active)


@event_route.route('/novo_evento', methods=['GET', 'POST'])
@login_required
@coor_required
def event_new():
    if request.method == 'POST':
        try:
            if UnciEvent.query.filter_by(slug=request.form.get('slug')).first():
                flash('Slug de evento já registrado!')
                return redirect(url_for('event.event_new'))

            new_event = UnciEvent(title=request.form.get('title'),
                                desc=request.form.get('desc'),
                                slug=request.form.get('slug'),
                                start=request.form.get('start'),
                                end=request.form.get('end'))
            db.session.add(new_event)
            db.session.commit()
        except SQLAlchemyError:
            flash('Ocorreu um erro ao tentar registrar o evento...')
            return redirect(url_for('home'))

        flash(f"Evento {new_event.title} cadastrado com sucesso!")
        return redirect(url_for('event.event_new'))

    return render_template('event/admin/new.html')


@event_route.route('/<event_id>')
def event_home(event_id):
    try:
        if not UnciEvent.query.filter_by(id=event_id).first():
            flash("Nenhum evento foi encontrado com esse ID!")
            return redirect(url_for('home'))
        
        sub_events = SubEvent.query.filter_by(event_id=event_id).all()
    except SQLAlchemyError:
        flash("Ocorreu um erro ao acessar o evento.")
        return redirect(url_for('home'))

    return render_template('event/event_home.html', sub_events=sub_events, event_id=event_id)


@event_route.route('/<event_id>/edit', methods=['GET', 'PUT'])
@login_required
@admin_or_above
def event_edit(event_id):
    if request.method == 'PUT':
        try:
            edit_event = UnciEvent.query.filter_by(id=event_id).first()

            edit_event.title = request.form.get('title')
            edit_event.desc = request.form.get('desc')
            edit_event.slug = request.form.get('slug')
            edit_event.start = request.form.get('start')
            edit_event.end = request.form.get('end')

            db.session.commit()

        except SQLAlchemyError:
            flash(
                'Sinto muito... ocorreu um erro ao atualizar as informações do evento...')
            return redirect(url_for('event.home', event_id=event_id))

        flash("Evento atualizado com sucesso!")
        return redirect(url_for('event.home', event_id=event_id))
    
    # METHOD == GET
    try:
        if not UnciEvent.query.filter_by(id=event_id).first():
            flash("Evento não encontrado! procure o setor tecnico se tiver certeza que digitou um url correto!")
            return redirect(url_for('home'))
        
        event = UnciEvent.query.filter_by(id=event_id).first()
    except SQLAlchemyError:
        flash('Ocorreu um erro ao acessar as informações do evento! Se persistir, consulte o setor de T.I!')
        return redirect(url_for('event.home', event_id=event_id))

    return render_template('event/admin/edit.html', event=event)


@event_route.route('/<event_id>/deletar', methods=['GET', 'DELETE'])
@login_required
@admin_or_above
def event_delete(event_id):
    if request.method == 'DELETE':
        try:
            delete_event = UnciEvent.query.filter_by(id=event_id).first()
            db.session.delete(delete_event)
            db.session.commit()
        except SQLAlchemyError:
            flash(
                "Ocorreu um erro ao tentar deletar um evento... se persistir, procure o setor de T.I!")
            return jsonify(deleted=False)

        return jsonify(deleted=True)

    # aqui será executada uma mensagem para confirmar a exclusão do evento
    try:
        delete_event = UnciEvent.query.filter_by(id=event_id).first()
    except SQLAlchemyError:
        flash("Ocorreu um erro ao tentar acessar as informações do evento para sua exclusão! Caso persista, procucar setor de T.I!")
        return redirect(url_for('event.home', event_id=event_id))

    return render_template('event/admin/delete.html', event=delete_event)
