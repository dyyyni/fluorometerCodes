import csv
import spikeDetection

data2 = [1,1,1.1,1,0.9,1,1,1.1,1,0.9,1,1.1,1,1,0.9,1,1,1.1,1,1,1,1,1.1,0.9,1,1.1,1,1,0.9,
       1,1.1,1,1,1.1,1,0.8,0.9,1,1.2,0.9,1,1,1.1,1.2,1,1.5,1,3,2,5,3,2,1,1,1,0.9,1,1,3,
       2.6,4,3,3.2,2,1,1,0.8,4,4,2,2.5,1,1,1]

data = [0]


detector = spikeDetection.real_time_peak_detection(data, 100, 10, 0)

i = 0
with open('longMeas01.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, dialect='excel')
    for row in reader:
        if i > 2:
            detector.thresholding_algo(int(row[0]))
        i += 1

detector.thresholding_algo(580000)
detector.thresholding_algo(500000)

print(detector.signals.count(1))