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

    def __init__(self, **kwargs):
        self.profile_id = kwargs.get('profile_id')
        self.reference = kwargs.get('reference')
        self.amount = kwargs.get('amount')
        self.status = kwargs.get('status', 'pending')

class PaymentRepository(Repository):
    def __init__(self, database):
        super().__init__(database)

class Payment:
    def __init__(self, dbRepository: Repository) -> None:

        self.db = dbRepository

    def create_payment(self, id, reference, amount):
        payment = DB_Payment(profile_id=id, reference=self.generate_reference(), amount=amount)
        saved_payment = self.db.save(payment)
        return saved_payment.to_dict()

    def generate_reference():
        return str(uuid.uuid4())

    def initialize_payment(self, profile_id, email, amount):
        headers = {
            "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}",
            "Content-Type": "application/json"
        }
        reference = str(uuid.uuid4())
        payment_data = {
            "email": email,
            "amount": int(amount * 100),
            "reference": reference,
            "callback_url": f"https://scholafit.com/verifying-payment.html"
        }

        response = requests.post("https://api.paystack.co/transaction/initialize", json=payment_data, headers=headers)

        if response.status_code == 200:
            print('good response')
            data = response.json()
            print(data)
            return data['data']['authorization_url'], data['data']['reference']
        else:
            print(response.status_code)
            return None, None

    def create_payment_controller(self, profile_id, email, amount):
        # Initialize payment with Paystack
        auth_url, reference = self.initialize_payment(profile_id=profile_id, email=email, amount=amount)

        if auth_url:
            print('success')
            # Save payment details in your database
            payments = DB_Payment(profile_id=profile_id, reference=reference, amount=amount)
            print(reference)
            self.db.save(payments)
            # Redirect user to Paystack payment page
            return make_response(jsonify({"authorization_url": auth_url, "reference": reference}), 200)
        else:
            print('failed')
            return make_response(jsonify({"error": "Failed to initialize payment"}), 500)
    
    def get_payment_by_reference(self, reference):
        print(self.db.database.session.query(DB_Payment).filter_by(reference=reference))
        payment = self.db.database.session.query(DB_Payment).filter_by(reference=reference).first()
        return payment

    def update_payment_status(self, payment, status):
        payment.status = status
        self.db.database.session.commit()

    def update_profile_balance(self, profile, amount):
        profile.account_balance += amount
        self.db.database.session.commit()

    # subscriptions for packages directly
    def initialize_payment_5000(self, profile_id, email, amount=5000):
        headers = {
            "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}",
            "Content-Type": "application/json"
        }
        reference = str(uuid.uuid4())
        payment_data = {
            "email": email,
            "amount": int(5000 * 100),
            "reference": reference,
            "callback_url": f"http://localhost:5000/api/v1/payments/verify-premium/{reference}"
        }

        response = requests.post("https://api.paystack.co/transaction/initialize", json=payment_data, headers=headers)

        if response.status_code == 200:
            print('good response')
            data = response.json()
            return data['data']['authorization_url'], data['data']['reference']
        else:
            print(response.status_code)
            return None, None
        
    def create_payment_5000(self, profile_id, email, amount=5000):
        # Initialize payment with Paystack
        auth_url, reference = payment.initialize_payment_5000(profile_id=profile_id, email=email, amount=amount)

        if auth_url:
            print('success')
            # Save payment details in your database
            payments = DB_Payment(profile_id=profile_id, reference=reference, amount=amount)
            self.db.save(payments)
            # Redirect user to Paystack payment page
            return make_response(jsonify({"authorization_url": auth_url, "reference": reference}), 200)
        else:
            print('failed')
            return make_response(jsonify({"error": "Failed to initialize payment"}), 500)


database = get_db()
paymentRepo = PaymentRepository(database)
payment = Payment(paymentRepo)
