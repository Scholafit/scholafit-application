from . import app_views
from app.controller.auth import login, logout, forgot_password, reset_password, verify_new_user
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

@app_views.route('/verify/<token>', methods=['POST'])
def verify_user_route(token):
    return verify_new_user(request, token)