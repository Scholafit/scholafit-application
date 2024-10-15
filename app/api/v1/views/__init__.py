from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from .profile import *
from .student import *
from .user import *
from .auth import *
from .subscription import *
from .learning_module import *