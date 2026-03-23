import yfinance as yf
import json
import matplotlib.pyplot as mlt
import os

base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "stocks.json")

with open(file_path, "r") as file:
    tsym=json.load(file)

while True:
    try: 
        stock=input("Enter your Stock name: ").title()
        ticker=yf.Ticker(tsym.get(stock))
    except (AttributeError):
        print("Invalid stock name")
    else:
        break

while True:
    try:
        timeperiod=input("Enter time period (5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max): ")
        assert timeperiod in ['5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    except (AssertionError):
        print("Invalid date range")
    else:
        break

dateIndex=1
df=ticker.history(period=timeperiod)
date=[]
dateInYears=[]
price=[]
priceInDollars=[]
while True:
    if dateIndex>len(df.index):
        break
    else:
        date.append(str(df.index[dateIndex-1]).split()[0])
        dateInYears.append((str(df.index[dateIndex-1]).split()[0]).split("-")[0])
        price.append(df.iloc[dateIndex-1,3])
        dateIndex+=1
if df.iloc[len(df.index)-1,0]<df.iloc[0,3]:
    icolor='#9c0606'
else:
    icolor='green'
mlt.plot(date,price,color=icolor)
mlt.plot([max(price)]*len(date),color="black",linestyle="dotted",label="peak/lowest price")
mlt.plot([min(price)]*len(date),color="black",linestyle="dotted")
mlt.xticks(date[::len(date)//5],dateInYears[::len(date)//5])
mlt.xlabel("Date")
mlt.ylabel("Price in Dollars")
mlt.title(stock + " (rough estimation)")
mlt.legend()
mlt.grid()
mlt.show()

