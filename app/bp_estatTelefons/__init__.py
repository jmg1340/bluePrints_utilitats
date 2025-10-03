from flask import Blueprint

estatTelefons = Blueprint( 'estatTelefons', __name__, template_folder='templates', static_folder='static')

from . import routes
