from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, Regexp, Email, ValidationError
from application.models import Users


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), 
                        Length(min=5, max=20, message="Username must have between 5 and 20 characters"), 
                        Regexp('^\w+$', message="Username must contain only letters, numbers or underscore")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), 
                            Length(min=5, message="Password must have at least 5 characters")])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), 
                                    EqualTo('password', message="Password must match the confirmation")])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists. Please choose a different one')


class UpdateAccountForm(FlaskForm):
    username = StringField('User', validators=[DataRequired(), 
                        Length(min=5, max=20, message="Username must have between 5 and 20 characters"), 
                        Regexp('^\w+$', message="Username must contain only letters, numbers or underscore")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists. Please choose a different one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')

class RequestResetForm(FlaskForm):
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. Please register')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), 
                            Length(min=5, message="Password must have at least 5 characters")])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), 
                                    EqualTo('password', message="Password must match the confirmation")])
    submit = SubmitField('Reset')
