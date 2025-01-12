import pymysql
from .idatatable import IDataTable

class SessionalTable(IDataTable):
    
    def __init__(self, db: str, user:str, password:str, host = "localhost"):
        self._db = db
        self._user = user
        self._password = password
        self._host = host
        
    def _create_database(self):
        self._cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self._db};")
        
    def connect(self):
        """Connect to the database and delete all the previous loaded tables"""
        
        self._connection = pymysql.connect(host=self._host, user=self._user, password=self._password)
        self._cursor = self._connection.cursor()
        
        self._create_database() 
        
        self._cursor.execute(f"USE {self._db}")
        self._cursor.execute("DROP TABLE IF EXISTS sessional_recordings;")        
        self._connection.commit()
            
        self._create_table()
            
    def _create_table(self):
            self._cursor.execute("""CREATE TABLE sessional_recordings (timestamp DATETIME,
                                                                        current_x FLOAT, current_y FLOAT, current_z FLOAT,
                                                                        target_x FLOAT, target_y FLOAT, target_z FLOAT,
                                                                        linear_feedback_x FLOAT, linear_feedback_y FLOAT, linear_feedback_z FLOAT,
                                                                        angular_feedback_x FLOAT, angular_feedback_y FLOAT, angular_feedback_z FLOAT,
                                                                        linear_control_x FLOAT, linear_control_y FLOAT, linear_control_z FLOAT,
                                                                        angular_control_x FLOAT, angular_control_y FLOAT, angular_control_z FLOAT,
                                                                        alpha FLOAT, r FLOAT,
                                                                        scan_data JSON,
                                                                        odom_data JSON);""")
            
    def insert_data(self, data:list[dict]):
        """
        Inserts a batch of records into the table.
        
        Args
        ----
            - data: each dict is a row and the topic data of an instance
        """
        
        query = """INSERT INTO sessional_readings (timestamp, 
                                                    current_x, current_y, current_z, 
                                                    target_x, target_y, target_z, 
                                                    linear_feedback_x, linear_feedback_y, linear_feedback_z, 
                                                    angular_feedback_x, angular_feedback_y, angular_feedback_z, 
                                                    linear_control_x, linear_control_y, linear_control_z, 
                                                    angular_control_x, angular_control_y, angular_control_z, 
                                                    alpha, r, scan_data, odom_data) 
                                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

        formatted_data = [[record["timestamp"],
                            record["current_x"], record["current_y"], record["current_z"],
                            record["target_x"], record["target_y"], record["target_z"],
                            record["linear_feedback_x"], record["linear_feedback_y"], record["linear_feedback_z"],
                            record["angular_feedback_x"], record["angular_feedback_y"], record["angular_feedback_z"],
                            record["linear_control_x"], record["linear_control_y"], record["linear_control_z"],
                            record["angular_control_x"], record["angular_control_y"], record["angular_control_z"],
                            record["alpha"], record["r"],
                            pymysql.converters.escape_string(str(record["scan_data"])),  # JSON
                            pymysql.converters.escape_string(str(record["odom_data"]))]for record in data]   # JSON
    
        self._cursor.executemany(query, formatted_data)
        self._connection.commit()
        
    def extract_data(self):
        """Extracts data from the sessional table to load it into the historical table."""
        
        query = """SELECT timestamp, 
                        current_x, current_y, current_z, 
                        linear_feedback_x, linear_feedback_y, linear_feedback_z, 
                        linear_control_x, linear_control_y, linear_control_z, 
                        alpha, r 
                    FROM sessional_recordings
                    LIMIT 200;"""
        
        self._cursor.execute(query)
        data = self._cursor.fetchall()
        
        self._delete_data()
        
        return data
    
    def _delete_data(self):
        query = """DELETE FROM sessional_recordings LIMIT 200;"""
        self._cursor.execute(query)
        self._connection.commit()
        
    
    def check_length(self) -> int:
        """Check the length of the sessional table"""
        
        query = """SELECT COUNT(*) FROM sessional_recordings;"""
        self._cursor.execute(query)
        length = self._cursor.fetchone()[0]
        
        return length
    
    def close_connection(self):
        self._cursor.close()
        self._connection.close()
        

        
        
