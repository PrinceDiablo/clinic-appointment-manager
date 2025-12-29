from flask import Blueprint

bp = Blueprint(
    'doctor',
    __name__,
    template_folder="templates",
    url_prefix='/doctor'
    
)

from . import routes