from . import app_views
from app.controller.payment import create_payment, verify_payment, get_payment, create_payment_premium, verify_payment_premium
from flask import request

@app_views.route('/payments/top-up', methods=['POST'])
def top_up_account():
    return create_payment(request)

@app_views.route('/payments/verify/<reference>', methods=['GET'])
def verify_payment_status(reference):
    return verify_payment(reference)

@app_views.route('/payments/<reference>', methods=['GET'])
def get_payment_by_ref(reference):
    return get_payment(reference)

@app_views.route('/payments/premium', methods=['POST'])
def sub_premium():
    return create_payment_premium(request)

@app_views.route('payments/verify-premium/<reference>', methods=['GET'])
def verify_premium(reference):
    return verify_payment_premium(reference)