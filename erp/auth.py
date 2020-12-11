import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from erp import db
from erp.erp_const import K_RET_USER_LOGGED_IN

bp = Blueprint('auth', __name__, url_prefix='/auth')
@bp.route('/register', methods=('GET', 'POST'))
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            sqldb = db.get_db()
            if db.add_user(username, password) < 0:
                error = 'Add user fail'
        if error is None:
            print(url_for('auth.login'))
            db.close_db()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = -1
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            db.get_db()
            user_id = db.user_login(username, password)
            if user_id < 0:
                error = 'Login failed, wrong user name or password'
            db.close_db()
        if error is None:
            print(url_for('auth.login'))
            session.clear()
            session['user_id'] = user_id
            session['user_name'] = username
            return redirect(url_for('index.index'))
        flash(error)
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    print(url_for('index'))
    return redirect(url_for('index'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    if user_id is None or user_name is None:
        print('User id none')
        g.user = None
    else:
        g.user = {'username' : user_name, 'userid' : user_id}

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            print(url_for('auth.login'))
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
