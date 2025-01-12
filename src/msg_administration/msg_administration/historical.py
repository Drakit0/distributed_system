import pymysql
from .datatable import DataTable

class HistoricalTable(DataTable):
    
    def __init__(self, db: str, user:str, password:str, host = "localhost"):
        self._db = db
        self._user = user
        self._password = password
        self._host = host
        self._session = 1
        
    def connect(self):
        self._connection = pymysql.connect(host=self._host, user=self._user, password=self._password)
        self._cursor = self._connection.cursor()
        self._cursor.execute(f"USE {self._db}")
        
        self._cursor.execute("SHOW TABLES;")
        tables = self._cursor.fetchall()
        
        if not tables:
            self._create_table()
            
        else:
            self._cursor.execute("""SELECT session 
                                    FROM historical_recordings 
                                    ORDER BY timestamp DESC 
                                    LIMIT 1;""")
            
            self._session = self._cursor.fetchone()[0] + 1
            
    def _create_table(self):
            self._cursor.execute("""CREATE TABLE historical_recordings (timestamp DATETIME, session INT,
                                                            current_x FLOAT, current_y FLOAT, current_z FLOAT,
                                                            linear_feedback_x FLOAT, linear_feedback_y FLOAT, linear_feedback_z FLOAT,
                                                            linear_control_x FLOAT, linear_control_y FLOAT, linear_control_z FLOAT,
                                                            alpha FLOAT, r FLOAT);""")
            
    def insert_data(self, data: list[dict]):
        """
        Inserts a batch of records into the table.
        
        Args
        ----
            - data: each dict is a row and the topic data of an instance
        """
        
        query = """INSERT INTO historical_recordings (timestamp, session, 
                                                        current_x, current_y, current_z, 
                                                        linear_feedback_x, linear_feedback_y, linear_feedback_z, 
                                                        linear_control_x, linear_control_y, linear_control_z, 
                                                        alpha, r) 
                                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    
        formatted_data = [[record["timestamp"], self._session,
                            record["current_x"], record["current_y"], record["current_z"],
                            record["target_x"], record["target_y"], record["target_z"],
                            record["linear_feedback_x"], record["linear_feedback_y"], record["linear_feedback_z"],
                            record["linear_control_x"], record["linear_control_y"], record["linear_control_z"],
                            record["alpha"], record["r"]] for record in data]
    
        self._cursor.executemany(query, formatted_data)
        self._connection.commit()
        
    def close_connection(self):
        self._cursor.close()
        self._connection.close()
        

        