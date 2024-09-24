from abc import ABC, abstractmethod

class MessagingServiceProvider(ABC):

    @abstractmethod
    def send(self, recepient: str, message: str, subject: str = None):
        raise NotImplementedError
    

class MailChimpEmailMessagingService(MessagingServiceProvider):
    pass

class TwilioSmsMessagingService(MessagingServiceProvider):
    pass