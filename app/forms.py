'''
forms.py

Copyright Matthew Wollenweber 2014


'''

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, StringField, SubmitField, IntegerField
from wtforms.validators import Required


class LoginForm(Form):
    openid = TextField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)



