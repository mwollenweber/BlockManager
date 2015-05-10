
from flask import Blueprint

phishTank  = Blueprint('phishtank', __name__)

from . import views
