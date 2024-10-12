from .base_model import BaseModel
from .database import Repository, get_db
from sqlalchemy import String, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
import os, requests
import uuid
from flask import make_response, jsonify, request

class DB_Payment(BaseModel):
    __tablename__ = 'payments'

    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey('profiles.id'), nullable=False)
    reference: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default='PENDING')
    currency: Mapped[str] = mapped_column(String(10), default='NGN')

    profile = relationship("DB_Profile", back_populates="payments")

    def __init__(self, profile_id, reference, amount, status='pending'):
        self.profile_id = profile_id
        self.reference = reference
        self.amount = amount
        self.status = status

class PaymentRepository(Repository):
    def __init__(self, database):
        super().__init__(database)

class Payment:
    def __init__(self, dbRepository: Repository) -> None:

        self.db = dbRepository

    def create_payment(self, profile_id, reference, amount):
        payment = DB_Payment(profile_id=profile_id, reference=reference, amount=amount)
        saved_payment = self.db.save(payment)
        return saved_payment.to_dict()

    def generate_reference():
        return str(uuid.uuid4())

    def initialize_payment(profile_id, email, amount):
        headers = {
            "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}",
            "Content-Type": "application/json"
        }

        payment_data = {
            "email": email,
            "amount": int(amount * 100),  # Paystack expects the amount in kobo
            "reference": payment.generate_reference(),
            "callback_url": "https://127.0.0.1:5000/api/v1/payment/verify"  # Replace with your callback
        }

        response = requests.post("https://api.paystack.co/transaction/initialize", json=payment_data, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data['data']['authorization_url'], data['data']['reference']
        else:
            return None, None

    def create_payment_controller(profile_id, email, amount):
        # Initialize payment with Paystack
        auth_url, reference = payment.initialize_payment(profile_id, email, amount)

        if auth_url:
            # Save payment details in your database
            payment.create_payment(profile_id, reference, amount)

            # Redirect user to Paystack payment page
            return make_response(jsonify({"authorization_url": auth_url}), 200)
        else:
            return make_response(jsonify({"error": "Failed to initialize payment"}), 500)
    
    def get_payment_by_reference(self, reference):
        payment = self.db.database.session.query(DB_Payment).filter_by(reference=reference).first()
        return payment.to_dict()

    def update_payment_status(self, payment, status):
        payment.status = status
        self.db.database.session.commit()

    def update_profile_balance(self, profile, amount):
        profile.account_balance += amount
        self.db.database.session.commit()


database = get_db()
paymentRepo = PaymentRepository(database)
payment = Payment(paymentRepo)