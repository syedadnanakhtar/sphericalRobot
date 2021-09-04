import csv
from matplotlib import pyplot as plt

file_path = r"C:\Users\NCETIS\Documents\Experiments\26JanVicon\Front Command IMU Readings"
first_file = 74
last_file = 100#first_file
data = {}

plt.title("Pitch Angles (velocity = 10)")
plt.xlabel("time (sec)")
plt.ylabel("angle (degrees)")
plt.axis([0, 30, -60, 60])

for file_no in range(first_file,last_file+1):
    filename = file_path + r"\Log" + str(file_no) + ".csv"
    try:
        with open(filename, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for i in csvreader.fieldnames:
                data[i] = []
            for row in csvreader:
                for (k, v) in row.items():
                    if ((v != None) and ((k == "roll") or (k == "Time") or (k == "pitch"))):
                        data[k].append(float(v))

        pitch = data["pitch"][0:]
        roll = data["roll"][0:]
        t = data["Time"][0:]

        n = len(pitch)
        print "Total no. of points: ", n
        plt.plot(t, pitch,hold=True)
        plt.plot(t, roll, hold=True)
        plt.show()
    except IOError:
        print "Log"+str(file_no)+".csv not found"

plt.show()
