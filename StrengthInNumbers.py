import numpy as np
import pandas as pd

rpos = np.zeros(100) #USE this to store Positions
def getMyPosition(prcSoFar):
    global currentPos
    global rpos
    global sumPnLperstock
    (nInst,nt) = prcSoFar.shape
    prcSoFar = pd.DataFrame(prcSoFar)
    prcSoFar = prcSoFar.transpose()
    long_ema = prcSoFar.ewm(span=10, adjust=False).mean()
    short_ema = prcSoFar.ewm(span=4, adjust=False).mean()
    grad_long_ema = long_ema.diff(axis=0)
    grad_short_ema = short_ema.diff(axis=0)
    std_of_price=prcSoFar.pct_change(axis=0).std()
    std_of_price_grad= prcSoFar.pct_change(axis=0).std()
    posSize = 3500
    buy = posSize
    sell = -posSize
    ev = np.zeros(nInst)
    days = prcSoFar.shape[0]
    negrange = [0, 20, 24, 25, 27, 30, 42, 45, 46, 50, 56, 64, 77, 84, 87, 88, 90]
    for i in range(0,100):
        ev[i] = 0
        if i not in negrange:
            if std_of_price_grad[i]>0.15 and prcSoFar.iloc[nt-1, i] > short_ema.iloc[nt-1, i] and  grad_short_ema.iloc[nt-1, i] < 0 :
                if ev[i] == 0:
                    rpos[i] = sell
                if ev[i] > 0:
                    rpos[i] = sell
            if std_of_price_grad[i]>0.15 and prcSoFar.iloc[nt-1, i] < short_ema.iloc[nt-1, i] and grad_short_ema.iloc[nt-1, i] > 0:
                if ev[i] == 0:
                    rpos[i] = buy
                if ev[i] > 0:
                    rpos[i] = buy 
            if std_of_price[i]<0.01 and grad_short_ema.iloc[nt-1, i]  <0:
                if ev[i] == 0:
                    rpos[i] = sell
                if ev[i] > 0:
                    rpos[i] = sell  
            
            if std_of_price[i]<0.01 and grad_short_ema.iloc[nt-1, i] > 0:
                if ev[i] == 0:
                    rpos[i] = buy
                if ev[i] > 0:
                    rpos[i] = buy 
            if std_of_price_grad[i]<0.01 and grad_long_ema.iloc[nt-1, i]  <0:
                if ev[i] == 0:
                    rpos[i] = sell
                if ev[i] > 0:
                    rpos[i] = sell
            
            if std_of_price_grad[i]<0.01 and grad_long_ema.iloc[nt-1, i] > 0:
                if ev[i] == 0:
                    rpos[i] = sell
                if ev[i] > 0:
                    rpos[i] = sell
    currentPos = rpos
    return currentPos
