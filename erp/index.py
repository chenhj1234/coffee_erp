from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from erp.auth import login_required
from erp import db

bp = Blueprint('index', __name__)

@bp.route('/')
@login_required
def index():
    #return redirect(url_for('rawbean.rawbean_handler'))# render_template('index.html')
    return render_template('index.html')