from flask import Blueprint

info_estacio = Blueprint( 'info_estacio', __name__, template_folder='templates', static_folder='static')

from . import routes
