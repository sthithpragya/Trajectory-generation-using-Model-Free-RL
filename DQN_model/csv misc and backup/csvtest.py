import csv
import numpy as np

row = [0,0,0]
arr = np.zeros((3,2))


with open('names.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(arr[1])
