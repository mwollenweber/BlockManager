
from flask import Blueprint

alexa = Blueprint('alexa', __name__)

from . import views
