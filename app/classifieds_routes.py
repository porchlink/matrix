from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.auth_forms import LoginForm
from app.client_forms import AddClientForm, EditClientForm, AddClientNoteForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models.user_models import User
from app.models.community_models import *
from urllib.parse import urlsplit
from app.freshbooks.classifieds import *

@app.route('/')
@app.route('/classifieds')
@login_required
def classifieds():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Community).order_by(Community.name.desc())
    comms = db.paginate(query, page=page,
                        per_page=10, error_out=False)
    return render_template('classifieds/classifieds.html', title='Classifieds', communities=comms)

@app.route('/')
@app.route('/classifieds/<community>')
@login_required
def comm_classifieds(community='pradera'):
    page = request.args.get('page', 1, type=int)
    inv_ = get_classifieds(community)
    return render_template('classifieds/comm_classifieds.html', title='Community Classifieds', community=community, inv=inv_)

