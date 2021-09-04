# Servo Control
import time
import wiringpi
import socket
import sys
import dynamixel
import dynamixel2
import RPi.GPIO as GPIO

#Setting up pwm for servo
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(12, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

target = 0
present = 0
thread_flag = True

#Setting up Servo for Android control
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
id1 = 1
id2 = 2
prev_data=' '
vert_1 =145 #higher value means motor 1 (front motor) towards right
vert_2 = 151 #higher value means motor 2 (rear motor) towards left


while True:
        data=conn.recv(1024)
       
        if not data: break
        
        pos_b = data.rfind('b')
        data =  data[:pos_b]
        pos_a = data.rfind('a')
        data = data[pos_a+1:]
        pos_y = str.find(data , 'y')

        if (pos_a != -1 and pos_b !=-1 and pos_a < pos_b):
            str_x = data[1:pos_y]
            str_y = data[pos_y+1:]

            x = int(str_x)-50
            y=  int(str_y)-50

            p=x/2
            v=y/2

            wiringpi.pwmWrite(12 , 155+v)
            dynamixel.write_angle(vert_1+p , id1)
            dynamixel.write_angle(vert_2-p , id2)
            if v==0:
                wiringpi.pwmWrite(12 , 0)

            print 'Data: ',data, ' | P: ',p, ' | V: ',v


print ('Socket is now closing')
conn.close()
thread_flag = False
wiringpi.pwmWrite(12, 0)
