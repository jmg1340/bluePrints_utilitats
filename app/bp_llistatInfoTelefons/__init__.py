from flask import Blueprint

llistatTelefons = Blueprint( 'llistatTelefons', __name__, template_folder='templates', static_folder='static')

from . import routes
