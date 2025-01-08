from isubscriber import ISubscriber
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Pose
from std_msgs.msg import Float64


class LidarSubscriber(ISubscriber):
    
    def __init__(self, node:Node, topic:str = "/scan") -> None:
        self._node = node
        self._topic = topic
        self._subscriber = None
        
    def subscribe(self) -> None:
        self._subscriber = self.node.create_subscription(LaserScan, self.topic, self.received_message)
        self._node.get_logger().info(f"Subscribed to {self._topic}")
        
    def received_message(self, msg:LaserScan) -> None:
        self._node.get_logger().info(f"""Scan data:
                                    angle_min: {msg.angle_min}
                                    angle_max: {msg.angle_max}
                                    angle_increment: {msg.angle_increment}
                                    time_increment: {msg.time_increment}
                                    scan_time: {msg.scan_time}
                                    range_min: {msg.range_min}
                                    range_max: {msg.range_max}
                                    ranges: {msg.ranges}
                                    intensities: {msg.intensities}""")
        
class OdomSubscriber(ISubscriber):
    
    def __init__(self, node:Node, topic:str = "/odom") -> None:
        self._node = node
        self._topic = topic
        self._subscriber = None
        
    def subscribe(self) -> None:
        self._subscriber = self.node.create_subscription(Odometry, self.topic, self.received_message)
        self._node.get_logger().info(f"Subscribed to {self._topic}")
        
    def received_message(self, msg:Odometry) -> None:
        self._node.get_logger().info(f"""Odometry data:
                                    estimated pose: {msg.pose.pose}
                                    pose covariance: {msg.pose.covariance}
                                    estimated twist: {msg.twist.twist}
                                    twist covariance: {msg.twist.covariance}""")
        
class VelSubscriber(ISubscriber):
    
    def __init__(self, node:Node, topic:str) -> None:
        self._node = node
        self._topic = topic
        self._subscriber = None
        
    def subscribe(self) -> None:
        self._subscriber = self.node.create_subscription(Twist, self.topic, self.received_message)
        self._node.get_logger().info(f"Subscribed to {self._topic}")
        
    def received_message(self, msg:Twist) -> None:
        self._node.get_logger().info(f"""{self.topic} velocity data:
                                    linear: {msg.linear}
                                    angular: {msg.angular}""")
        
class PoseSubscriber(ISubscriber):
    
    def __init__(self, node:Node, topic:str) -> None:
        self._node = node
        self._topic = topic
        self._subscriber = None
        
    def subscribe(self) -> None:
        self._subscriber = self.node.create_subscription(Pose, self.topic, self.received_message)
        self._node.get_logger().info(f"Subscribed to {self._topic}")
        
    def received_message(self, msg:Pose) -> None:
        self._node.get_logger().info(f"""{self.topic} pose data:
                                    position: {msg.position}
                                    orientation: {msg.orientation}""")
        
class FloatSubscriber(ISubscriber):
    
    def __init__(self, node:Node, topic:str) -> None:
        self._node = node
        self._topic = topic
        self._subscriber = None
        
    def subscribe(self) -> None:
        self._subscriber = self.node.create_subscription(Float64, self.topic, self.received_message)
        self._node.get_logger().info(f"Subscribed to {self._topic}")
        
    def received_message(self, msg:Float64) -> None:
        self._node.get_logger().info(f"""{self.topic} 
                                    data: {msg.data}""")
        