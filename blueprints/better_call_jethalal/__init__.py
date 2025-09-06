from flask import Blueprint

bp = Blueprint('jethalal', __name__, url_prefix='/jethalal')

# Import routes after blueprint creation to avoid circular imports
from . import routes
