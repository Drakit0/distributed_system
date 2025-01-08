from Factory.Creators.factory import SubscriberFactory
from Factory.Node.node import Node
from Factory.Subscribers.subscribers import LidarSubscriber, OdomSubscriber, VelSubscriber, PoseSubscriber, FloatSubscriber

class LidarSubscriberCreator(SubscriberFactory):
    
    def __init__(self, node:Node) -> None:
        self._node = node
        self.create_subscriber()
    
    def create_subscriber(self) -> LidarSubscriber:
        return LidarSubscriber(self._node)
    
class OdomSubscriberCreator(SubscriberFactory):
    
    def __init__(self, node:Node) -> None:
        self._node = node
        self.create_subscriber()
    
    def create_subscriber(self) -> OdomSubscriber:
        return OdomSubscriber(self._node)
    
class VelSubscriberCreator(SubscriberFactory):
    
    def __init__(self, node:Node, topic:str) -> None:
        self._node = node
        self._topic = topic
        self.create_subscriber()
    
    def create_subscriber(self) -> VelSubscriber:
        return VelSubscriber(self._node, self._topic)
    
class PoseSubscriberCreator(SubscriberFactory):
    
    def __init__(self, node:Node, topic:str) -> None:
        self._node = node
        self._topic = topic
        self.create_subscriber()
    
    def create_subscriber(self) -> PoseSubscriber:
        return PoseSubscriber(self._node, self._topic)
    
class FloatSubscriberCreator(SubscriberFactory):
    
    def __init__(self, node:Node, topic:str) -> None:
        self._node = node
        self._topic = topic
        self.create_subscriber()
    
    def create_subscriber(self) -> FloatSubscriber:
        return FloatSubscriber(self._node, self._topic)
    