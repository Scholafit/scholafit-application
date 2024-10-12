from . import app_views
from app.controller.payment import create_payment, verify_payment, get_payment

@app_views.route('/payments/top-up', methods=['POST'])
def top_up_account():
    return create_payment()

@app_views.route('/payments/verify/<reference>', methods=['GET'])
def verify_payment_status(reference):
    return verify_payment(reference)

@app_views.route('/payments/<reference>', methods=['GET'])
def get_payment_by_ref(reference):
   
    return get_payment(reference)