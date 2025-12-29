from flask import Blueprint

bp = Blueprint(
    'clinic_receptionist',
    __name__,
    template_folder="templates",
    url_prefix='/receptionist'

)

from . import routes