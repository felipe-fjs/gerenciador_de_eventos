from flask import Blueprint, render_template, request
from flask_login import login_required
from app.controllers.decorators.roles import coor_required


coor_route = Blueprint('coor', __name__)


@coor_route.route('/coor_home')
@login_required
@coor_required
def coor_home():    
    return render_template("event/admin/coor_home.html")

