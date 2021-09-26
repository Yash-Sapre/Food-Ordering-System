from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField , BooleanField
from wtforms.validators import DataRequired,Length, EqualTo


class RegistrationForm(FlaskForm):
    Username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    Email = StringField('Email',validators=[DataRequired()])
    Password = PasswordField('Password',validators=[DataRequired()])
    ConfirmPassword = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('Password')])
    Submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    Username = StringField('Username', validators=[DataRequired()])
    Password = PasswordField('Password', validators=[DataRequired()])
    Remember = BooleanField('Remember Field')
    Submit = SubmitField('Sign Up')



