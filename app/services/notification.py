from .messaging_service_provider import MessagingServiceProvider 
from abc import ABC, abstractmethod
from typing import TypeVar


class Notification(ABC):
    def __init__(self, messagingServiceProvider:MessagingServiceProvider)-> None:
        self.messagingServiceProvider = messagingServiceProvider

    @abstractmethod
    def notify(self, recepient: str, message: str, subject=None):
        raise NotImplementedError


class EmailNotification(Notification):
    def __init__(self, messagingServiceProvider:MessagingServiceProvider) -> None:
        super().__init__(messagingServiceProvider)
    

    def notify(self, recepient: str, message: str, subject: str):
        self.messagingServiceProvider.send(recepient, message, subject)


class SMSNotification(Notification):
    def __init__(self, messagingServiceProvider:MessagingServiceProvider) -> None:
        super().__init__(messagingServiceProvider)
    

    def notify(self, recepient: str, message: str):
        self.messagingServiceProvider.send(recepient, message)
