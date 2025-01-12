from abc import ABC, abstractmethod
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Pose

class DataTable(ABC):
    
    def __init__(self, db: str, user:str, password:str, host:str):
        self._db = db
        self._user = user
        self._password = password
        self._host = host
    
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def _create_table(self):
        pass
    
    @abstractmethod
    def insert_data(self, data):
        pass
    
    @abstractmethod
    def close_connection(self):
        pass