from flask import make_response, jsonify, Request
from app.models.subscription import subscription
from datetime import datetime

def subscribe(request: Request):
    """
    Subscribe a user to a plan.
    Args:
        request (Request): Request containing user subscription data.
    Returns:
        JSON: A success message or error message.
    """
    data = request.json
    user_id = data.get('user_id')
    plan = data.get('plan')

    try:
        subscribe_response = subscription.create_subscription(user_id=user_id, plan=plan)
        if "error" in subscribe_response:
            return make_response(jsonify(subscribe_response), 400)
        return make_response(jsonify(subscribe_response), 201)
    except Exception as e:
        return make_response(jsonify({"error": f"An error occurred: {str(e)}"}), 500)

def get_all_subcriptions():
    return subscription.get_all()

def get_subscription(user_id: int):
    """
    Get the subscription details of a user.
    Args:
        user_id (int): ID of the user.
    Returns:
        JSON: Subscription details or error message.
    """
    try:
        subscription_details = subscription.get_subscription_by_user_id(user_id)
        if not subscription_details:
            return make_response(jsonify({"error": "Subscription not found"}), 404)
        return make_response(jsonify(subscription_details), 200)
    except Exception as e:
        return make_response(jsonify({"error": f"An error occurred: {str(e)}"}), 500)


def renew_subscription(request: Request):
    data = request.json
    subscription_id = data.get('subscription_id')
    new_end_date = data.get('new_end_date')

    try:
        renewed_subscription = subscription.renew_subscription(
            subscription_id=subscription_id,
            new_end_date=datetime.fromisoformat(new_end_date) if new_end_date else None
        )
        if "error" in renewed_subscription:
            return make_response(jsonify(renewed_subscription), 404)
        return make_response(jsonify(renewed_subscription), 200)
    except Exception as e:
        return make_response(jsonify({"error": f"An error occurred: {str(e)}"}), 500)