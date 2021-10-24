from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class SignUpForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[
        DataRequired(),
        Email(message="Please, enter a valid email"),
        Length(min=6)
        ])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=6, message="Please, select a stronger password")
        ])
    confirm_password = PasswordField("Confirm Your Password", validators=[
        DataRequired(),
        EqualTo("password", message="Passwords must match")
        ])

    submit = SubmitField('Register')