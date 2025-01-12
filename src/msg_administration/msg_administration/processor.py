import datetime
import numpy as np
from std_msgs.msg import Float64
from .sessional import SessionalTable
from .historical import HistoricalTable
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Pose


class DataProcessor:
    
    def __init__(self, db = "ChairRecordings", user = "UNIJES", password = "REDACTED"):
        self._db = db
        self._user = user
        self._password = password
        self._data_buffer = []
        self._recording = {}
        self._sessional_table = SessionalTable(self._db, self._user, self._password)
        self._historical_table = HistoricalTable(self._db, self._user, self._password)
        
        self._sessional_table.connect()
        
    def _lidar_processor(self, msg:LaserScan, topic:str):
        self._recording[topic.replace("/", "") + "data"] = [msg.angle_min, msg.angle_max, msg.angle_increment, msg.time_increment, msg.scan_time, msg.range_min, msg.range_max, msg.ranges, msg.intensities]
        
    def _odom_processor(self, msg:Odometry, topic:str):
        self._recording[topic.replace("/", "") + "data"] = [msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z, msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w, msg.twist.twist.linear.x, msg.twist.twist.linear.y, msg.twist.twist.linear.z, msg.twist.twist.angular.x, msg.twist.twist.angular.y, msg.twist.twist.angular.z]
        
    def _twist_processor(self, msg:Twist, topic:str):
        topic = topic.replace("/", "").split("_")[0]
        
        dirs = ["x", "y", "z"]
        
        linear_data = list(map(lambda attr: getattr(msg.linear, attr),dirs)) 
        angular_data = list(map(lambda attr: getattr(msg.angular, attr), dirs))
        
        for i, data in enumerate(linear_data):
            self._recording["linear_" + topic + dirs[i]] = data
            
        for i, data in enumerate(angular_data):
            self._recording["angular_" + topic + dirs[i]] = data
            
    def _pose_processor(self, msg:Pose, topic:str):
        topic = topic.replace("/", "").split("_")[0]
        
        dirs = ["x", "y", "z"]
        
        position_data = list(map(lambda attr: getattr(msg.position, attr),dirs)) 
        
        for i, data in enumerate(position_data):
            self._recording[topic + "_"+ dirs[i]] = data

    def _float_processor(self, msg:Float64, topic:str):
        self._recording[topic.replace("/", "")] = msg.data
        
    def _manage_empty(self, topic:str):
        """ Centinel values for unregistered topics."""
        if topic == "/scan":
            self._recording["scan"] = [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, [], []]
            
        elif topic == "/odom":
            self._recording["odom"] = [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]
            
        elif topic.split("_")[-1] == "vel":
            msg = Twist()
            msg.linear.x = -1.0
            msg.linear.y = -1.0
            msg.linear.z = -1.0
            msg.angular.x = -1.0
            msg.angular.y = -1.0
            msg.angular.z = -1.0
            self._twist_processor(msg, topic)
            
        elif topic.split("_")[-1] == "pose":
            msg = Pose()
            msg.position.x = -1.0
            msg.position.y = -1.0
            msg.position.z = -1.0
            self._pose_processor(msg, topic)
            
        else:
            self._recording[topic.replace("/", "")] = -1.0
    
    def _check_empty(self, present_topics:list, complete_topics:list):
        for topic in complete_topics:
            if topic not in present_topics:
                self._manage_empty(topic)
                
    def process_reading(self, readings:dict[dict], complete_topics:list):
        present_topics = list(readings.keys())
        self._check_empty(present_topics, complete_topics)
        
        timestamps = []
        
        for topic, timestamp_msg in readings.items():
            timestamp, msg = timestamp_msg.items()
            
            if topic == "/scan":
                self._lidar_processor(msg, topic)
                
            elif topic == "/odom":
                self._odom_processor(msg, topic)
                
            elif topic.split("_")[-1] == "vel":
                self._twist_processor(msg, topic)
                
            elif topic.split("_")[-1] == "pose":
                self._pose_processor(msg, topic)
                
            else:
                self._float_processor(msg, topic)
                
            timestamps.append(timestamp)
            
        timestamps = np.array()
        mean_timestamp = np.mean(timestamps)
        mean_timestamp_sql = datetime.datetime.fromtimestamp(mean_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        self._recording["timestamp"] = mean_timestamp_sql
                
        self._data_buffer.append(self._recording)
        self._recording = {}
        
        if len(self._data_buffer) == 100:
            self._sessional_table.insert_data(self._data_buffer)
            self._data_buffer = []
            
    def keep_data(self):
        if len(self._data_buffer) != 0:
            self._sessional_db.insert_data(self._data_buffer)
            
        self._historical_table.connect()
        iterations = np.ceil(np.ndarray(self._sessional_table.check_length() / 200))
        
        for _ in range(iterations):
            self._historical_table.insert_data(self._sessional_table.extract_data())
            
        self._sessional_table.close_connection()
        self._historical_table.close_connection()
        