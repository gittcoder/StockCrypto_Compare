import asyncio
import websockets
import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from yahoo_fin.stock_info import *
import yfinance
import json


COLOR = 'white'
plt.rcParams['text.color'] = 'red'
plt.rcParams['axes.labelcolor'] = COLOR
plt.rcParams['xtick.color'] = COLOR
plt.rcParams['ytick.color'] = COLOR
plt.figure(facecolor='black')
ax = plt.axes()
ax.set_facecolor("black")


maindata={}
mydict={}
hist={}
time={}
pricesto={}
percentgain={}
name={}
disptim={}
n=0
i={}
i[1]=0


def cypt1(cid,crypttime):
    
    days=0
    disptim[i[1]]=crypttime
    if(crypttime.find("y")!=-1):
        days=int(crypttime[0:crypttime.find("y")])*365
        time[i[1]]=days
    elif(crypttime.find("mo")!=-1):
        days=int(crypttime[0:crypttime.find("m")])*30
        time[i[1]]=days
    elif(crypttime.find("d")!=-1):
        days=int(crypttime[0:crypttime.find("d")])
        time[i[1]]=days
    else:
        print("err")
    
    url = f'https://api.coingecko.com/api/v3/coins/{cid}/market_chart'
    load = {'vs_currency': 'usd', 'days' : days, 'interval' : 'daily'}
    response= requests.get(url, params=load)
    data=response.json()
    timestamp_list,pricelist=[],[]
    name[i[1]]= cid
    for price in data['prices']:
        timestamp_list.append(datetime.datetime.fromtimestamp(price[0]/1000))
        pricelist.append(price[1])
    maindata= {'x' :timestamp_list,'y' : pricelist}
    df=pd.DataFrame(maindata)
    initialval=df.iloc[0:1 , 1:]
    inivalconvert=pd.to_numeric(initialval['y'])
    s=str(inivalconvert)
    sp=s.find(" ")
    nam=s.find("N")
    g=s[sp+4:nam]
    inival2=float(g)
    md1=maindata['x']
    md2=maindata['y']
    plt.plot(md1,md2,label=cid)
    df2=df.tail(1)
    currval=df2.iloc[0:1 , 1:]
    pr=pd.to_numeric(currval['y'])
    w=str(pr)
    r=w.find(" ")
    q=w.find("N")
    z=w[r+4:q]
    finval2=float(z)
    percentgain[i[1]]= ((finval2-inival2)/inival2)*100
    pricesto[i[1]]=finval2
    i[1]=i[1]+1
    plt.legend()
    plt.savefig('images/sample.png')
    
    

def stock(x,tim):
    disptim[i[1]]=tim
    mydict[1]=yfinance.Ticker(x)
    hist[1]=mydict[1].history(period=tim)
    p=pd.DataFrame(hist[1]['Close'])
    q=str(p.head(1))
    lastins=q.rindex(" ")
    oldval=float(q[lastins+1:])
    if(tim.find("y")!=-1):
        time[i[1]]=int(tim[0:tim.find("y")])*365
    elif(tim.find("mo")!=-1):
        time[i[1]]=int(tim[0:tim.find("m")])*30
    elif(tim.find("y")!=-1):
        time[i[1]]=int(tim[0:tim.find("d")])
    name[i[1]]=x
    plt.plot(hist[1].index,hist[1]['Close'],label=x)
    pricesto[i[1]]=float(get_live_price(x))
    currentvalsto=float(get_live_price(x))
    print(type(currentvalsto))
    percentgain[i[1]]=((currentvalsto-oldval)/oldval)*100
    i[1] = i[1]+1
    plt.legend()
    plt.savefig('images/sample.png')

def output():
    keys=[]
    values=[]
    for i in range(len(pricesto)):
          keys.append("name"+str(i))
          values.append(name[i])

          keys.append("price"+str(i))
          values.append("{:.5f}".format(pricesto[i]))

          keys.append("gain"+str(i))
          values.append("{:.5f}".format(percentgain[i]))

          keys.append("time"+str(i))
          values.append(disptim[i])
    
    res = {keys[i]: values[i] for i in range(len(keys))}
    with open('scripts/json_files/result_stock_info.json', 'w') as fp:
        json.dump(res, fp)
    suggested={}
    mostexp=pricesto[0]
    cheap=pricesto[0]
    mostenam=""
    mostcheapnam=""
    for iterator in range(0,len(pricesto),1):
        suggested[iterator]=percentgain[iterator]/(pricesto[iterator]*time[iterator])
    sugg=suggested[0]
    suggnam=""
    pricesug=pricesto[0]
    for iterator in range(0,len(pricesto),1):
        if(pricesto[iterator]>=mostexp):
            mostexp=pricesto[iterator]
            mostenam=name[iterator]
        if(pricesto[iterator]<=cheap):
            cheap=pricesto[iterator]
            mostcheapnam=name[iterator]
        if(suggested[iterator]>=sugg):
            sugg=suggested[iterator]
            pricesug=pricesto[iterator]
            suggnam=name[iterator]
    keys=["most_exp","price","cheap_invest","cheap_price","suggested","sugg_price"]
    values=[str(mostenam),"{:.5f}".format(mostexp),str(mostcheapnam),"{:.5f}".format(cheap),str(suggnam),"{:.5f}".format(pricesug)]
    res = {keys[i]: values[i] for i in range(len(keys))}
    with open('scripts/json_files/result.json', 'w') as fp:
        json.dump(res, fp)

def websiteconnection(str1):
    lst1=str1.split()
    if(lst1[0]=="stock"):
        stock(lst1[1],lst1[2])
        output()
    elif(lst1[0]=="crypto"):
        cypt1(lst1[1],lst1[2])
        output()



@asyncio.coroutine
def hello(websocket, path):
    for i in range(2):
        name = yield from websocket.recv()
        greeting = "Hello {}!".format(name)
        yield from websocket.send(greeting)
        if name!="abcd":
            print("\n----Received ",name)
            print("----Plotting Graph")
            websiteconnection(name)
            print("----Success")

start_server = websockets.serve(hello, 'localhost',5557)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()