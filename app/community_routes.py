from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.community_forms import AddCommunityForm
from flask_login import login_required
import sqlalchemy as sa
from app.models.community_models import Community
from urllib.parse import urlsplit


@app.route('/')
@app.route('/communities')
@login_required
def communities():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Community).order_by(Community.name.desc())
    comms = db.paginate(query, page=page,
                        per_page=10, error_out=False)
    return render_template('communities/communities.html', title='Home', communities=comms)

@app.route('/communities/add_community', methods=['GET', 'POST'])
@login_required
def add_community():
    form = AddCommunityForm()
    if form.validate_on_submit():
        community = Community()
        community.name = form.name.data
        db.session.add(community)
        db.session.commit()
        flash(f'{form.name.data} was added as a community.')
        return redirect(url_for('communities'))
    return render_template('communities/add_community.html', title='Add Community',
                           form=form)

@app.route('/communities/delete_client/<id>')
def delete_community(id):
    c = Community.query.get(id)
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for('communities'))