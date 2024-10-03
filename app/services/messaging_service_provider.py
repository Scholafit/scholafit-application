from abc import ABC, abstractmethod
import mailchimp_transactional as MailChimpTransactional
from mailchimp_transactional.api_client import ApiClientError


class MessagingServiceProvider(ABC):

    @abstractmethod
    def send(self, recepient: str, message: str, subject: str = None):
        raise NotImplementedError
    

class MailChimpEmailMessagingService(MessagingServiceProvider):

    def __init__(self, api_key:str, sender_address:str):
        self.api_key = api_key
        self.sender = sender_address
        self._client = None
    
    def init(self):
        try:
            self.client = MailChimpTransactional.Client(self.api_key)
        except ApiClientError as err:
            print(f'An exception occured {err.text}')

    @property
    def client(self):
        return self._client
    
    @client.setter
    def client(self, mailChimp):
        self._client = mailChimp
    
    def send(self, recepient: str, body: str, subject: str):
        
        msg = {
            "from_email": self.sender,
            "subject": subject,
            "text": body,
            "to": [
                {
                    "email": recepient,
                    "type": "to"
                }
            ]
        }
        
        resp = self.client.messages.send({"message":msg})
        print(resp)
        
        

class TwilioSmsMessagingService(MessagingServiceProvider):
    pass