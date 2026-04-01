import yfinance as yf
import json 
import numpy as np
import os
import matplotlib.pyplot as mlt
from matplotlib.animation import FuncAnimation
import time 


base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "stocks.json")

with open(file_path, "r") as file:
    tickerNames=json.load(file)


def getStock():
    global stockName
    global tickerSymbol
    global timePeriod

    while True:
        try:
            stockName=input("Enter stock name: ").title()
            assert stockName != None
            tickerSymbol=yf.Ticker(tickerNames.get(stockName))
        except (AttributeError,AssertionError):
            print("Invalid stock name")
        else:
            break
    
    while True:
        try:
            timePeriod=input("Time peroid: (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max): ")
            assert timePeriod in ['1d','5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
        except AssertionError:
            print("Invalid time period")
        else:
            break

    
    

def getStockHistory():
    date=[]
    closingPrice=[]
    if timePeriod == '1d':
        df=tickerSymbol.history(timePeriod,interval='1m')
        for i in range(len(df.index)):
            date.append(str(df.index[i].time()))
            closingPrice.append(round(float(df.iloc[i,3]),3))
    elif timePeriod == '5d':
        df=tickerSymbol.history(timePeriod,interval='1m')
        for i in range(len(df.index)):
            date.append(str(df.index[i]))
            closingPrice.append(round(float(df.iloc[i,3]),3))
    elif timePeriod in ['1mo','3mo','6mo']:
        df=tickerSymbol.history(timePeriod,interval='1d')
        for i in range(len(df.index)):
            date.append(str(df.index[i].date()))
            closingPrice.append(round(float(df.iloc[i,3]),3))
    else:
        df=tickerSymbol.history(timePeriod,interval='1d')
        for i in range(len(df.index)):
            date.append(str(df.index[i].date()))
            closingPrice.append(round(float(df.iloc[i,3]),3))

    return date,closingPrice



def latestPrice():
    if timePeriod == '1d':
        df=tickerSymbol.history(timePeriod,interval='1m')
        return str(df.index[-1].time()), round(float(df.iloc[-1,3]),3)
    elif timePeriod == '5d':
        df=tickerSymbol.history(timePeriod,interval='1m')
        return str(df.index[-1]), round(float(df.iloc[-1,3]),3)
    elif timePeriod in ['1mo','3mo','6mo']:
        df=tickerSymbol.history(timePeriod,interval='1d')
        return str(df.index[-1].date()), round(float(df.iloc[-1,3]),3)
    else:
        df=tickerSymbol.history(timePeriod,interval='1d')
        return str(df.index[-1].date()), round(float(df.iloc[-1,3]),3)
  

def update(frame):
    oldDate,oldPrice=history[0],history[1]
    lDate,lPrice=latestPrice()
    oldDate.append(lDate)
    oldPrice.append(lPrice)
    line.set_data(oldDate,oldPrice)
    axis.relim()
    return line,


stockDetails=getStock()
history=getStockHistory()
fig,axis=mlt.subplots()
line,=axis.plot(history[0],history[1])
mlt.xticks(history[0][::len(history[0])//5])
mlt.grid()
mlt.xlabel("Date")
mlt.ylabel("Price in Dollars")
mlt.title(stockName + " (rough estimation)")
ani = FuncAnimation(fig, update, interval=60000, cache_frame_data=False)
mlt.show()

