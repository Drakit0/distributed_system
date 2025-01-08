from abc import ABC, abstractmethod
from Factory.Subscribers.ISubscriber import ISubscriber

class SubscriberFactory(ABC):
    
    @abstractmethod
    def create_subscriber(self) -> ISubscriber:
        pass