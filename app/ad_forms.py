from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange
from datetime import datetime
from app.models.community_models import Community
from dateutil.relativedelta import relativedelta

next_month = datetime.now()+relativedelta(months=+1)

class AddAdForm(FlaskForm):
    community_query = Community.query.all()#['Stonegate','Stroh Ranch']#
    communities = []
    for c in community_query:
        communities.append(c)
    community = SelectField('Customer', choices=communities, default=1)
    text = TextAreaField('Ad Text')
    start_month = IntegerField('Start Month', validators=[DataRequired(),NumberRange(min=1, max=12)], default=next_month.month)
    start_year = IntegerField('Start Year', validators=[DataRequired()], default=next_month.year)
    end_month = IntegerField('End Month', validators=[DataRequired(),NumberRange(min=1, max=12)], default=next_month.month)
    end_year = IntegerField('End Year', validators=[DataRequired()], default=next_month.year)
    submit = SubmitField('Add +')