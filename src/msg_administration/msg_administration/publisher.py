import time
import rclpy
import random
import threading
from rclpy.node import Node
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Pose




class MultiPublisher(Node):
    
    def __init__(self):
        super().__init__("multi_publisher_node")

        # Create publishers for each topic
        self.lidar_pub = self.create_publisher(LaserScan, "/scan", 10)
        self.odom_pub = self.create_publisher(Odometry, "/odom", 10)
        self.feedback_vel_pub = self.create_publisher(Twist, "/feedback_vel", 10)
        self.control_cmd_vel_pub = self.create_publisher(Twist, "/control_cmd_vel", 10)
        self.target_pose_pub = self.create_publisher(Pose, "/target_pose", 10)
        self.current_pose_pub = self.create_publisher(Pose, "/current_pose", 10)
        self.alpha_pub = self.create_publisher(Float64, "/alpha", 10)
        self.r_pub = self.create_publisher(Float64, "/r", 10)

        self.get_logger().info("MultiPublisher Node has been started.")

    def publish_random_scan(self):
        """Publish a random LaserScan message on /scan."""
        
        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "laser_frame"

        msg.angle_min = -3.14
        msg.angle_max = 3.14
        msg.angle_increment = 0.01
        msg.time_increment = 0.0
        msg.scan_time = 0.1
        msg.range_min = 0.0
        msg.range_max = 10.0

        size = int((msg.angle_max - msg.angle_min) / msg.angle_increment)
        msg.ranges = [random.uniform(0.0, 10.0) for _ in range(size)]
        msg.intensities = [random.uniform(0.0, 10.0) for _ in range(size)]

        self.lidar_pub.publish(msg)
        self.get_logger().info("Published random LaserScan on /scan.")

    def publish_random_odom(self):
        """Publish a random Odometry message on /odom."""
        
        msg = Odometry()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "odom_frame"

        # Random position
        msg.pose.pose.position.x = random.uniform(-10.0, 10.0)
        msg.pose.pose.position.y = random.uniform(-10.0, 10.0)
        msg.pose.pose.position.z = 0.0  # 2D

        # Random orientation
        msg.pose.pose.orientation.x = random.uniform(-1.0, 1.0)
        msg.pose.pose.orientation.y = random.uniform(-1.0, 1.0)
        msg.pose.pose.orientation.z = random.uniform(-1.0, 1.0)
        msg.pose.pose.orientation.w = random.uniform(-1.0, 1.0)

        # Random twist
        msg.twist.twist.linear.x = random.uniform(-5.0, 5.0)
        msg.twist.twist.linear.y = random.uniform(-5.0, 5.0)
        msg.twist.twist.linear.z = random.uniform(-5.0, 5.0)
        msg.twist.twist.angular.x = random.uniform(-5.0, 5.0)
        msg.twist.twist.angular.y = random.uniform(-5.0, 5.0)
        msg.twist.twist.angular.z = random.uniform(-5.0, 5.0)

        self.odom_pub.publish(msg)
        self.get_logger().info("Published random Odometry on /odom.")

    def publish_random_twist(self, publisher_name: str):
        """Publish a random Twist message on either /feedback_vel or /control_cmd_vel."""
        
        msg = Twist()
        msg.linear.x = random.uniform(-5.0, 5.0)
        msg.linear.y = random.uniform(-5.0, 5.0)
        msg.linear.z = random.uniform(-5.0, 5.0)
        
        msg.angular.x = random.uniform(-5.0, 5.0)
        msg.angular.y = random.uniform(-5.0, 5.0)
        msg.angular.z = random.uniform(-5.0, 5.0)

        if publisher_name == "feedback_vel":
            self.feedback_vel_pub.publish(msg)
            self.get_logger().info("Published random Twist on /feedback_vel.")
            
        elif publisher_name == "control_cmd_vel":
            self.control_cmd_vel_pub.publish(msg)
            self.get_logger().info("Published random Twist on /control_cmd_vel.")
            
        else:
            self.get_logger().warn(f"Unknown publisher name {publisher_name} for Twist.")

    def publish_random_pose(self, publisher_name: str):
        """Publish a random Pose message on either /target_pose or /current_pose."""
        
        msg = Pose()
        msg.position.x = random.uniform(-10.0, 10.0)
        msg.position.y = random.uniform(-10.0, 10.0)
        msg.position.z = random.uniform(-10.0, 10.0)

        msg.orientation.x = random.uniform(-1.0, 1.0)
        msg.orientation.y = random.uniform(-1.0, 1.0)
        msg.orientation.z = random.uniform(-1.0, 1.0)
        msg.orientation.w = random.uniform(-1.0, 1.0)

        if publisher_name == "target_pose":
            self.target_pose_pub.publish(msg)
            self.get_logger().info("Published random Pose on /target_pose.")
            
        elif publisher_name == "current_pose":
            self.current_pose_pub.publish(msg)
            self.get_logger().info("Published random Pose on /current_pose.")
            
        else:
            self.get_logger().warn(f"Unknown publisher name {publisher_name} for Pose.")

    def publish_random_float(self, publisher_name: str):
        """Publish a random Float64 message on either /alpha or /r."""
        
        msg = Float64()
        msg.data = random.uniform(-100.0, 100.0)

        if publisher_name == "alpha":
            self.alpha_pub.publish(msg)
            self.get_logger().info("Published random Float64 on /alpha.")
            
        elif publisher_name == "r":
            self.r_pub.publish(msg)
            self.get_logger().info("Published random Float64 on /r.")
            
        else:
            self.get_logger().warn(f"Unknown publisher name {publisher_name} for Float64.")


def main(args=None):
    rclpy.init(args=args)
    node = MultiPublisher()

    spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True) # Start the node in a separate thread for input handling
    spin_thread.start()

    try:
        print("\nType one or more topic keywords (separated by ':') and press Enter.")
        print("Available keywords (topics): scan, odom, feedback_vel, control_cmd_vel, target_pose, current_pose, alpha, r")
        print("Example usage: 'r:current_pose' -> publishes 2 random messages on /r and /current_pose.\n")
        print("Type 'q' to quit.\n")

        while True:
            user_input = input("Enter topics (or 'q' to quit): ").strip()
            if user_input.lower() == 'q':
                print("Exiting...")
                break

            if not user_input:
                continue  # Ignore empty input

            topics = user_input.split(':') # Split topics

            for topic in topics:
                t = topic.replace(" ", "")  # Remove spaces

                for _ in range(1): # Proofs with many messages
                    if t == "scan":
                        node.publish_random_scan()
                        
                    elif t == "odom":
                        node.publish_random_odom()
                        
                    elif t == "feedback_vel":
                        node.publish_random_twist("feedback_vel")
                        
                    elif t == "control_cmd_vel":
                        node.publish_random_twist("control_cmd_vel")
                        
                    elif t == "target_pose":
                        node.publish_random_pose("target_pose")
                        
                    elif t == "current_pose":
                        node.publish_random_pose("current_pose")
                        
                    elif t == "alpha":
                        node.publish_random_float("alpha")
                        
                    elif t == "r":
                        node.publish_random_float("r")
                        
                    else:
                        node.get_logger().warn(f"Unknown topic '{t}'. Skipping.")

    except KeyboardInterrupt:
        node.destroy_node()
        rclpy.shutdown()
        spin_thread.join()
        


if __name__ == "__main__":
    main()
