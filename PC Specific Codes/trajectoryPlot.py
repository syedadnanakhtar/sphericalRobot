import csv
from matplotlib import pyplot as plt
import transforms3d as tf
import math

file_path = r"C:\Users\NCETIS\Documents\Experiments\26JanVicon"
first_file = 110
last_file = 120#first_file + 1
data = {}
useless_lines = 3
x_samples = -1
y_samples = -1
plt.title("Trajectory (10 deg right pendulum angle)")
plt.xlabel("x (mm)")
plt.ylabel("y (mm)")
plt.axis([-4000, 4000, -4000, 4000])
#plt.ion()

x_new=[]
y_new=[]

for file_no in range(first_file,last_file):
    if file_no == 96:
        file_no = file_no + 1
    filename = r"\trajectory " + str(file_no) + ".csv"
    filename = file_path + filename

    with open(filename, 'r') as csvfile:
        for j in range(useless_lines):
            garb = csvfile.readline()
        csvreader = csv.DictReader(csvfile)
        for i in csvreader.fieldnames:
            data[i] = []
        for row in csvreader:
            for (k, v) in row.items():
                if ((v != None) and (v != '') and (v!= "rad") and (v != "mm") and ((k == "TX") or ((k == "TY") or (k == "RX") or (k == "RY") or (k == "RZ") or (k == "RW")))):
                    data[k].append(float(v))
                #elif ((v != '') and (v != None) and (v != "mm") and ((k == "RX")) or (k == "RY") or (k == "RZ") or (k == "RW"))):
                #    print "value: ", float(v)

    x = data["TX"][0: x_samples]
    y = data["TY"][0: y_samples]
    rx = data["RX"][0: y_samples]
    ry = data["RY"][0: y_samples]
    rz = data["RZ"][0: y_samples]

    RX = [math.degrees(r) for r in rx]
    RY = [math.degrees(r) for r in ry]
    RZ = [math.degrees(r) for r in rz]

    n = len(x)
    print "Total no. of points: ", n
    time = range(0, n)
    # plt.plot(time,RZ)


    j = 0
    x_new=[]
    y_new=[]
    for y_val in y:
        #print y_val
        if y_val < 4000:
            y_new.append(y_val)
            x_new.append(x[j])

        j = j + 1
    plt.plot(x_new, y_new)

    # dist = 0
    # for i in range(1,len(x_new)):
    #     dist = dist + math.sqrt( (x_new[i] - x_new[i-1])**2 + (y_new[i] - y_new[i-1])**2 )
    # print "Total Distance travelled (mm): ",dist
    # print "Total Time: ", n/29.3
    # print "Speed (cm/s)", (dist*29.3/(n*100))

# alpha = []
# beta = []
# gamma = []
#for i in range(0,n):
    #angle = tf.euler.quat2euler([rw[i],rx[i], ry[i], rz[i]])
    #alpha.append(math.degrees(angle[0]))
    #beta.append(math.degrees(angle[1]))
    #gamma.append(math.degrees(angle[2]))

plt.show()