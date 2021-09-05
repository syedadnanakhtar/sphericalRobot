# Spherical Robot for Search and Reconnaisance

![Spherical Robot](/spherical-robot.jpg)

The project involved the development of a remotely operated robot equipped with vision sensor for search and reconnaissance applications. A spherical robot comprises of a ball shaped outer shell, which holds the entire mechanism, actuators, and electronics. It has several advantages over wheeled and legged robots. Owing to its spherical shape, it cannot overturn as opposed to wheeled and legged robots. It is maneuverable in any direction and can easily recover from collisions and obstacles. The spherical shape also eases the deployment strategy. It can be thrown, kicked or dropped at the site of operation with no risk of overturning or extruding actuator and electronics damage. This project uses the spherical robot developed in embedded control laboratory of systems and control engineering group, IIT Bombay. The design of this spherical robot is gearless and scalable in size. Hence, this project investigates its applications in various environments. The manually operated spherical robot would provide visual feedback and other application specific information to the operator for reconnaissance and search. 

Here is a very nice [video](https://www.youtube.com/watch?v=-q8D7BcLjac) of the robot of our smaller version of the robot. 

## Code organization
The code is categorized into two categories based on what hardware/system it runs on i.e. [Raspberry-Pi/Robot specific codes](https://github.com/syedadnanakhtar/sphericalRobot/tree/main/RPi%20specific%20Codes) and [PC-specific codes](https://github.com/syedadnanakhtar/sphericalRobot/tree/main/PC%20Specific%20Codes). 

### Robot-specific codes
- `myServo.py` runs on the Raspberry-Pi and is responsible for the following tasks
   - Receive commands from the android smartphone with remote android App v1.0 (with buttons and not joystick)
   - Actuate servo motor and dynamixel according to the command
   - Read data from the IMU and store it into a new Log file
- `myServo2.py` is an alternate version which also runs on Raspberry-Pi and should be used when Android app with joystick is used to send commands i.e. v1.1 
- `dynamixel.py` is a library that runs on Raspberry-Pi is being used currently to provide high-level control with the dynamixel.
- `ax.py` and `ax12.py` are also libraries enabling easy control of the dynamixel. They offer more command options such as synchronous commanding to both the dynamixels in one        packet specifying the speed of the motor movement. This feature is not present in `dynamixel.py.`
- `stream.sh` is a shell file which consists of a command that starts live video stream to a remote station.
### PC-specific codes
- Mplayer- This receives the video stream from the spherical robot and plays it. You can run it from the command prompt. First, make `...\mplayer-svn-37946-6` your       default directory and then simply run`netcam_stream.bat` which starts streaming. The content of the batch file is as follows 
  `mplayer -fps 200 -demuxer h264es ffmpeg://tcp://<RPI IP ADDRESS>:<PORT>`
  NOTE: first start streaming from the spherical bot end my running the `stream.sh` shell file.
- Lucas-Kanade optical flow tracker- `test.py`, `test1.py`, `test2.py`, `test3.py` are various codes containing optical flow implementation using openCV.
- Programs that assist with plotting and visualizing data:
  - `IMU_Plotter.py` reads a log file (generated by `myServo.py` running on Raspberry-Pi) saved on the computer and plots pitch, yaw and roll angles.
  - `trajectoryPlot.py` reads a .csv file (saved from VICON) and plot the trajectory of the robot in XY plane.
- Android Studio project named `MyClient2` is the code for the remote control app v1.0
- `Spherical_Bot.aia` is the MIT app inventor application for remote control app v1.1

### Packages/Libraries
- Camera streaming applications
  1. Steam using `motion` library. The streamed video opens on a web-browser or Remote app v1.1. Follow the [link](https://pimylifeup.com/raspberry-pi-webcamserver/) to set this up.
  2. Stream using netcat utility which saves you writing low level code based on UDP to stream video. On the remote station, an application called `Mplayer` will receive this stream and play. Find the instructions to set it up [here](https://nerdfuns.wordpress.com/2014/01/03/raspberry-pi-camera-modulehow-to-live-stream-to-your-pc/). After having done this, you simple have to run a shell file, `stream.sh`, to start streaming. The commands within this file takes in the stream through raspivid and broadcasts it on a port of your choice via netcat. This port number should be the same at both places, the shell file containing commands as well as MPlayer configuration file.
- Library to provide high level control for the dynamixel- `ax.py` and `ax12.py` as mentioned before.
- Package to interface MPU-9250 IMU with Raspberry-Pi. A configuration file named `RTIMULib.ini` is included in the folder. Download the GitHub repo [here](https://github.com/RTIMULib/RTIMULib2).
- Wiring-Pi to provide interface with the servo motors Download instructions [here](http://wiringpi.com/).
  
## Contact
The information and instruction here is non-exhaustive. Should you find any bug in the code, or have any questions, please feel free to reach out to me on `syed.akhtar[at]tum[dot]de`.
