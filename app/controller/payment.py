from flask import make_response, jsonify, Request
from app.models.payment import payment
from app.models.profile import profileRepo, DB_Profile
from app.models.subscription import subscription
import requests
import os

def create_payment(request: Request):
    data = request.json
    profile_id = data.get('profile_id')
    email = data.get('email')
    amount = data.get('amount')
    payments = payment.create_payment_controller(profile_id=profile_id, email=email, amount=amount)
    return payments
    #return ({"payment": payments}), 201

# Create payment for premium
def create_payment_premium(request: Request):
    data = request.json
    profile_id = data.get('profile_id')
    email = data.get('email')
    amount = data.get('amount')
    payments = payment.create_payment_5000(profile_id=profile_id, email=email, amount=amount)
    return payments

def get_payment(reference):
    user_payment = payment.get_payment_by_reference(reference)
    if user_payment:
        return make_response(jsonify({"profile": user_payment.to_dict(), "msg": "SUCCESS"}), 200)
    
    return make_response(jsonify({"profile": None, "msg": 'profile not found'}), 404)

def verify_payment(reference):
    payments = payment.get_payment_by_reference(reference)
    if not payments:
        return make_response(jsonify({"error": "Payment not found"}), 404)

    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers).json()
    if response.get('data') and response['data']['status'] == 'success':
        profile = profileRepo.get_by_id(DB_Profile, payments.profile_id)
        payment.update_profile_balance(profile, payments.amount)
        payment.update_payment_status(payments, 'SUCCESS')
        return make_response(jsonify(profile.to_dict()), 200)
    if response.get('data') and response['data']['status'] == 'abandoned':
        return make_response(jsonify({"error": response}), 402)

    return make_response(jsonify({"error": "Payment verification failed"}), 400)

# verify for premium subscription
def verify_payment_premium(reference):
    payments = payment.get_payment_by_reference(reference)
    if not payments:
        return make_response(jsonify({"error": "Payment not found"}), 404)

    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers).json()
    if response.get('data') and response['data']['status'] == 'success':
        profile = profileRepo.get_by_id(DB_Profile, payments.profile_id)
        print(profile.to_dict())
        subscription.create_subscription(user_id=profile.user_id, plan='PREMIUM')
        #payment.update_profile_balance(profile, payments.amount)
        payment.update_payment_status(payments, 'SUCCESS')
        user_profile = profileRepo.get_by_id(DB_Profile, payments.profile_id)
        return make_response(jsonify({"data": user_profile.to_dict(), "success": "Verified"}), 200)
    if response.get('data') and response['data']['status'] == 'abandoned':
        return make_response(
            jsonify({
                "status": "Payment not successful",
                "status_code": 402,
                "message": response['data'].get('message', 'No additional details provided'),
                "errors": [{"field": "payment_status", "error": response['data'].get('gateway_response', 'Abandoned')}]
            }),
            402
        )

    return make_response(
            jsonify({
                "status": "Payment verification failed",
                "status_code": 500,
                "message": "Unexpected error during payment verification",
                "errors": [{"field": "response", "error": response}]
            }),
            500
        )