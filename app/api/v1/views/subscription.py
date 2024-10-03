from . import app_views
from app.controller.subscription import subscribe, get_subscription, renew_subscription, get_all_subcriptions
from flask import request

@app_views.route('/subscribe', methods=['POST'])
def subscribe_route():
    return subscribe(request)

@app_views.route('/subscriptions', methods=['GET'])
def get_all_subscriptions():
    return get_all_subcriptions()

@app_views.route('/subscription/<int:user_id>', methods=['GET'])
def get_subscription_route(user_id):
    return get_subscription(user_id)

@app_views.route('/renew-subscription', methods=['POST'])
def renew_subscription_route():
    return renew_subscription(request)