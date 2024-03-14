from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class AddCommunityForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add +')

# class EditClientForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired()])
#     email = StringField('email', validators=[DataRequired(), Email()])
#     submit = SubmitField('Update')

# class AddClientNoteForm(FlaskForm):
#     body = TextAreaField('Note', validators=[DataRequired()])
#     submit = SubmitField('Add +')
