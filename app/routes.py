from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.auth_forms import LoginForm
from app.client_forms import AddClientForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models.user_models import User
from app.models.client_models import Client
from urllib.parse import urlsplit

@app.route('/')
@app.route('/index')
#@login_required
def index():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Client).order_by(Client.created_ts.desc())
    clients = db.paginate(query, page=page,
                        per_page=10, error_out=False)
    return render_template('index.html', title='Home', clients=clients)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

