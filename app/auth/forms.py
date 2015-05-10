'''
app/auth/forms.py

Copyright Matthew Wollenweber 2014


'''


#from flask.ext import Form
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, db




class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField("Login")
    
    def get_user(self):
        return db.session.query(User).filter_by(email=self.email.data).first()
    

class RegistrationForm(Form):
    fName = StringField('First Name', validators=[Required(), Length(3,32)])
    lName  = StringField('Last Name', validators=[Required(), Length(3,32)])  
    email = StringField('Email', validators=[Required(), Length(4,64), Email()])
    password = PasswordField('Password', validators=[Required(), EqualTo('password2', message="Passwords do not match")])
    password2 = PasswordField("Confirm password", validators=[Required()])
    submit = SubmitField("Register")
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email aready registered")
        
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first(): 
            raise ValidationError("Username already in use")
        
class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[Required()])
    password = PasswordField('New password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Update Password')

class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class ChangeEmailForm(Form):
    email = StringField('New Email', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
