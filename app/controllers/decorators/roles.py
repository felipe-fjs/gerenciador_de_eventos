from functools import wraps
from app.models.colab import EventColab
from flask import redirect, url_for, flash
from flask_login import current_user

def colab_or_above(f):
    @wraps(f)
    def decored_function(*args, **kwargs):
        if not EventColab.query.filter_by(id=current_user.id).first():
            flash("Você precisa de permissão de colaborador, no mínimo, para acessar esse link!")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    
    return decored_function


def fiscal_or_above(f):
    @wraps(f)
    def decored_function(*args, **kwargs):
        if not EventColab.query.filter_by(id=current_user.id).first().role >= 2:
            flash("Você precisa de permissão de fiscal, no mínimo, para acessar esse link!")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    
    return decored_function


def admin_or_above(f):
    @wraps(f)
    def decored_function(*args, **kwargs):
        if EventColab.query.filter_by(id=current_user.id).first().role >= 3:
            flash("Você precisa de permissão de administrador, no mínimo, para acessar esse link!")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    
    return decored_function
