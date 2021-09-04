
import time
import wiringpi
import socket
import sys
import dynamixel
import RPi.GPIO as GPIO
import threading
import getopt
sys.path.append('.')
import RTIMU
import os.path
import math
import csv

#Setting up pwm for servo
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(12, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)


target = 0
present = 0
thread_flag = True

class ServoControlThread(threading.Thread):
        def run(self):
            print ("thread started")
            while(1 and thread_flag):
                if target == 0:
                    present = 0
                elif target > present:
                    if present == 0:
                        present = 155
                    present = present + 1
                elif target < present:
                    if present == 0:
                        present = 155 
                    present = present - 1
                wiringpi.pwmWrite(12 , present)
                time.sleep(0.5)

class CSVWriterThread(threading.Thread):
        def run(self):
			SETTINGS_FILE = "RTIMULib"

			print("Using settings file " + SETTINGS_FILE + ".ini")
			if not os.path.exists(SETTINGS_FILE + ".ini"):
			  print("Settings file does not exist, will be created")

			s = RTIMU.Settings(SETTINGS_FILE)
			imu = RTIMU.RTIMU(s)

			print("IMU Name: " + imu.IMUName())

			if (not imu.IMUInit()):
				print("IMU Init Failed")
				sys.exit(1)
			else:
				print("IMU Init Succeeded")

			imu.setSlerpPower(0.02)
			imu.setGyroEnable(True)
			imu.setAccelEnable(True)
			imu.setCompassEnable(True)

			poll_interval = 10#imu.IMUGetPollInterval()

			files = [f for f in os.listdir('.') if os.path.isfile(f) and os.path.splitext(f)[1] == ".csv"]
			new_file_no = 1
			for f in files:
				existing_file_no = (os.path.splitext(f)[0])[3:]
				if existing_file_no.isdigit():
					n = int(existing_file_no)
					if n >= new_file_no:
						new_file_no = n + 1

			new_file_name = "Log" + str(new_file_no) + ".csv"
			print new_file_name, "created"

			with open(new_file_name, 'wb') as f:
				writer = csv.writer(f)

				label_row = []
				label_row.append('Time');
				label_row.append('roll');
				label_row.append('pitch');
				label_row.append('yaw');
				label_row.append('Accel_x');
				label_row.append('Accel_y');
				label_row.append('Accel_z');
				label_row.append('Gyro_x');
				label_row.append('Gyro_y');
				label_row.append('Gyro_z');
				label_row.append('Compass_x');
				label_row.append('Compass_y');
				label_row.append('Compass_z');

				writer.writerow(label_row);
				start_time = time.time()

				while thread_flag:

					if imu.IMURead():
						data = imu.getIMUData()
						fusionPose = data["fusionPose"]
						rawAccelData = data["accel"]
						rawCompassData = data["compass"]
						rawGyroData = data["gyro"]
						fuse_row = []

						elapsed_time = time.time() - start_time

						fuse_row.append(elapsed_time);
						fuse_row.append(math.degrees(fusionPose[0]));
						fuse_row.append(math.degrees(fusionPose[1]));
						fuse_row.append(math.degrees(fusionPose[2]));
						fuse_row.append(rawAccelData[0]);
						fuse_row.append(rawAccelData[1]);
						fuse_row.append(rawAccelData[2]);
						fuse_row.append(rawGyroData[0]);
						fuse_row.append(rawGyroData[1]);
						fuse_row.append(rawGyroData[2]);
						fuse_row.append(rawCompassData[0]);
						fuse_row.append(rawCompassData[1]);
						fuse_row.append(rawCompassData[2]);

						writer.writerow(fuse_row);
						time.sleep(poll_interval*1.0/1000.0)


#Setting up Server for Android control
HOST = ''
PORT = 6000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("socket created.")
try:
        s.bind((HOST,PORT))
except socket.error as msg:
        print ('Bind failed. Error code: ' + str(msg))
        sys.exit()
print ('Socket bind complete')
s.listen(10)
print ('socket now listening')
conn, addr = s.accept()
v =10
p =10
id1 = 1
id2 = 2
prev_data=' '

servothread = ServoControlThread(name = "Thread1")
servothread.start()
csvthread = CSVWriterThread(name = "Thread2")
csvthread.start()

vert_1=150 #higher value means front motor towards right
vert_2=150 #higher value means rear motor towards left

while True:
        data=conn.recv(4)
       
        if not data: break
        data = data.decode('ascii')
        if prev_data[0] == data[0]:
            continue
        prev_data = data
        print (data)

        if data[0] == 'p': #set pendulum angle
            p = int(data[1:])

        elif data[0] == 'v': #set velocity
            v = int(data[1:])

        if data[0] == 'h': #stop robot
            target = 0
            dynamixel.write_angle(vert_1 , id1)
            dynamixel.write_angle(vert_2 , id2)

        if data[0] == 'w': # move forward
            dynamixel.write_angle(vert_1 , id1)
            dynamixel.write_angle(vert_2 , id2)
            target = 155 + v

        if data[0] == 's': #move back
            target = 155 - v
            dynamixel.write_angle(vert_1 , id1)
            dynamixel.write_angle(vert_2 , id2)

        if data[0] == 'e': #move front right
            target = 155 + v
            dynamixel.write_angle(vert_1+p , id1)
            dynamixel.write_angle(vert_2-p , id2)

        if data[0] == 'q': #move front left
            target = 155 + v
            dynamixel.write_angle(vert_1-p , id1)
            dynamixel.write_angle(vert_2+p , id2)

        if data == 'a': #move left
            target = 0
            dynamixel.write_angle(vert_1-p , id1)
            dynamixel.write_angle(vert_2+p , id2)

        if data == 'd': #move right
            target = 0
            dynamixel.write_angle(vert_1+p , id1)
            dynamixel.write_angle(vert_2-p , id2)

        if data[0] == 'x': #move back right
            target = 155 - v
            dynamixel.write_angle(vert_1+p , id1)
            dynamixel.write_angle(vert_2-p , id2)


        if data[0] == 'z': #move back left
            target = 155 - v
            dynamixel.write_angle(vert_1-p , id1)
            dynamixel.write_angle(vert_2+p , id2)

print ('Socket is now closing')
conn.close()
thread_flag = False
wiringpi.pwmWrite(12, 0)
