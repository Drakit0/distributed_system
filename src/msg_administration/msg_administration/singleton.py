from rclpy.node import Node
from .subscribers import LidarSubscriber, OdomSubscriber, TwistSubscriber, PoseSubscriber, FloatSubscriber
from .creators import LidarSubscriberCreator, OdomSubscriberCreator, TwistSubscriberCreator, PoseSubscriberCreator, FloatSubscriberCreator

class SubscriberManager:
    
    def __init__(self):
        self._subscribers = {}
        
    def get_subscriber(self, node:Node, topic:str) -> LidarSubscriber | OdomSubscriber | TwistSubscriber | PoseSubscriber | FloatSubscriber:
        """
        Get the subscriber for the topic if it exists, otherwise create it.
        
        Args
        ----
            - node: The node that will be used to create the subscriber.
            - topic: The topic that the subscriber will be listening to.
            
        Returns
        -------
            - The subscriber for the topic."""
        
        if topic not in self._subscribers.keys():
            self._subscribers[topic] = self._create_subscriber(node, topic)
            
        return self._subscribers[topic]
    
    def _create_subscriber(self, node:Node, topic:str) -> LidarSubscriber | OdomSubscriber | TwistSubscriber | PoseSubscriber | FloatSubscriber | None:
        if topic == "/scan":
            creator = LidarSubscriberCreator(node)
            return creator.create_subscriber()
        
        elif topic == "/odom":
            creator = OdomSubscriberCreator(node)
            return creator.create_subscriber()
        
        elif topic == "/feedback_vel":
            creator = TwistSubscriberCreator(node, topic)
            return creator.create_subscriber()
        
        elif topic == "/control_cmd_vel":
            creator = TwistSubscriberCreator(node, topic)
            return creator.create_subscriber()

        elif topic == "/target_pose":
            creator = PoseSubscriberCreator(node, topic)
            return creator.create_subscriber()
        
        elif topic == "/current_pose":
            creator = PoseSubscriberCreator(node, topic)
            return creator.create_subscriber()
        
        elif topic == "/alpha":
            creator = FloatSubscriberCreator(node, topic)
            return creator.create_subscriber()
        
        elif topic == "/r":
            creator = FloatSubscriberCreator(node, topic)
            return creator.create_subscriber()

        else:
            raise ValueError(f"The subscriber type: {topic} hasn't been integrated yet, camone McFly, it's not that hard...")
        
