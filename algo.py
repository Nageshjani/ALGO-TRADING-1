#import yfinance as yf
import pandas as pd
import talib as ta
#import matplotlib
#from matplotlib import pyplot as plt

df=pd.read_csv('Reliance1_SMA200_202.csv')
Close=df['Close']
df['SMA200']=ta.SMA(Close,timeperiod=200)
#df1=ta.SMA(Close, timeperiod=200)
#print(sma)
#df.to_csv('Reliance1_SMA200_202.csv')




Order_running=False
Price_To_Exit_For_Profit=0
Price_To_Exit_For_Lose=0
total_sold_amount=0
total_bought_amount=0
total_exit_amount=0
PL_SOLD=[]
PL_BOUGHT=[]

Shares=0
Share=[]
investment=10000
sold=[]
exit_sold=[]
bought=[]
exit_bought=[]

index_list=[]

for index, item in enumerate(df['Close'], start=0):   # Python indexes start at zero
    #selling stretegy
     if item<=df['SMA200'][index] and Order_running==False:
        Shares=int(investment/item)
        Share.append(Shares)
        index_list.append(index)
        sold.append(item)
        total_sold_amount=Shares*item
        #print("SOLD AT",index+2,"PRICE -->",int(item),'shares-->',Shares)
        print("SOLD AT",index+2,df['Date'][index],"PRICE -->",int(item),'shares-->',Shares)

        Price_To_Exit_For_Profit=item-10*(item/100)
        Price_To_Exit_For_Lose=item+2*(item/100)
        Order_running=True 
     if item <=Price_To_Exit_For_Profit  and Order_running==True:
        print("EXIT & PROFIT AT",index+2,df['Date'][index],"PRICE -->",int(item))
        total_exit_amount=Shares*item
        PL_SOLD.append(-(total_exit_amount-total_sold_amount))
        exit_sold.append(item)
        Order_running=False
     if item >=Price_To_Exit_For_Lose  and Order_running==True:
        print("EXIT & LOSE AT",index+2,df['Date'][index],"PRICE -->",int(item))
        total_exit_amount=Shares*item
        PL_SOLD.append(-(total_exit_amount-total_sold_amount))
        exit_sold.append(item)
        Order_running=False





print('--------------------------------------------------')


for index, item in enumerate(df['Close'], start=0):   # Python indexes start at zero
    #buying stretegy
     if item>=df['SMA200'][index] and Order_running==False:
        Shares=int(investment/item)
        Share.append(Shares)
        index_list.append(index)
        bought.append(item)
        total_bought_amount=Shares*item
        print("BOUGHT AT",index+2,df['Date'][index],"PRICE -->",int(item),'shares-->',Shares)
        Price_To_Exit_For_Profit=item+10*(item/100)
        Price_To_Exit_For_Lose=item-2*(item/100)
        Order_running=True 
     if item >=Price_To_Exit_For_Profit  and Order_running==True:
        print("EXIT & PROFIT AT",index+2,df['Date'][index],"PRICE -->",int(item))
        total_exit_amount=Shares*item
        PL_BOUGHT.append((total_exit_amount-total_bought_amount))
        exit_bought.append(item)
        Order_running=False
     if item <=Price_To_Exit_For_Lose  and Order_running==True:
        print("EXIT & LOSE AT",index+2,df['Date'][index],"PRICE -->",int(item))
        total_exit_amount=Shares*item
        PL_BOUGHT.append((total_exit_amount-total_bought_amount))
        exit_bought.append(item)
        Order_running=False



#print('---------------------------------')
#print(PL)



df['Share'] = pd.Series(Share)
df['sold_price'] = pd.Series(sold)
df['exit_sold'] = pd.Series(exit_sold)
df['PL_SOLD'] = pd.Series(PL_SOLD)

df['bought_price'] = pd.Series(bought)
df['exit_bought'] = pd.Series(exit_bought)
df['PL_BOUGHT'] = pd.Series(PL_BOUGHT)






#print(df['PL'].sum())
#sum=df['PL'].sum()
#print('NET RETURN',100*(sum/investment))

#df.to_csv('Reliance1_SMA205.csv')



print('-------------------------------------------------------------------------------------------')

sum=df['PL_SOLD'].sum()+df['PL_BOUGHT'].sum()
print("NET PL -->",sum,"ORIGINAL INVESTMENT WAS -->",investment)

print('NET RETURN % --->',100*(sum/investment),"%","IN PERIOD OF",(index/365),"YEARS")