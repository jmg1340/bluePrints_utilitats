from flask import Blueprint

pings = Blueprint( 'pings', __name__, template_folder='templates')

from . import routes