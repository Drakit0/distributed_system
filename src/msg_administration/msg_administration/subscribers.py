import time
import rclpy
from threading import Lock
from rclpy.node import Node
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
from .isubscriber import ISubscriber
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Pose


class LidarSubscriber(ISubscriber):
    
    def __init__(self, node:Node, topic:str = "/scan") -> None:
        super().__init__()
        self._node = node
        self._lock = Lock()  # Read-write safe actions
        self._topic = topic
        self.messages: dict[float, LaserScan] = {}
        self._node.get_logger().info(f"Subscribing to {self._topic}")
        
        self._subscription = self._node.create_subscription(LaserScan, self._topic, self._received_message, 10)
    
    def _received_message(self, msg:LaserScan) -> None:
        # self._node.get_logger().info(f"""Scan data:
        #                             angle_min: {msg.angle_min}
        #                             angle_max: {msg.angle_max}
        #                             angle_increment: {msg.angle_increment}
        #                             time_increment: {msg.time_increment}
        #                             scan_time: {msg.scan_time}
        #                             range_min: {msg.range_min}
        #                             range_max: {msg.range_max}
        #                             ranges: {msg.ranges}
        #                             intensities: {msg.intensities}""")
        
        timestamp = self._node.get_clock().now().to_msg() # Received time
        seconds = timestamp.sec + timestamp.nanosec / 1_000_000_000.0
        
        with self._lock:
            self.messages[seconds] = msg
        
    def get_messages(self) -> dict:
        with self._lock:
            return self.messages
        
    def errase_messages(self) -> None:
        with self._lock:
            self.messages.clear()
        
class OdomSubscriber(ISubscriber):
    
    def __init__(self, node:Node, topic:str = "/odom") -> None:
        super().__init__() 
        self._node = node
        self._lock = Lock()  # Read-write safe actions
        self._topic = topic
        self.messages: dict[float, Odometry] = {}
        self._node.get_logger().info(f"Subscribing to {self._topic}")
        
        self._subscription = self._node.create_subscription(Odometry, self._topic, self._received_message, 10)

    def _received_message(self, msg:Odometry) -> None:
        # self._node.get_logger().info(f"""Odometry data:
        #                             estimated pose: {msg.pose.pose}
        #                             pose covariance: {msg.pose.covariance}
        #                             estimated twist: {msg.twist.twist}
        #                             twist covariance: {msg.twist.covariance}""")
        
        timestamp = self._node.get_clock().now().to_msg() # Received time
        seconds = timestamp.sec + timestamp.nanosec / 1_000_000_000.0
        
        with self._lock:
            self.messages[seconds] = msg
        
    def get_messages(self) -> dict:
        with self._lock:
            return self.messages
        
    def errase_messages(self) -> None:
        with self._lock:
            self.messages.clear()
        
class TwistSubscriber(ISubscriber):
    
    def __init__(self, node:Node, topic:str) -> None:
        super().__init__() 
        self._node = node
        self._lock = Lock()  # Read-write safe actions
        self._topic = topic
        self.messages: dict[float, Twist] = {}
        self._node.get_logger().info(f"Subscribing to {self._topic}")
        self._subscription = self._node.create_subscription(Twist, self._topic, self._received_message, 10)
        
    def _received_message(self, msg:Twist) -> None:
        # self._node.get_logger().info(f"""{self._topic} velocity data:
        #                             linear: {msg.linear}
        #                             angular: {msg.angular}""")
        
        timestamp = self._node.get_clock().now().to_msg() # Received time
        seconds = timestamp.sec + timestamp.nanosec / 1_000_000_000.0
        
        with self._lock:
            self.messages[seconds] = msg
        
    def get_messages(self) -> dict:
        with self._lock:
            return self.messages
        
    def errase_messages(self) -> None:
        with self._lock:
            self.messages.clear()
        
class PoseSubscriber(ISubscriber):
    
    def __init__(self, node:Node, topic:str) -> None:
        super().__init__()
        self._node = node
        self._lock = Lock()  # Read-write safe actions
        self._topic = topic
        self.messages: dict[float, Pose] = {}
        self._node.get_logger().info(f"Subscribing to {self._topic}")
        self._subscription = self._node.create_subscription(Pose, self._topic, self._received_message, 10)
        
    def _received_message(self, msg:Pose) -> None:
        # self._node.get_logger().info(f"""{self._topic} pose data:
        #                             position: {msg.position}
        #                             orientation: {msg.orientation}""")
        
        timestamp = self._node.get_clock().now().to_msg() # Received time
        seconds = timestamp.sec + timestamp.nanosec / 1_000_000_000.0
        
        with self._lock:
            self.messages[seconds] = msg
        
    def get_messages(self) -> dict:
        with self._lock:
            return self.messages
        
    def errase_messages(self) -> None:
        with self._lock:
            self.messages.clear()
        
class FloatSubscriber(ISubscriber):
    
    def __init__(self, node:Node, topic:str) -> None:
        super().__init__()
        self._node = node
        self._lock = Lock() # Read-write safe actions
        self._topic = topic
        self.messages: dict[float, Float64] = {}
        self._node.get_logger().info(f"Subscribing to {self._topic}")
        self._subscription = self._node.create_subscription(Float64, self._topic, self._received_message, 10)

    def _received_message(self, msg:Float64) -> None:
        # self._node.get_logger().info(f"""{self._topic} 
        #                             data: {msg.data}""")
        
        timestamp = self._node.get_clock().now().to_msg() # Received time
        seconds = timestamp.sec + timestamp.nanosec / 1_000_000_000.0

        with self._lock:
            self.messages[seconds] = msg.data
        
    def get_messages(self) -> dict:
        with self._lock:
            return self.messages
        
    def errase_messages(self) -> None:
        with self._lock:
            self.messages.clear()
        