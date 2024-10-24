from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.controllers.decorators.roles import coor_required
from ..models.colab import ColabRole, ColabArea


coor_route = Blueprint('coor', __name__)


@coor_route.route('/coor_home')
@login_required
@coor_required
def coor_home():    
    return render_template("coor/coor_home.html")


@coor_route.route('/niveis')
@login_required
@coor_required
def get_roles():
    try:
        roles = ColabRole.query.all()
    except SQLAlchemyError:
        flash('Houve um erro ao recuperar as informações de nível.')
        return redirect(url_for('coor.coor_home'))
    
    return render_template('coor/roles.html', roles=roles)


@coor_route.route('/areas')
@login_required
@coor_required
def get_areas():
    try:
        areas = ColabArea.query.all()
    except SQLAlchemyError:
        flash('Houve um erro ao recuperar as informações de nível.')
        return redirect(url_for('coor.coor_home'))
    
    return render_template('coor/areas.html', areas=areas[::-1])

@coor_route.route('/nova_area', methods=['POST', 'GET'])
@login_required
@coor_required
def new_area():
    if request.method == 'POST':
        area = ColabArea(name=request.form.get('area'))
        try:
            db.session.add(area)
            db.session.commit()
            flash(f'Área "{area.name}" criada com sucesso!')
        except SQLAlchemyError:
            db.session.rollback()
            flash(f'Ocorreu um erro ao registrar a área de atuação de colaborador "{area.name}"')

            return redirect(url_for('coor.new_area'))
        
        return redirect(url_for('coor.get_areas'))
        
    return render_template('colab/new_area.html')

@coor_route.route('/editar_area/<area_id>', methods=['POST', 'GET'])
@login_required
@coor_required
def edit_area(area_id):
    if request.method == 'POST':
        try:
            area = ColabArea.query.filter_by(id=request.form.get('area_id')).first()
            area.name = request.form.get('area')
            
            db.session.commit()

        except SQLAlchemyError:
            db.session.rollback()
            flash("Ocorreu um erro ao salvar as informações atualizadas...")
            return redirect(url_for('coor.get_roles'))
        
        flash("Dados atualizados com sucesso!")
        return redirect(url_for('coor.get_areas'))

    try: 
        area = ColabArea.query.filter_by(id=area_id).first()
    except SQLAlchemyError:
        flash('ocorreu um erro ao acessar os dados dessa area')
        return redirect(url_for('coor.get_roles'))

    return render_template('coor/edit_area.html', area=area)

@coor_route.route('/nova_funcao', methods=['POST', 'GET'])
@login_required
@coor_required
def new_role():
    if request.method == 'POST':
        role = ColabRole(role=request.form.get('role'))
        try:
            db.session.add(role)
            db.session.commit()
            flash(f'Função/nível "{role.role}" criada com sucesso!')
        except SQLAlchemyError:
            db.session.rollback()
            flash(f'Ocorreu um erro ao registrar a função/nível "{role.role}"')
            return redirect(url_for('coor.new_role'))
        
    return render_template('colab/new_role.html')

