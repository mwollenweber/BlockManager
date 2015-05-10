'''
app/main/forms.py

Copyright Matthew Wollenweber 2014


'''

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, Field
from wtforms.fields import FileField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo, IPAddress, ip_address, NumberRange
from wtforms.widgets.core import HTMLString, html_params, escape
from wtforms import ValidationError
from re import findall

from ..models import User


class InlineButtonWidget(object):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('type', 'submit')
        # Allow passing title= or alternately use field.description
        title = kwargs.pop('title', field.description or '')
        title = ''
        params = html_params(title=title, **kwargs)

        html = '''
                <div class="btn-group">
                    <div class="dropdown">
                          <button class="btn btn-default dropdown-toggle disabled"
                              type="button" id="investigateAddressButton" data-toggle="dropdown">
                                Investigate <span class="caret"></span>
                          </button>
                          <ul id="investigateDropMenu" class="dropdown-menu" role="menu" >
                            <li id="googleLink"></li>
                          </ul>
                    </div>
                </div>
                    '''
        #return HTMLString(html % (params, escape(field.label.text)))
        return HTMLString(html)


class BootStrapSubmitWidget(object):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('type', 'submit')
        # Allow passing title= or alternately use field.description
        title = kwargs.pop('title', field.description or '')
        title = ''

        field.label = ''
        field.label = False
        field.description = ''

        params = html_params(title=title, **kwargs)

        html = '''<button type="submit" id="blockButton" class="btn btn-danger disabled"
                  title="Enter an Address to Block" data-toggle="tool-tip">  Submit Block</button>'''
        return HTMLString(html)


class InlineButtonField(BooleanField):
    widget = InlineButtonWidget()


class BootStrapSubmitField(BooleanField):
    widget = BootStrapSubmitWidget()


class cidrAddress(object):
    def __init__(self, min=10, max=18, message=None,
                 regex="^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\\/(\\d|[1-2]\\d|3[0-2]))?$"):
        self.min = min
        self.max = max
        self.message = message
        self.regex = regex

    def __call__(self, form, field):
        if len(field.data) < 10 or len(field.data) > 18:
            raise ValidationError(self.message)

        if findall(self.regex, cidr) == None:
            raise ValidationError(self.message)


class IPcidr(object):
    def __init__(self, min=7, max=18, message=None,
                 regex="^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\\/(\\d|[1-2]\\d|3[0-2]))?$"):
        self.min = min
        self.max = max
        self.message = message
        self.regex = regex

    def __call__(self, form, field):
        if len(field.data) < self.min or len(field.data) > self.max:
            raise ValidationError(self.message)

        if findall(self.regex, cidr) == None:
            raise ValidationError(self.message)


class ipSearch(Form):
    # accept IP
    IP = StringField('IP', validators=[Required(), Length(1, 18), IPAddress()])
    submit = SubmitField("Search")


class cidrSearch(Form):
    cidr = StringField('IP', validators=[Required(), Length(10, 18), cidrAddress()])
    submit = SubmitField("Search")


class blockForm(Form):
    address = StringField('Address', validators=[Required(), Length(7, 18), IPAddress()])
    notes = StringField("Notes", validators=[Required(), Length(4, 512)])
    duration = IntegerField("Block Length (Days)", [Required(), NumberRange(1, 90)], default=90)

    investigate = InlineButtonField("", description=None, validators=None)
    submitBlock = BootStrapSubmitField("", description='', validators=None)

class uploadBlockListForm(Form):
    filePath = FileField("Upload")
    duration = IntegerField("Duration")
    notes = StringField("Notes")
    submit = SubmitField("Submit")
