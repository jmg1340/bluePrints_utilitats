from flask import Blueprint

swPM = Blueprint( 'swPM', __name__, template_folder='templates')

from . import routes