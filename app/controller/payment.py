from flask import make_response, jsonify, request
from app.models.payment import payment
from app.models.profile import profileRepo, DB_Profile
import requests
import os

def create_payment():
    data = request.json
    payments = payment.create_payment(
        profile_id=data['profile_id'],
        reference=data['reference'],
        amount=data['amount']
    )
    return make_response(jsonify({"payment": payments}), 201)


def get_payment(reference):
    user_payment = payment.get_payment_by_reference(reference)
    if user_payment:
        return make_response(jsonify({"profile": user_payment, "msg": "SUCCESS"}), 200)
    
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
        profile = profileRepo.get_by_id(DB_Profile, payment.profile_id)
        payment.update_profile_balance(profile, payment.amount)
        payment.update_payment_status(payment, 'SUCCESS')
        return make_response(jsonify(profile.to_dict()), 200)

    return make_response(jsonify({"error": "Payment verification failed"}), 400)