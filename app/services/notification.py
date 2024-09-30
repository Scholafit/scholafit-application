from .messaging_service_provider import MessagingServiceProvider, MailChimpEmailMessagingService
from abc import ABC, abstractmethod
import os
from typing import TypeVar


class Notification(ABC):
    """
    Abstract base class for notification services.

    This class defines a common interface for sending notifications using different messaging
    service providers. Subclasses must implement the `notify` method to define how notifications
    are sent.

    Attributes:
        messagingServiceProvider (MessagingServiceProvider): An instance of a messaging service provider
            that handles sending notifications. This must be provided by subclasses.
    """
    def __init__(self, messagingServiceProvider:MessagingServiceProvider)-> None:
        self.messagingServiceProvider = messagingServiceProvider

    @abstractmethod
    def notify(self, recepient: str, message: str, subject=None):
        raise NotImplementedError


class EmailNotification(Notification):
    """
    Implementation of the Notification class responsible for sending email notifications.

    This class uses a specified messaging service provider to send email notifications.

    Attributes:
        messagingServiceProvider (MessagingServiceProvider): An instance of a messaging service
            provider that handles sending emails. This can be any class that implements the
            MessagingServiceProvider interface.
    """
    def __init__(self, messagingServiceProvider:MessagingServiceProvider) -> None:
        """
        Initializes the EmailNotification service with a specified messaging service provider.

        Args:
            messagingServiceProvider (MessagingServiceProvider): A service provider for sending
                messages, implementing the MessagingServiceProvider interface.
        """
        super().__init__(messagingServiceProvider)
    

    def notify(self, recepient: str, message: str, subject: str):
        """
        Sends an email notification to the specified recipient.

        Args:
            recipient (str): The email address of the recipient.
            message (str): The body content of the email.
            subject (str): The subject line of the email.
        """
        self.messagingServiceProvider.send(recepient, message, subject)


def get_email_notification_service(sender_address: str):
    """
    Initializes and returns an email notification service using MailChimp's transactional API.

    Args:
        sender_address (str): The email address that will be used as the sender for outgoing emails.
        example: registration@scholafit.com
    Returns:
        EmailNotification: An instance of the EmailNotification class initialized with 
                           the MailChimp email messaging client.
    
    Environment Variables:
        MAILCHIMP_TRANSACTIONAL_API_KEY: API key for MailChimp's transactional email service, 
                                         retrieved from the environment variables.
    """

    API_KEY = os.getenv('MAILCHIMP_TRANSACTIONAL_API_KEY')
    client = MailChimpEmailMessagingService(API_KEY, sender_address)
    client.init()
    return EmailNotification(client)


class SMSNotification(Notification):
    def __init__(self, messagingServiceProvider:MessagingServiceProvider) -> None:
        super().__init__(messagingServiceProvider)
    

    def notify(self, recepient: str, message: str):
        
        self.messagingServiceProvider.send(recepient, message)

