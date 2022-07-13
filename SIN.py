import numpy as np
import pandas as pd

rpos = np.zeros(100) #USE this to store Positions

def getMyPosition(prcSoFar):
    global currentPos
    global rpos
    (nInst,nt) = prcSoFar.shape
    prcSoFar = pd.DataFrame(prcSoFar)
    prcSoFar1 = prcSoFar
    prcSoFar = prcSoFar.transpose()
    trade_count = np.zeros(nInst)
    long_ema = prcSoFar.ewm(span=40, adjust=False).mean()
    short_ema = prcSoFar.ewm(span=8, adjust=False).mean()
    grad_long_ema = long_ema.diff(axis=0)
    grad_short_ema = short_ema.diff(axis=0).ewm(span=3, adjust=False).mean()
    std_of_price=prcSoFar.std()
    std_of_price_grad= prcSoFar.diff(axis=0).std()
    posSize = 1500
    buy = posSize
    sell = -posSize
    buybig = posSize*6
    sellbig = -posSize*6
    r_pos = np.zeros(nInst)
    curr_pos = np.zeros(nInst)
    ev = np.zeros(nInst)
    stock_pnl = np.zeros(nInst)
    days = prcSoFar.shape[0]

    for m in range(days):
        for n in range(0,100):
            if std_of_price_grad[n]>0.6 and prcSoFar.loc[nt-1, n] > short_ema.loc[nt-1, n] and  grad_short_ema.loc[nt-1, n] < 0 :
                r_pos[n] += sell  
                
            if std_of_price_grad[n]>0.6 and prcSoFar.loc[nt-1, n] < short_ema.loc[nt-1, n] and grad_short_ema.loc[nt-1, n] > 0:
                r_pos[n] += buy    
            if std_of_price[n]<0.02 and grad_short_ema.loc[nt-1, n]  <0:
                r_pos[n] += sell 
                
                if r_pos[n]<-posSize:
                    r_pos[n] += sell
            
            if std_of_price[n]<0.02 and grad_short_ema.loc[nt-1, n] > 0:
                r_pos[n] += buy
                
                if r_pos[n]>posSize:
                    r_pos[n] = buy
            if std_of_price_grad[n]<0.02 and grad_long_ema.loc[nt-1, n]  <0:
                r_pos[n] += sell 
                
                if r_pos[n]<-posSize:
                    r_pos[n] += sell   
            
            if std_of_price_grad[n]<0.02 and grad_long_ema.loc[nt-1, n] > 0:
                r_pos[n] += buy
                
                if r_pos[n]>posSize:
                    r_pos[n] += buy
            stock_pnl[n] += curr_pos[n] * prcSoFar.loc[m, n] - curr_pos[n] * prcSoFar.iloc[m-1, n]
            curr_pos = r_pos

    for i in range(0,100):
        ev[i] = 0
        if trade_count[i] > 0:
            ev[i] = stock_pnl[i]
        if std_of_price_grad[i]>0.6 and prcSoFar.loc[nt-1, i] > short_ema.loc[nt-1, i] and  grad_short_ema.loc[nt-1, i] < 0 :
            if ev[i] == 0:
                rpos[i] += sell  
            if ev[i] > 0:
                rpos[i] += sellbig
        if std_of_price_grad[i]>0.6 and prcSoFar.loc[nt-1, i] < short_ema.loc[nt-1, i] and grad_short_ema.loc[nt-1, i] > 0:
            if ev[i] == 0:
                rpos[i] += buy  
            if ev[i] > 0:
                rpos[i] += buybig   
        if std_of_price[i]<0.02 and grad_short_ema.loc[nt-1, i]  <0:
            if ev[i] == 0:
                rpos[i] += sell  
            if ev[i] > 0:
                rpos[i] += sellbig    
        
        if std_of_price[i]<0.02 and grad_short_ema.loc[nt-1, i] > 0:
            if ev[i] == 0:
                rpos[i] += buy  
            if ev[i] > 0:
                rpos[i] += buybig   

        if std_of_price_grad[i]<0.02 and grad_long_ema.loc[nt-1, i]  <0:
            if ev[i] == 0:
                rpos[i] += sell  
            if ev[i] > 0:
                rpos[i] += sellbig  
        
        if std_of_price_grad[i]<0.02 and grad_long_ema.loc[nt-1, i] > 0:
            if ev[i] == 0:
                rpos[i] += sell  
            if ev[i] > 0:
                rpos[i] += sellbig
    currentPos = rpos
    return currentPos
