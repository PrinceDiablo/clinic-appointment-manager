from flask import Blueprint

bp = Blueprint('appointments', __name__, template_folder="templates", url_prefix='/appointments')
from . import routes