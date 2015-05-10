
from flask import Blueprint

mdl = Blueprint('mdl', __name__)

from . import views
