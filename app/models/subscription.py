from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import datetime as dt
from .base_model import BaseModel
from .database import Repository, get_db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.profile import DB_Profile, profileRepo


class DB_Subscription(BaseModel):
    __tablename__ = 'subscriptions'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    plan: Mapped[str] = mapped_column(ENUM('free_trial', 'premium', 'enterprise'), nullable=False)
    status: Mapped[str] = mapped_column(ENUM('ACTIVE', 'INACTIVE'), nullable=False, default='ACTIVE')
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user = relationship("DB_User", back_populates="subscription")

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.plan = kwargs.get('plan')
        self.status = kwargs.get('status', 'ACTIVE')
        self.start_date = kwargs.get('start_date')
        self.end_date = kwargs.get('end_date')

class SubscriptionRepository(Repository):
    def __init__(self, database: SQLAlchemy):
        super().__init__(database)

class Subscription:
    def __init__(self, dbRepository: Repository) -> None:
        self.db = dbRepository
        self.profile_repo = profileRepo

    def create_subscription(self, user_id: int, plan: str, start_date: datetime = None, end_date: datetime = None):
        # Set default start and end dates if not provided
        if not start_date:
            start_date = datetime.now(dt.timezone.utc)
        if not end_date:
            if plan == "FREE_TRIAL":
                end_date = start_date + timedelta(days=7)
            elif plan == "PREMIUM":
                end_date = start_date + timedelta(days=30)
            elif plan == "ENTERPRISE":
                end_date = start_date + timedelta(days=30)

        subscription = DB_Subscription(
            user_id=user_id,
            plan=plan,
            status="ACTIVE",
            start_date=start_date,
            end_date=end_date
        )

         #Update subscription status of the user profile
        user_profile = self.profile_repo.database.session.query(DB_Profile).filter_by(user_id=user_id).first()
        if user_profile:
            user_profile.subscription_status = "ACTIVE"
            self.profile_repo.database.session.commit()

        saved_subscription = self.db.save(subscription)

        return saved_subscription.to_dict()

    def get_all(self):
        subscriptions = self.db.get_all(DB_Subscription)
        return [subscription.to_dict() for subscription in subscriptions]

    def get_subscription_by_user_id(self, user_id: int) -> DB_Subscription | None:
        subscription = self.db.database.session.query(DB_Subscription).filter_by(user_id=user_id).first()
        if subscription:
            return subscription.to_dict()
        else:
            return None

    def renew_subscription(self, subscription_id: int, new_end_date: datetime = None):
        subscription = self.db.get_by_id(DB_Subscription, subscription_id)
        if not subscription:
            return {"error": "Subscription not found"}

        # If new_end_date is not provided, extend by 30 days as default
        if not new_end_date:
            new_end_date = subscription.end_date + timedelta(days=30)

        subscription.end_date = new_end_date
        subscription.status = "ACTIVE" 
        self.db.database.session.commit()

        # Update the profile database subscription status to ACTIVE
        user_profile = self.profile_repo.database.session.query(DB_Profile).filter_by(user_id=subscription.user_id).first()
        if user_profile:
            user_profile.subscription_status = "ACTIVE"
            self.profile_repo.database.session.commit()

        return subscription.to_dict()


# Scheduler for checking subscription status
def check_subscription_status():
    """
    A function to check subscription status and update it.
    """
    all_subscriptions = Subscription(get_db()).get_all()  # Get all subscriptions
    for sub in all_subscriptions:
        if sub['status'] == 'ACTIVE' and datetime.now(dt.timezone.utc) > sub['end_date']:
            Subscription(get_db()).update_subscription(sub['id'], status='INACTIVE')

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_subscription_status, trigger="interval", days=1)
scheduler.start()

database = get_db()
subscriptionRepo = SubscriptionRepository(database)
subscription = Subscription(subscriptionRepo)
