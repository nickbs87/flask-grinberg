from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length



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



class EditProfileForm(FlaskForm):
    name = StringField('Real Name', validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')