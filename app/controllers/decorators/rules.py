from functools import wraps
from app.models.colab import EventColab
from flask_login import current_user

def fiscal_or_above(f):
    @wraps(f)
    def decored_function(*args, **kwargs):
        if EventColab.query.filter_by(id=current_user.id).first():
            