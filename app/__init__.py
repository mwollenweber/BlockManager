'''
Copyright Matthew Wollenweber 2014
Block Manager

'''

from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.mail import Mail, Message
from flask.ext.admin import Admin, BaseView, expose, form, helpers
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import admin, login


from config import config
import os.path as op

bootstrap = Bootstrap() 
mail = Mail()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

from .admin.views import MyView, MyAdminIndexView, AuthenticatedModelView, AuthenticatedFileAdmin
from models import User, ipBlock, protectedRanges


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    #pagedown.init_app(app)
    
    #admin crap
    admin = Admin(app, 'Auth', index_view=MyAdminIndexView(), base_template='/admin/my_master.html')
    admin.add_view(AuthenticatedModelView(User, db.session))
    admin.add_view(AuthenticatedModelView(ipBlock, db.session))
    admin.add_view(AuthenticatedModelView(protectedRanges, db.session))
    path = op.join(op.dirname(__file__), 'static')
    admin.add_view(AuthenticatedFileAdmin(path, '/static/', name='Static Files'))    
 
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    #disabling alexa for heroku's limited db options
    #from .services.alexa import alexa as alexa_blueprint
    #app.register_blueprint(alexa_blueprint, url_prefix="/alexa")
    
    from .services.mdl import mdl as mdl_blueprint
    app.register_blueprint(mdl_blueprint, url_prefix="/mdl")
    
    from .services.et import et as et_blueprint
    app.register_blueprint(et_blueprint, url_prefix="/et")
    
    from .services.phishtank import phishTank as phishTank_blueprint
    app.register_blueprint(phishTank_blueprint, url_prefix="/phishTank")
    
       
    return app


app = create_app("development")
if __name__ == '__main__':
    app.run()


