from flask import Blueprint

pings = Blueprint( 'pings', __name__, template_folder='templates', static_folder='static')

from . import routes