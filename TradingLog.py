#File used to test most fit individual for trading accuracy

import GeneticAlgorithm

individual = [35, 13, 94, 15, 19, 20, 86, 14]

ticker = 'V'

data_frame = GeneticAlgorithm.acquire_data(ticker)

close = data_frame.Close
sma50 = data_frame.SMA50
sma200 = data_frame.SMA200
date = 0
traits = []
buy = 0
sell = 1
ret = 0
capital = 10000
win = 0
trade = 0

print(individual)

for i in range(0, len(close)):
    date = date + 1
    if sma50[i] > sma200[i]: #Uptrend
        traits = individual[4:8]
        #print('Uptrend')
    elif sma200[i] > sma50[i]: #Downtrend
        traits = individual[0:4]
        #print('Downtrend')
    
    #Form logic based on individuals traits
    buy_value = traits[0]
    buy_interval = traits[1]
    sell_value = traits[2]
    sell_interval = traits[3]

    #Form RSI dataframes for return analysis
    rsi_buy_string = 'RSI' + str(buy_interval)
    rsi_buy = data_frame[rsi_buy_string]
    rsi_sell_string = 'RSI' + str(sell_interval)
    rsi_sell = data_frame[rsi_sell_string]

    rsi_value_buy = round(rsi_buy[i])
    prev_buy_value = round(rsi_buy[i - 1])
    rsi_value_sell = round(rsi_sell[i])
    #print('RSI buy: ', buy_value, 'RSI buy in dataframe: ', rsi_value_buy)

    #Buy and sell actions
    if rsi_value_buy == buy_value and buy == 0:
        #print('Buy Logic 1')
        buy_price = close[i]
        shares = round(capital / buy_price) - 1
        bought = shares * buy_price
        buy = 1
        sell = 0
        print('Buy action at ', date)
        print('RSI buy interval', buy_value, 'Current RSI value', rsi_value_buy)
        print(shares, ' shares bought at ', buy_price,)
        print('Total capital spent: ', bought)

    elif rsi_value_buy >= buy_value and prev_buy_value <= buy_value and buy == 0:
        #print('Buy Logic 2')
        print('Buy action at day', date)
        buy_price = close[i]
        shares = round(capital / buy_price) - 1
        bought = shares * buy_price
        buy = 1
        sell = 0
        print('RSI buy interval', buy_value, 'Current RSI value', rsi_value_buy)
        print(shares, ' shares bought at ', buy_price,)
        print('Total capital spent: ', bought)

    elif rsi_value_sell >= sell_value and sell == 0:
        sold_price = close[i]
        sold = shares * sold_price
        ret = (sold - bought)
        if ret >= 0:
            win = win + 1
        capital = ret + capital
        buy = 0
        sell = 1
        trade = trade + 1
        print('RSI sell interval', sell_value, 'Current RSI value', rsi_value_sell)
        print(shares, ' shares sold at ', sold_price,)
        print('Return: ', ret)
        print('Total capital left: ', capital)   
        print('Sell action at day', date)

first_price = close[0]
last_price = close[len(close) - 1]
bahshares = round(10000/first_price) - 1 
bahbought = bahshares * first_price
bahsold = bahshares * last_price
bahreturn = (bahsold - bahbought) + 10000

print('Total Capital after GA strategy: ', capital)
print('Win Percentage: ', (win/trade) * 100)
print('Total Capital after Buy and Hold strategy: ', bahreturn)

print(individual)




