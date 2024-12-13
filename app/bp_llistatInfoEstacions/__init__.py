from flask import Blueprint

llistatEstacions = Blueprint( 'llistatEstacions', __name__, template_folder='templates', static_folder='static')

from . import routes
