#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'predictMissingHumidity' function below.
#
# The function is expected to return a FLOAT_ARRAY.
# The function accepts following parameters:
#  1. STRING startDate
#  2. STRING endDate
#  3. STRING_ARRAY knownTimestamps
#  4. FLOAT_ARRAY humidity
#  5. STRING_ARRAY timestamps
#
import pandas as pd
import numpy as np
import statsmodels.api as sm
from math import sqrt
from datetime import datetime

def predictMissingHumidity(startDate, endDate, knownTimestamps, humidity, timestamps):
    # Write your code here
    dates =[]
    for i in range(len(knownTimestamps)):
        dates.append(datetime.strptime(knownTimestamps[i],'%Y-%m-%d %H:%M'))
    time_series = pd.DataFrame({'level':humidity}, index=dates)
    time_series.index = pd.DatetimeIndex(time_series.index).to_period('H')
    
    best_order=(1,1,1)
    best_seasonal_order = (1,1,1,6)

    model = sm.tsa.statespace.SARIMAX(time_series['level'],
                                          order=best_order,
                                          seasonal_order=best_seasonal_order,
                                          enforce_stationarity=True,
                                          enforce_invertibility=True)
    fitted = model.fit(disp=0)
    
    missing_dates = []
    for i in range(len(timestamps)):
        dates.append(datetime.strptime(timestamps[i],'%Y-%m-%d %H:%M'))
    
    prediction =[]
    for i in range(len(missing_dates)):
        prediction.append(fitted.predict(missing_dates[i], missing_dates[i],dynamic=False).values[0])
        
    return prediction
        
if __name__ == '__main__':
    def main():
        fptr = open(os.environ['OUTPUT_PATH'], 'w')

        startDate = input()

        endDate = input()

        knownTimestamps_count = int(input().strip())

        knownTimestamps = []

        for _ in range(knownTimestamps_count):
            knownTimestamps_item = input()
            knownTimestamps.append(knownTimestamps_item)

        humidity_count = int(input().strip())

        humidity = []

        for _ in range(humidity_count):
            humidity_item = float(input().strip())
            humidity.append(humidity_item)

        timestamps_count = int(input().strip())

        timestamps = []

        for _ in range(timestamps_count):
            timestamps_item = input()
            timestamps.append(timestamps_item)

        result = predictMissingHumidity(startDate, endDate, knownTimestamps, humidity, timestamps)
    
        fptr.write('\n'.join(map(str, result)))
        fptr.write('\n')

        fptr.close()
    
if __name__ == '__main__':
    main()
