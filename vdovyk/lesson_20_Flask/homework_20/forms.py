from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
)


class SignUpForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[
        DataRequired(),
        Email(message='Please, enter a valid email'),
        Length(min=6)
        ])
    password = PasswordField(label='Password', validators=[
        DataRequired(),
        Length(min=6, message='Please, select a stronger password')
    ])
    confirm_password = PasswordField(label='Confirm Your Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])

    submit = SubmitField('Register')




