from . import app_views
from app.controller.auth import login, logout
from flask import request


@app_views.route('/login', methods=['POST'])
def login_route():
    return login(request)

@app_views.route('/logout', methods=['POST'])
def logout_route():
    return logout()