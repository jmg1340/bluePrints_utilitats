from flask import Blueprint

marcadors = Blueprint( 'marcadors', __name__, template_folder='templates', static_folder='static')

from . import routes
