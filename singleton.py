from Factory.Creators.creators import LidarSubscriberCreator, OdomSubscriberCreator, VelSubscriberCreator, PoseSubscriberCreator, FloatSubscriberCreator
from Factory.Node.node import Node
from Factory.Subscribers.subscribers import LidarSubscriber, OdomSubscriber, VelSubscriber, PoseSubscriber, FloatSubscriber

class SubscriberManager:
    
    def __init__(self):
        self._subscribers = {}
        
    def get_subscriber(self, node:Node, topic:str) -> LidarSubscriber: | OdomSubscriber | VelSubscriber | PoseSubscriber | FloatSubscriber:
        if topic not in self._subscribers.keys():
            self._subscribers[topic] = self._create_subscriber(node, topic)
            
        return self._subscribers[topic]
    
    def _create_subscriber(self, node:Node, topic:str) -> LidarSubscriber: | OdomSubscriber | VelSubscriber | PoseSubscriber | FloatSubscriber:
        if subscriber_type == "/scan":
            return LidarSubscriberCreator(node).create_subscriber()
        
        elif subscriber_type == "/odom":
            return OdomSubscriberCreator(node).create_subscriber()
        
        elif subscriber_type == "/feedback_vel":
            return VelSubscriberCreator(node, topic).create_subscriber()
        
        elif subscriber_type == "/control_cmd_vel":
            return VelSubscriberCreator(node, topic).create_subscriber()

        elif subscriber_type == "/target_pose":
            return PoseSubscriberCreator(node, topic).create_subscriber()
        
        elif subscriber_type == "/current_pose":
            return PoseSubscriberCreator(node, topic).create_subscriber()
        
        elif subscriber_type == "/alpha":
            return FloatSubscriberCreator(node, topic).create_subscriber()
        
        elif subscriber_type == "/r":
            return FloatSubscriberCreator(node, topic).create_subscriber()

        else:
            raise ValueError(f"The subscriber type: {subscriber_type} hasn't been integrated yet, camone McFly, it's not that hard...")