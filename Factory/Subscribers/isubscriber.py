from abc import ABC, abstractmethod

class ISubscriber(ABC):
    
    @abstractmethod
    def subscribe(self) -> None:
        pass
    
    @abstractmethod
    def received_mesaage(self, msg) -> None:
        pass