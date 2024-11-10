from flask import Blueprint

perfils = Blueprint( 'perfils', __name__, template_folder='templates', static_folder='static')

from . import routes
