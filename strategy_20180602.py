#測試投資報酬率: 4.7%

#零股不能信用交易(融資、融券)

#計算歷史到目前的MA值與標準差
def gc(p,price,ma,period):
    if p>=ma[period-1] and price[period-1]<=ma[period-1]:
        return True
    else:
        return False
def dc(p,price,ma,period):
    if p<=ma[period-1] and price[period-1]>=ma[period-1]:
        return True
    else:
        return False
def gc2s(p,price,upb,period):
    if p>=upb[period-1] and price[period-1]<=upb[period-1]:
        return True
    else:
        return False
def dc2s(p,price,upb,period):
    if p<=upb[period-1] and price[period-1]>=upb[period-1]:
        return True
    else:
        return False
def gcn2s(p,price,lwb,period):
    if p>=lwb[period-1] and price[period-1]<=lwb[period-1]:
        return True
    else:
        return False
def dcn2s(p,price,lwb,period):
    if p<=lwb[period-1] and price[period-1]>=lwb[period-1]:
        return True
    else:
        return False


    
def buy(p,position,stack,cash_amount):
    position+=1
    stack.append(p)
    cash_amount-=p
    
    return position,stack,cash_amount 

def sell(p,position,stack,cash_amount,acc_profit):
    position-=1
    last_buy_price = stack.pop()
    sell_price = p
    fee = 0.00145
    profit = sell_price - last_buy_price - fee
    cash_amount+=sell_price
    
    acc_profit+=profit
    
    return position,stack,cash_amount,acc_profit

def buy_info(p,position,stack,cash_amount):
    print('buy:$',p)
    print('position:',position)
    print('stack:',stack)
    print('cash amount:$',cash_amount) 
    
def sell_info(p,position,stack,cash_amount,acc_profit):
    print('sell:$',p)
    print('position:',position)
    print('stack:',stack)
    print('cash amount:$',cash_amount)
    print('accumulative profit: $',acc_profit)

    
def strategy(price,n_partition):
    cash_amount=1000.0/n_partition
    acc_profit = 0
    price = np.array(price)
    window = 20
    ma,s,upb,lwb= [np.nan]*(window-1),[np.nan]*(window-1),[np.nan]*(window-1),[np.nan]*(window-1)
    position = 0
    stack = []


    
    for period,p in enumerate(price):
        if period >=(window-1):
            ma.append(np.mean(price[period-window+1:period+1]))
            s.append(np.std(price[period-window+1:period+1]))
            lwb.append(ma[period]+s[period])
            upb.append(ma[period]-s[period])
    
            if period>=window:
                if gc(p,price,ma,period) and cash_amount-p>=0:
                    position,stack,cash_amount=buy(p,position,stack,cash_amount)    
                    #buy_info(p,position,stack,cash_amount)
                
                if dc(p,price,ma,period) and len(stack)>0:
                    position,stack,cash_amount,acc_profit=sell(p,position,stack,cash_amount,acc_profit)
                    #sell_info(p,position,stack,cash_amount,acc_profit)
                   
                if gc2s(p,price,ma,period) and len(stack)>0:
                    position,stack,cash_amount,acc_profit=sell(p,position,stack,cash_amount,acc_profit)
                    #sell_info(p,position,stack,cash_amount,acc_profit)
                    
                if dc2s(p,price,ma,period) and len(stack)>0:
                    position,stack,cash_amount,acc_profit=sell(p,position,stack,cash_amount,acc_profit)
                    #sell_info(p,position,stack,cash_amount,acc_profit)
                    
                if gcn2s(p,price,ma,period) and cash_amount-p>0:
                    position,stack,cash_amount=buy(p,position,stack,cash_amount)
                    #buy_info(p,position,stack,cash_amount)
                if dcn2s(p,price,ma,period) and cash_amount-p>0:
                    position,stack,cash_amount=buy(p,position,stack,cash_amount)
                    #buy_info(p,position,stack,cash_amount)
    return acc_profit

from pandas_datareader import data as pdr
import fix_yahoo_finance as yf

yf.pdr_override()
start = '2017-01-01'
end = '2017-12-31'

#台股所有ADR的名稱
ADR = [ 'CATY','ASX','SPIL','AUO','SINA','TSM','UMC','BVSN','CA','GIGM','LSCC','SSTI']
#抓取國泰的資料
Price = []
portfolio_acc_profit = 0
cash_amount = 1000.0
for adr in ADR:
    print(adr)
    df = pdr.get_data_yahoo(adr,start=start,end=end)
    ts = df['Open'].tolist()
    Price.append(ts)
for price in Price:
    acc_profit = strategy(price,len(Price))
    portfolio_acc_profit+=acc_profit
print('Portfolio Return Rate:',portfolio_acc_profit/cash_amount*100.0,'%')