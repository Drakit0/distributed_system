# distributed_system

A ROS 2 (Python) package that listens to the topics of an autonomous wheelchair and is meant to store them in MySQL. It was written for the wheelchair that Universidad Pontificia Comillas prepares for the UNIJES competition between Jesuit universities. It is a university project by one author, written between November 2024 and January 2025. The code is unfinished in places, see "State" below.

The report that explains the design is in Spanish: `documentación.pdf` (source `documentación.docx`). The class diagrams are `initial_uml.drawio` (first plan) and `final_uml.drawio` (as implemented).

## Design

The package is `src/msg_administration/msg_administration`. It uses four patterns:

- Factory: `factory.py` defines `SubscriberFactory`, and `creators.py` has one creator per message type (`LidarSubscriberCreator`, `OdomSubscriberCreator`, `TwistSubscriberCreator`, `PoseSubscriberCreator`, `FloatSubscriberCreator`). The products are in `subscribers.py` and follow the `ISubscriber` interface. Each subscriber stores the last messages together with the time at which they arrived, because several of the topics have no header.
- Singleton: `singleton.py` has `SubscriberManager`, which creates the subscriber of a topic the first time it is requested and returns the same one afterwards.
- Mediator: `mediator.py` has the `Mediator` node. A timer reads the subscribers, keeps only messages that arrived within 0.5 seconds of each other, and passes the group on for processing and display.
- Decorator: `decorators.py` has `VisualizationDecorator`, which wraps `Mediator.show_data` to plot the `/r` and `/alpha` pair as a point. The report says this part did not reach a working state.

Data handling is in `processor.py` (`DataProcessor`, which turns each message type into a row and buffers 100 rows) and in `datatable.py`, `sessional.py` and `historical.py`. `SessionalTable` holds everything received during a run and is dropped and recreated at each start. `HistoricalTable` keeps a reduced set of columns (positions, feedback and control linear velocity, alpha, r) with a session number.

Topics handled: `/scan` (LaserScan), `/odom` (Odometry), `/feedback_vel` and `/control_cmd_vel` (Twist), `/target_pose` and `/current_pose` (Pose), `/alpha` and `/r` (Float64).

`publisher.py` is a test node. It reads topic names from the keyboard (for example `r:current_pose`) and publishes random messages on them, so the system can be tried without the wheelchair.

## Running

Requirements: a ROS 2 installation with `rclpy` and the standard message packages, plus `pymysql`, `numpy` and `matplotlib`. The storage classes need a MySQL server.

The database password is read from the environment and is not stored in the code:

```
export CHAIR_DB_PASSWORD=...
export CHAIR_DB_USER=UNIJES          # optional, this is the default
export CHAIR_DB_NAME=ChairRecordings # optional, this is the default
```

Build and run from a ROS 2 workspace:

```
cd <workspace>
cp -r <this repo>/src/msg_administration src/
colcon build --packages-select msg_administration
source install/setup.bash
ros2 run msg_administration publisher
ros2 run msg_administration subscriber
```

## State

In `mediator.py` the creation of `DataProcessor` and the wrapping of `show_data` with the decorator are commented out. As committed, the subscriber node logs the grouped messages and shows `r` and `alpha`, but it does not write to the database. The processor and table classes are written but were not checked against a live server in this repository.

## Author

Pablo Tuñón Laguna.

## Licence

MIT, see `LICENSE`.
