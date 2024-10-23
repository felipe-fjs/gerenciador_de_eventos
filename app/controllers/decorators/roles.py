from functools import wraps
from app.models.colab import EventColab, Colab
from flask import redirect, url_for, flash
from flask_login import current_user


def there_is_colab(event_id):
    """Returns true if there is a colab in the event"""
    if EventColab.query.filter_by(user_id=current_user.id, event_id=event_id).first():
        return True
    return False

def colab_role(event_id) -> int:
    """Returns the colab role"""
    return EventColab.query.filter_by(user_id=current_user.id, event_id=event_id).first().role


def there_is_coor():
    """Returns true if the current user is a coordinator"""
    if Colab.query.filter_by(user_id=current_user.id).first() and Colab.query.filter_by(user_id=current_user.id).first().is_coor:
        return True
    return False


def colab_or_above(f):
    @wraps(f)
    def decored_function(*args, **kwargs):
        event_id = kwargs.get('event_id')

        if there_is_colab(event_id) and there_is_coor():
            flash ("Você não pode acessar o scanner!")
            return redirect(url_for('home'))

        return f(*args, **kwargs)
    
    return decored_function


def fiscal_or_above(f):
    @wraps(f)
    def decored_function(*args, **kwargs):
        event_id = kwargs.get('event_id')
        if not (there_is_colab(event_id) and colab_role(event_id) >= 2) and not there_is_coor() :
            flash("Você precisa de permissão de fiscal, no mínimo, para acessar esse link!")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    
    return decored_function


def admin_or_above(f):
    @wraps(f)
    def decored_function(*args, **kwargs):
        event_id = kwargs.get('event_id')
        if (there_is_colab(event_id=event_id) and colab_role(event_id=event_id) == 3) and not there_is_coor():
            flash("Você precisa de permissão de administrador, no mínimo, para acessar esse link!")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    
    return decored_function


def coor_required(f):
    @wraps(f)
    def decored_function(*args, **kwargs):
        if not there_is_coor():
            flash("Você precisa de permissão de Coordenador, no mínimo, para acessar esse link!")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    
    return decored_function
