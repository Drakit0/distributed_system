from abc import abstractmethod
from rclpy.node import Node
from .isubscriber import ISubscriber

class SubscriberFactory:
    
    def __init__(self, node:Node):
        self._node = node
    
    @abstractmethod
    def create_subscriber(self) -> ISubscriber:
        pass