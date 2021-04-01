#This program takes stock prices of the past 5 days and predict the prices for the next day. 
#It then implements simple logic of buying the stock that will rise the most and sell the stock that will drop the most.
import sklearn.metrics as metrics
import pandas as pd
import numpy as np

# !/bin/python3

import math
import os
import random
import re
import sys

import statsmodels.api as sm
from math import sqrt
from datetime import datetime


def parse_data(data, df_dict):
    money = float(data[0].split(" ")[0])
    num_stock = {}
    del (data[0])

    for i in range(len(data)):
        d_list = data[i].split(" ")
        num_stock[d_list[0]] = float(d_list[1])
        dates = pd.date_range(end="2012-10-1", periods=5)
        if d_list[0] not in df_dict:
            df_dict[d_list[0]] = pd.DataFrame({d_list[0]: [d_list[2], d_list[3], d_list[4], d_list[5], d_list[6]]},
                                              index=dates)

    for key in df_dict:
        df_dict[key][key] = df_dict[key][key].astype(float)

    return money, num_stock


def PredictNext(df_dict):
    forecasts = {}
    for key in df_dict:
        best_order = (1, 1, 0)
        best_seasonal_order = (1, 1, 0, 1)

        model = sm.tsa.statespace.SARIMAX(df_dict[key][key],
                                          order=best_order,
                                          seasonal_order=best_seasonal_order,
                                          enforce_stationarity=True,
                                          enforce_invertibility=True)
        fitted = model.fit(disp=0)

        forecasts[key] = fitted.predict('2012-10-02', '2012-10-02', dynamic=False).values[0]

        # print(forecasts)
    return forecasts


def BuySell(forecasts, df_dict, money, num_stock):
    diffs = {}
    # for key in df_dict:
    #    print(df_dict[key].head())
    #    print(forecasts[key])
    for key in df_dict:
        diffs[key] = df_dict[key][-1:].values[0][0] - forecasts[key]
        # print(df_dict[key][-1:].values[0][0])
        # print(forecasts[key])
    # print(diffs)
    up = {}
    down = {}
    for key in diffs:
        if diffs[key] > 0:
            up[key] = (num_stock[key], diffs[key])
        if diffs[key] < 0:
            down[key] = (num_stock[key], diffs[key])

    if len(up) == 0 and len(down) == 0:
        return [0]
    elif len(up) > 0 and len(down) == 0 and money >0:
        buy = max(up, key=diffs.get)
        num_buy = money / df_dict[buy][-1:].values[0][0]
        if num_buy > 0:
            return [1, (buy, 'BUY', num_buy)]
        else:
            return[0]
    elif len(up) == 0 and len(down) > 0:
        profit = {}
        for key in down:
            profit[key] = -(down[key][0] * down[key][1])
        max_key = max(profit, key=profit.get)
        if profit[max_key] > 0:
            return [1, (max_key, 'SELL', down[max_key][0])]
        else:
            return [0]
    elif len(up)> 0 and len(down) > 0 and money > 0:
        buy = max(up, key=diffs.get)
        num_buy = math.floor(money / df_dict[buy][-1:].values[0][0])
        profit = {}
        for key in down:
            profit[key] = -(down[key][0] * down[key][1])
        max_key = max(profit, key=profit.get)
        if profit[max_key] > 0 and num_buy >0:
            return [2, (buy, 'BUY', num_buy), (max_key, 'SELL', down[max_key][0])]
        elif profit[max_key] > 0 and num_buy == 0:
            return [1, (max_key, 'SELL', down[max_key][0])]
        elif profit[max_key] == 0 and num_buy > 0:
            return [1, (buy, 'BUY', num_buy)]
        else:
            return [0]


if __name__ == '__main__':
    def main():

        data = []
        df_dict = {}
        for line in sys.stdin:
            if 'E' == line.rstrip():
                break
            data.append(line.rstrip())

        money, num_stock = parse_data(data, df_dict)

        # for i in df_dict:
        #    print(df_dict[i][i].dtypes)

        forecasts = PredictNext(df_dict)

        buy_sell = BuySell(forecasts, df_dict, money, num_stock)

        if buy_sell[0] == 0:
            print(0)
        else:
            print(buy_sell[0])
            for i in range(buy_sell[0]):
                print(buy_sell[i + 1][0], buy_sell[i + 1][1], buy_sell[i + 1][2])

if __name__ == '__main__':
    main()



