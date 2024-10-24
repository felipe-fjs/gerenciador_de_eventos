from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError
from .decorators.roles import admin_or_above
from ..models.colab import EventColab, ColabArea, ColabRole
from ..models.event import UnciEvent

colab_route = Blueprint('colab', __name__)

"""
    * /nome_evento/colab (get): exibe os colaboradores do evento
    * /nome_evento/colab/novo (get e posto): registra novo colaborador
    * /nome_evento/colab/edit (get e put): edita um colaborador
    * /nome_evento/colab/delete (delete): remove um colaborador

    * /nome_evento/fiscal (get): exibe os fiscais do evento, divididos por área de atuação
    * /nome_evento/fiscal/novo (get e post): registra novo fiscal, que já é um colaborador
    * /nome_evento/fiscal/edit (get e put): edita um fiscal
    * /nome_evento/fiscal/delete (delete): remove um fiscal

    * /nome_evento/sub_evento/colab/area/edit (get e put): edita quais colaboradores da area estarão no subevento
    * /nome_evento/sub_evento/colab/area/delete (delete): remove um colaborador de um subevento 
    
"""


@colab_route.route('/<int:event_id>/colabs')
@login_required
@admin_or_above
def event_colabs(event_id):
    try:
        if not UnciEvent.query.filter_by(id=event_id).first():
            flash(("Nenhum evento ativo com esse id."))
            return redirect(url_for('home'))

        colabs = EventColab.query.filter_by(event_id=event_id).all()
    except SQLAlchemyError as error:
        flash(f"Ocorreu um erro ao recuperar os colaboradores do evento '{event_id}'. {error}")
        return redirect(url_for('event.event_home', event_id=event_id))

    return render_template('colab/event_colabs.html', colabs=colabs, event_id=event_id)

@colab_route.route('/<int:event_id>/novo_colaborador', methods=['GET', 'POST'])
def new_colab(event_id):
    if request.method == 'POST':
        
        pass
    try:
        roles = ColabRole.query.all()
        areas = ColabArea.query.all()
    except SQLAlchemyError:
        flash("Ocorreu um erro ao carregar as informações para o registro de colaborador.")
        return redirect(url_for('home'))
    
    return render_template('colab/new_colab.html', event_id=event_id, areas=areas, roles=roles)
