from flask import Blueprint

main = Blueprint('main', __name__)
from app.models import Permission

from app.main import views, errors

@main.app_context_processor
def inject_permission():
	return dict(Permission=Permission)