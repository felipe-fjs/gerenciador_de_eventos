from app import db
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError
from app.controllers.decorators.roles import coor_required
from ..models.colab import ColabRole, ColabArea


coor_route = Blueprint('coor', __name__)

""" 
    - /niveis (get)
    - /novo_nivel (get e post)
    - /editar_nivel/id (get e put)
    - /deletar_nivel/id (delete)

    - /areas (get)
    - /nova_area (get e post)
    - /editar_area/id (get e put)
    - /deletar_area/id (delete)
"""

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

    return render_template('coor/role/roles.html', roles=roles)

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

    return render_template('colab/role/new_role.html')

@coor_route.route('/editar_nivel/<role_id>', methods=['POST', 'GET'])
@login_required
@coor_required
def edit_role(role_id):
    if request.method == 'POST':
        try:
            role = ColabRole.query.filter_by(id=request.form.get('role_id')).first()
            role.name = request.form.get('role')

            db.session.commit()

        except SQLAlchemyError:
            db.session.rollback()
            flash("Ocorreu um erro ao salvar as informações atualizadas...")
            return redirect(url_for('coor.get_roles'))

        flash("Dados atualizados com sucesso!")
        return redirect(url_for('coor.get_roles'))

    try:
        area = ColabArea.query.filter_by(id=role_id).first()
    except SQLAlchemyError:
        flash('ocorreu um erro ao acessar os dados desse nível.')
        return redirect(url_for('coor.get_roles'))

    return render_template('coor/role/edit_role.html', area=area)

@coor_route.route('/deletar_nivel/<role_id>', methods=['POST', 'GET'])
@login_required
@coor_required
def delete_role(role_id):
    if request.method == 'DELETE':
        try:
            role = ColabRole.query.filter_by(id=role_id).first()
            db.session.delete(role)
            db.session.commit()

        except SQLAlchemyError:
            flash(f'ocorreu um erro ao excluir o nível de ID {role_id}')
            return redirect(url_for('coor.get_roles'))
        
        flash('Nível excluido com sucesso!')
        return redirect(url_for('coor.get_roles'))

    try:
        role = ColabRole.query.filter_by(id=role_id).first()
    except SQLAlchemyError:
        flash('ocorreu um erro ao recuperar as informações do nível.')        
        return redirect(url_for('coor.get_roles'))
    
    return render_template('coor/role/delete_role.html', role=role)



@coor_route.route('/areas')
@login_required
@coor_required
def get_areas():
    try:
        areas = ColabArea.query.all()
    except SQLAlchemyError:
        flash('Houve um erro ao recuperar as informações de nível.')
        return redirect(url_for('coor.coor_home'))

    return render_template('coor/area/areas.html', areas=areas[::-1])

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

    return render_template('coor/area/new_area.html')

@coor_route.route('/editar_area/<area_id>', methods=['POST', 'GET'])
@login_required
@coor_required
def edit_area(area_id):
    if request.method == 'POST':
        try:
            area = ColabArea.query.filter_by(
                id=request.form.get('area_id')).first()
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

    return render_template('coor/area/edit_area.html', area=area)

@coor_route.route('/deletar_area/<area_id>', methods=['POST', 'GET'])
@login_required
@coor_required
def delete_area(area_id):
    if request.method == 'DELETE':
        try:
            area = ColabArea.query.filter_by(id=area_id).first()
            db.session.delete(area)
            db.session.commit()

        except SQLAlchemyError:
            flash(f'ocorreu um erro ao excluir área de ID {area_id}')
            return redirect(url_for('coor.get_areas'))
        
        flash('Nível excluido com sucesso!')
        return redirect(url_for('coor.get_areas'))

    try:
        area = ColabArea.query.filter_by(id=area_id).first()
    except SQLAlchemyError:
        flash('ocorreu um erro ao recuperar as informações do nível.')        
        return redirect(url_for('coor.get_areas'))
    
    return render_template('coor/area/delete_area.html', area=area)
