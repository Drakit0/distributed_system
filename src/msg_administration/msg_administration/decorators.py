import time
import numpy as np
import matplotlib.pyplot as plt
from .decorator import BaseDecorator


class VisualizationDecorator(BaseDecorator):
    
    def __init__(self, mediator, show_data_func):
        self._mediator = mediator
        self._show_data_func = show_data_func

    def __call__(self):
        """
        Plot
        """
        
        with self._mediator._lock:
            
            decorated_topics = ["/r", "/alpha"]
            
            if all(topic in self._mediator._subscribers_data.keys() for topic in decorated_topics):
                
                plt.ion()  # Interactive
                self.fig, self.ax = plt.subplots()
                self.ax.set_xlim(-10, 10)
                self.ax.set_ylim(-10, 10)
                self.ax.set_xlabel('X')
                self.ax.set_ylabel('Y')
                self.ax.set_title('R alpha polar visualization')
                self.ax.grid(True)
                self.point, = self.ax.plot(0, 0, 'ro')  # Origin point
            
                r = self._mediator._subscribers_data["/r"]
                alpha = self._mediator._subscribers_data["/alpha"]
                
                r = list(r.values())[0]
                alpha = list(alpha.values())[0]

                x = r * np.cos(np.radians(alpha)) # Cartesian
                y = r * np.sin(np.radians(alpha))

                self.point, = self.ax.plot(x, y, 'ro')  # New point
                self._mediator.get_logger().info(f"Plotting point: x={x:.2f}, y={y:.2f}")

                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
                
                plt.show()
                time.time(1)
                plt.close()

                    

        self._show_data_func() # Original function