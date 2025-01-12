from abc import ABC, abstractmethod

class ISubscriber(ABC):
    
    @abstractmethod
    def _received_message(self, msg) -> None:
        pass
    
    @abstractmethod
    def get_messages(self) -> dict:
        pass
    
    @abstractmethod
    def errase_messages(self) -> None:
        pass