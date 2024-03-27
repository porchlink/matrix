from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.auth_forms import LoginForm
from app.client_forms import AddClientForm, EditClientForm, AddClientNoteForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models.user_models import User
from app.models.client_models import Client, ClientNotes
from app.models.ad_models import Ad
from urllib.parse import urlsplit
from app.freshbooks.classifieds import *

@app.route('/')
@app.route('/clients')
@login_required
def clients():
    page = request.args.get('page', 1, type=int)
    inv_ = get_classifieds()#['invoices']
    query = sa.select(Client).order_by(Client.created_ts.desc())
    clients = db.paginate(query, page=page,
                        per_page=10, error_out=False)
    return render_template('clients.html', title='Home', clients=clients, inv=inv_)

@app.route('/add_client', methods=['GET', 'POST'])
@login_required
def add_client():
    form = AddClientForm()
    if form.validate_on_submit():
        client = Client()
        client.name = form.name.data
        client.email = form.email.data
        client.password_hash = ""
        db.session.add(client)
        db.session.commit()
        flash(f'{form.name.data} was added as a client.')
        return redirect(url_for('clients'))
    return render_template('add_client.html', title='Add Client',
                           form=form)

@app.route('/clients/<id>', methods=['GET', 'POST'])
@login_required
def edit_client(id):
    form = EditClientForm()
    cl = db.first_or_404(sa.select(Client).where(Client.id == id))
    page = request.args.get('page', 1, type=int)
    query = cl.notes.select().order_by(ClientNotes.timestamp.desc())
    clientnotes = db.paginate(query, page=page,
                        per_page=10,
                        error_out=False)
    ad_query = cl.ads.select().order_by(Ad.timestamp.desc())
    clientads = db.paginate(ad_query, page=page,
                        per_page=10,
                        error_out=False)
    if form.validate_on_submit():
        cl.name = form.name.data
        cl.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('clients'))
    elif request.method == 'GET':
        form.name.data = cl.name
        form.email.data = cl.email
    return render_template('edit_client.html', title='Edit Client',
                           form=form, clientnotes=clientnotes.items, clientads=clientads.items, client_id=cl.id)

@app.route('/clients/add_note/<id>', methods=['GET', 'POST'])
@login_required
def add_client_note(id):
    form = AddClientNoteForm()
    cl = db.first_or_404(sa.select(Client).where(Client.id == id))
    if form.validate_on_submit():
        note = ClientNotes()
        note.body = form.body.data
        note.client = cl
        db.session.add(note)
        db.session.commit()
        flash(f'Note was added.')
        return redirect(url_for('edit_client', id=cl.id))
    return render_template('add_client_note.html', title='Add Note',
                           form=form)

@app.route('/clients/delete_note/<id>')
def delete_note(id):
    note = ClientNotes.query.get(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('edit_client', id=note.client_id))

@app.route('/clients/delete_client/<id>')
def delete_client(id):
    c = Client.query.get(id)
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for('clients'))

# @app.route('/clients/delete_note/<id>')
# def note_delete(id):
#     note = ClientNotes.query.get(id)
#     #out = ClientNotes.query.filter_by(id=id).delete()
#     if note:
#         msg_text = 'Note successfully removed'
#         db.session.commit()
#         flash(msg_text)
#     note = db.first_or_404(sa.select(ClientNotes).where(ClientNotes.id == id))
#     print(note.cl)
#     return redirect(url_for('edit_client', id=note.client_id))