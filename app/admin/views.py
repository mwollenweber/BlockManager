from flask import render_template, flash, redirect, session, url_for, request, g, make_response
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.admin import Admin, BaseView, expose
from flask.ext import admin, login
from flask.ext.admin.contrib import sqla
from flask.ext.admin import helpers, expose
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.admin.contrib.sqla import ModelView
import flask_login
from .. import admin
from ..models import User
from ..models import db
from ..auth.forms import LoginForm


class UserView(ModelView):
    def is_accessible(self):
        return current_user.isAdmin()
    
    # Show only name and email columns in list view
    column_list = ('lName', 'fName', 'email')
    
    # Enable search functionality - it will search for terms in
    # name and email fields
    column_searchable_list = ('lName', 'fName', 'email')
    
    # Add filters for name and email columns
    column_filters = ('lName', 'fName', 'email')
    

class MyView(BaseView):
    def is_accessible(self):
        return current_user.isAdmin()
    
    @expose('/index/')
    def index(self):
        if login.current_user.is_authenticated() and current_user.isAdmin():
            return self.render('index.html')
        else:
            redirect(url_for('.index'))
    
    def scaffold_form(self):
        
            form_class = super(UserView, self).scaffold_form()
            form_class.extra = TextField('Extra')
            return form_class    




# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):
    def is_accessible(self):
        return current_user.isAdmin()
    
    def scaffold_form(self):
            form_class = super(UserView, self).scaffold_form()
            form_class.extra = TextField('Extra')
            return form_class    

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        
        if login.current_user.isAdmin() and login.current_user.is_authenticated():
            return super(MyAdminIndexView, self).index()
        else:
            return redirect(url_for('.login_view'))

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated() and login.current_user.isAdmin():
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        if login.current_user.is_authenticated() and login.current_user.isAdmin():
            form = RegistrationForm(request.form)
            if helpers.validate_form_on_submit(form):
                user = User()
    
                form.populate_obj(user)
                # we hash the users password to avoid saving it as plaintext in the db,
                # remove to use plain text:
                user.password = generate_password_hash(form.password.data)
    
                db.session.add(user)
                db.session.commit()
    
                login.login_user(user)
                return redirect(url_for('.index'))
            link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
            self._template_args['form'] = form
            self._template_args['link'] = link
            return super(MyAdminIndexView, self).index()
        return redirect(url_for('.index'))

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))
    

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.isApprover() 
    
class AuthenticatedFileAdmin(FileAdmin):
    def is_accessible(self):
        return current_user.isAdmin()       
