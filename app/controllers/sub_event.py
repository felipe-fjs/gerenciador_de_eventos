from flask import Blueprint, flash, redirect, url_for, render_template, request
from sqlalchemy.exc import SQLAlchemyError
from app.models.event import SubEvent, UnciEvent


sub_event_route = Blueprint('sub_event', __name__)


""" 
    * /nome_evento/novo_sub_evento (get e post): cria um novo sub_evento (admin_or_above)
    * /nome_evento/sub_evento (get): carrega as informações de um sub_evento
    * /nome_evento/sub_evento/editar (get e put): edita as informações de um sub evento (admin_or_above)
    * /nome_evento/sub_evento/delete (delete): deletar um sub_evento (talvez só suspender)

    * /nome_evento/sub_evento/scanner (get e post): carrega a camera para escanear o qrcode

""" 
@sub_event_route.route('/<event_id>/novo_sub_evento', methods=['GET', 'POST'])
# @admin_or_above
def new(event_id):
    pass


@sub_event_route.route('/<event_id>/<subevent_id>')
def home(event_id, subevent_id):
    try:
        if not UnciEvent.query.filter_by(id=event_id).first():
            flash("Nenhum evento com esse id foi encontrado!")
            return redirect(url_for('home'))

        if not SubEvent.query.filter_by(id=subevent_id).first():
            flash('Sub Evento não encontrado!')
            return redirect(url_for('event.home'))
    
        sub_event = SubEvent.query.filter_by(id=subevent_id).first()

    except SQLAlchemyError:
        flash("ocorreu um erro ao acessar o sub evento...")

    return render_template('sub_event/info.html')


@sub_event_route.route('/<event_id>/<subevent_id>/editar')
def edit(subevent_id):
    pass


@sub_event_route.route('/<event_id>/<subevent_id>/delete')
def delete(subevent_id):
    pass

