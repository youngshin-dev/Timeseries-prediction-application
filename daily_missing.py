#!/bin/python3

import math
import os
import random
import re
import sys


#
# Complete the 'calcMissing' function below.
#
# The function accepts STRING_ARRAY readings as parameter.
#

import pandas as pd
import numpy as np
import statsmodels.api as sm
from math import sqrt
from datetime import datetime


def calcMissing(readings):
    # Write your code here
    dates=[]
    data_list = []
    #print(readings)
    #del(readings[0])
    for reading in readings:
        reading_list=reading.split("\t")
        date = datetime.strptime(reading_list[0],'%m/%d/%Y %H:%M:%S').date()
        dates.append(date)
        data_list.append(reading_list[1])
    time_series = pd.DataFrame({'level':data_list}, index=dates)
    time_series = time_series.apply(lambda x:pd.to_numeric(x,errors='coerce'))
    #print(time_series.head(20))
    null_inds=time_series[time_series['level'].isnull()].index.tolist()
    #for i in range(len(null_inds)):
    #    null_inds[i] = null_inds[i].strftime("%m-%d-%Y")
    #print(null_inds)
    
    #time_series.dropna(inplace=True)
    
    best_order=(1,1,2)
    best_seasonal_order = (1,1,2,8)

    model = sm.tsa.statespace.SARIMAX(time_series['level'],
                                          order=best_order,
                                          seasonal_order=best_seasonal_order,
                                          enforce_stationarity=True,
                                          enforce_invertibility=True)
    fitted = model.fit(disp=0)
    
    for i in range(len(null_inds)):
        print(fitted.predict(null_inds[i], null_inds[i],dynamic=False).values[0])
        
        
    
    
if __name__ == '__main__':