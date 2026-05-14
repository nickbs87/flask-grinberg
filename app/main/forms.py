from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email



class NameForm(FlaskForm):
    name = StringField(
        "What's your name",
        validators=[DataRequired()]
        )
    email = EmailField(
        "What's your email", 
        validators=[DataRequired(), Email()]
        )
    submit = SubmitField("Submit")
