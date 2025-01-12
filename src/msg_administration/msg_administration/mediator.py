import time
import rclpy
from threading import Lock
from rclpy.node import Node
from .singleton import SubscriberManager

class Mediator(Node):
    
    def __init__(self, subscriber_manager:SubscriberManager, topics:list[str], process_interval: float, necessary_topics = ["/current_pose", "/target_pose"], show_topics = ["/r", "/alpha", "/control_cmd_vel"]) -> None:
        super().__init__('mediator')
        self.topics = topics
        self._necessary_topics = necessary_topics
        self._show_topics = show_topics
        self._lock = Lock()
        self._subscribers_data = {}
        self._subscriber_manager = subscriber_manager
        
        self._timer = self.create_timer(process_interval, self._timer_callback)
        self.get_logger().info("Mediator node with timer callback started.")
        
    def _timer_callback(self) -> None:
        """Timer callback to process the data."""
        
        try:
            self._check_data_subscribers() # Check the information from the subscribers
            self.process_data() # Process the data
            self.show_data() # Show the data
            self._subscribers_data = {} # Releases subrcribers info
            
        except Exception as e:
            self.get_logger().error(f"Error in the timer callback: {e}")        
    
    def _check_data_subscribers(self) -> None:    
        """Check the information from the subscribers"""
        
        with self._lock:
            for topic in self.topics:
                
                subscriber = self._subscriber_manager.get_subscriber(self, topic) # Get the subscriber for the topic
                messages = subscriber.get_messages()
                                
                if messages:
                    
                    message_time = list(messages.keys())[-1]
                    
                    if len(self._subscribers_data.keys()) != 0:
                        
                        avg_time = sum([list(message.keys())[0] for message in self._subscribers_data.values()]) / len(self._subscribers_data.keys())
                        
                        if abs(message_time - avg_time) <= 0.5: # Allow only 0.5 seconds of delay between messages
                            self._subscribers_data[topic] = {message_time: messages[message_time]}
                                  
                    else:
                        self._subscribers_data[topic] = {message_time: messages[message_time]}
                        
                    subscriber.errase_messages() # Erase the messages from the subscriber                    
                    
    def process_data(self) -> None:
        """Call the data processors in case all necessary topics are available."""
           
        with self._lock:         
            if all(topic in self._subscribers_data.keys() for topic in self._necessary_topics): # Check if all necessary topics are available
                self.get_logger().info(f"{self._subscribers_data.keys()}")
                
            else:
                self.get_logger().info("Necessary topics are not available yet.")
            
    def show_data(self) -> None:
        """Show the data from the subscribers.""" 
        
        with self._lock:
            if all(topic in self._subscribers_data.keys() for topic in self._show_topics): # Check if all show topics are available
                self.get_logger().info("IOSEFF")
            

def main(args=None):
    rclpy.init(args=args)
    
    topics = ["/scan", "/odom", "/feedback_vel", "/control_cmd_vel", "/target_pose", "/current_pose", "/alpha", "/r"]
    subscriber_manager = SubscriberManager()
    mediator = Mediator(subscriber_manager, topics, 1.0)
    
    try:
        rclpy.spin(mediator)
        
    except KeyboardInterrupt:
        mediator.get_logger().info("Mediator node interrupted by user.")
    
    mediator.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
            
