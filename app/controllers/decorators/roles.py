from functools import wraps
from app.models.colab import EventColab, Colab
from flask import redirect, url_for, flash
from flask_login import current_user

def colab_or_above(f):
    @wraps(f)
    def decored_function(*args, **kwargs):
        event_id = kwargs.get('event_id')
        if not (EventColab.query.filter_by(user_id=current_user.id, event_id=event_id).first() and EventColab.query.filter_by(user_id=current_user.id).first().active) or not Colab.query.filter_by(user_id=current_user.id).is_coor:
            flash("Você precisa de permissão de colaborador, no mínimo, para acessar esse link!")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    
    return decored_function


def fiscal_or_above(f):
    @wraps(f)
    def decored_function(*args, **kwargs):
        event_id = kwargs.get('event_id')
        if not EventColab.query.filter_by(user_id=current_user.id, event_id=event_id).first().role >= 2 or not Colab.query.filter_by(user_id=current_user.id).is_coor:
            flash("Você precisa de permissão de fiscal, no mínimo, para acessar esse link!")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    
    return decored_function


def admin_or_above(f):
    @wraps(f)
    def decored_function(*args, **kwargs):
        event_id = kwargs.get('event_id')
        if EventColab.query.filter_by(user_id=current_user.id, event_id=event_id).first().role >= 3 or not Colab.query.filter_by(user_id=current_user.id).is_coor:
            flash("Você precisa de permissão de administrador, no mínimo, para acessar esse link!")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    
    return decored_function


def coor_required(f):
    @wraps(f)
    def decored_function(*args, **kwargs):
        if not Colab.query.filter_by(user_id=current_user.id).is_coor:
            flash("Você precisa de permissão de Coordenador, no mínimo, para acessar esse link!")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    
    return decored_function
