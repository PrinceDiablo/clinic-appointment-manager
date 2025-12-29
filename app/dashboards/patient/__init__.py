from flask import Blueprint

bp = Blueprint(
    'patient',
    __name__,
    template_folder="templates",
    url_prefix='/patient'

)

from . import routes