# Spherical Robot for Search and Reconnaisance
The project involved the development of a remotely operated robot equipped with vision sensor for search and reconnaissance applications. A spherical robot comprises of a ball shaped outer shell, which holds the entire mechanism, actuators, and electronics. It has several advantages over wheeled and legged robots. Owing to its spherical shape, it cannot overturn as opposed to wheeled and legged robots. It is maneuverable in any direction and can easily recover from collisions and obstacles. The spherical shape also eases the deployment strategy. It can be thrown, kicked or dropped at the site of operation with no risk of overturning or extruding actuator and electronics damage. This project uses the spherical robot developed in embedded control laboratory of systems and control engineering group, IIT Bombay. The design of this spherical robot is gearless and scalable in size. Hence, this project investigates its applications in various environments. The manually operated spherical robot would provide visual feedback and other application specific information to the operator for reconnaissance and search.

## Code organization
The code is categorized into two categories based on what hardware/system it runs on i.e. [Raspberry-Pi/Robot specific codes](https://github.com/syedadnanakhtar/sphericalRobot/tree/main/RPi%20specific%20Codes) and [PC-specific codes](https://github.com/syedadnanakhtar/sphericalRobot/tree/main/PC%20Specific%20Codes). 

### Robot-specific codes
- `ax12.py` and `dynamixel.py` are libraries to interface with the Dynamixel servo.
- `myServo.py` is the main code that runs on the Robot hardware which is Raspberry-Pi. The IMU (Invensense MPU-9050) is interfaced in the script, and the accelerometer, gyrometer values are logged when the robot is running. Moreover, the commands from the user (mobile phone app) is read by the script, and neccessary commands are issued to the dynamixel for the robot locomotion. 
### PC-specific codes
- `myClient2` is the application developed for android based phone that features arrow keys to navigate the robot. 

## Contact
Should you find any bug in the code, or have any questions, please feel free to reach out to me on `syed.akhtar[at]tum[dot]de`.
