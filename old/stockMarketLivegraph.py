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


def choice():
    return int(input("1.Get Live update: \n2.Get Historical graph: "))
    


def getStock():
    global stockName
    global tickerSymbol

    while True:
        try:
            stockName=input("Enter stock name: ").title()
            assert stockName != None
            tickerSymbol=yf.Ticker(tickerNames.get(stockName))
        except (AttributeError,AssertionError):
            print("Invalid stock name")
        else:
            break

   

def getStockHistory():
    date=[]
    closingPrice=[]
    df=tickerSymbol.history(period='1d',interval='1m')
    for i in range(len(df.index)):
        date.append(str(df.index[i].time()))
        closingPrice.append(round(float(df.iloc[i,3]),3))
    

    return date,closingPrice


def latestPrice():
    df=tickerSymbol.history(period='1d',interval='5m')
    return str(df.index[-1].time()), round(float(df.iloc[-1,3]),3)

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
if history[1][-1]>history[1][0]:
    newColor='green'
else:
    newColor='red'
line,=axis.plot(history[0],history[1],color=newColor)
mlt.xticks(history[0][::len(history[0])//5])
mlt.grid()
mlt.xlabel("Time")
mlt.ylabel("Price in Dollars")
mlt.title(stockName + " (rough estimation)")
ani = FuncAnimation(fig, update, interval=60000, cache_frame_data=False)
mlt.show()

