import yfinance as yf
import json 
import numpy as np
import os
import matplotlib.pyplot as mlt


base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "stocks.json")

with open(file_path, "r") as file:
    tickerNames=json.load(file)

stockName=""

def getStockDetails():
    global stockName
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

    return {"symbol":tickerSymbol,"time":timePeriod}
    

def getStockHistory(tickerSymbol,timePeriod):
    df=tickerSymbol.history(timePeriod)
    date=[]
    closingPrice=[]
    for i in range(len(df.index)):
        date.append(str(df.index[i].date()))
        closingPrice.append(round(float(df.iloc[i,3]),3))

    return np.array(date),np.array(closingPrice)

def plotStock(history):
    global stockName
    date=history[0]
    price=history[1]
    if price[0]>price[-1]:
        pickColor="red"
    else:
        pickColor="green"
    mlt.plot(date,price,color=pickColor)
    mlt.xticks(date[::len(date)//1])
    mlt.xlabel("Date")
    mlt.ylabel("Price in Dollars")
    mlt.title(stockName + " (rough estimation)")
    mlt.grid()
    mlt.show()



stockDetails=getStockDetails()
history=getStockHistory(stockDetails["symbol"],stockDetails["time"])
plotStock(history)


