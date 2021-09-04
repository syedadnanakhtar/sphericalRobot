import serial
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
port = serial.Serial("/dev/ttyAMA0", baudrate = 1000000, timeout = 3.0)


def write_angle( angle, i):
    GPIO.output(17 , GPIO.HIGH)
    time.sleep(0.0005)
    port.write(bytearray.fromhex(get_message(angle,i)))
    time.sleep(0.1)
    GPIO.output(17, GPIO.LOW)


def get_message(angle , id):
    id = str(id)
    command = "FF FF" + " 0" + id + " 05 03 1E " + (get_hex_angle(angle))[1] + " " + (get_hex_angle(angle))[0]
    command = command + " " +  get_crc( command )
    return command


def get_hex_angle(angle_deg):
    angle_deg = angle_deg / 0.29
    str = ("0x%0.2X"%angle_deg)[2:] #integer to hexadecimal
    for i in range(1 , 4 - len(str) + 1):
        str = "0" + str
    #print str
    return (str[:2] , str[2:])


def get_crc(msg):
    sum = int(msg[6:8],16)+int(msg[9:11],16) + int(msg[12:14],16) + int(msg[15:17],16) + int(msg[18:20],16) + int(msg[21:23],16)
    bin_sum = bin(sum)
    len_init = len(bin_sum)
    if (len(bin_sum) - 2) % 4 == 0:
        l = len(bin_sum)
    else:
        l = len(bin_sum) + 4 - (len(bin_sum) - 2) % 4
    for i in range(2 , l):
        if i <= len_init - 1 and bin_sum[i] == '0':
            bin_sum = bin_sum[:i] + "1" + bin_sum[i+1:]
        elif i > len_init - 1:
            bin_sum = bin_sum + "1"
    x_int = int(bin_sum,2)
    x_res_int = sum ^ x_int
    x_res_hex = ("0x%0.2X" % x_res_int)
    return x_res_hex[ len(x_res_hex) - 2:]

#print "Hex equivalent of angle is ", get_hex_angle(59.45)
#print "Generated CRC is ",get_crc("FF FF FE 05 03 1E CD 00")
#print "Entire message is ", get_message(59.45,1)
#write_angle(150,1)
