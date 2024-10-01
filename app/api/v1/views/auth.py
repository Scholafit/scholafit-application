from . import app_views
from app.controller.auth import login, logout, forgot_password, reset_password
from flask import request


@app_views.route('/login', methods=['POST'])
def login_route():
    return login(request)

@app_views.route('/logout', methods=['POST'])
def logout_route():
    return logout()

@app_views.route('/forgot-password', methods=['POST'])
def forgot_password_route():
    return forgot_password(request)

@app_views.route('/reset-password/<token>', methods=['POST'])
def reset_password_route(token):
    return reset_password(request, token)