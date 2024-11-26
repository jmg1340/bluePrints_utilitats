from flask import Blueprint

portes = Blueprint( 'portes', __name__, template_folder='templates', static_folder='static')

from . import routes
