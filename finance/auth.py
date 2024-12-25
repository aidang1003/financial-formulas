import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from finance.db import get_db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        walletaddress = request.form['walletaddress']
        db = get_db()
        error = None

        if not walletaddress:
            error = 'Wallet address is required.'


        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (walletaddress, minimumBalance, maximumBalance, factor) VALUES (?, ?, ?, ?)",
                    (walletaddress, 0, 5000, 2), # hard-coded values for now #TODO
                )
                db.commit()
            except db.IntegrityError:
                error = f"Address {walletaddress} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        walletaddress = request.form['walletaddress']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE walletaddress = ?', (walletaddress,)
        ).fetchone()

        if user is None:
            error = 'Incorrect Wallet Address.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view