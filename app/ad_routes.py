from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.auth_forms import LoginForm
from app.ad_forms import AddAdForm
from flask_login import login_required
import sqlalchemy as sa
from app.models.client_models import Client
from app.models.ad_models import Ad
import dateutil.parser as parser

@app.route('/ads/add_ad/<client_id>', methods=['GET', 'POST'])
@login_required
def add_ad(client_id):
    kwargs = {'text':request.args.get('ad_text'), 'community':request.args.get('community')}
    s_date = request.args.get('s_date')
    if s_date is not None:
        kwargs['start_month'] = parser.parse(s_date).month
        kwargs['start_year'] = parser.parse(s_date).year
    e_date = request.args.get('e_date')
    if s_date is not None:
        kwargs['end_month'] = parser.parse(e_date).month
        kwargs['end_year'] = parser.parse(e_date).year
    form = AddAdForm(**kwargs)
    cl = db.first_or_404(sa.select(Client).where(Client.id == client_id))
    if form.validate_on_submit():
        ad = Ad()
        ad.client = cl
        ad.community = form.community.data
        ad.text = form.text.data
        ad.set_start_date(form.start_month.data, form.start_year.data)
        ad.set_end_date(form.end_month.data, form.end_year.data)
        db.session.add(ad)
        db.session.commit()
        flash(f'Note was added.')
        return redirect(url_for('edit_client', id=cl.id))
    return render_template('ads/add_ad.html', title='Add New Ad',
                           form=form)

@app.route('/ads/delete_ad/<id>')
def delete_ad(id):
    ad = Ad.query.get(id)
    db.session.delete(ad)
    db.session.commit()
    return redirect(url_for('edit_client', id=ad.client_id))