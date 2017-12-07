## aggregate the nine hundred

import csv
import pandas as pd

root = '../modeloutput/'
frames = []
for floor in range(1700, 2000, 50):
    sourcefile = root + 'the900_' + str(floor) + '.csv'
    thisframe = pd.read_csv(sourcefile)
    frames.append(thisframe)

df = pd.concat(frames)
df.head()

df.to_csv('../plotdata/the900.csv', index = False)
