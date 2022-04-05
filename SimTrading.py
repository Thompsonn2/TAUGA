import pandas_datareader.data as pdr

def trade_function(data_frame, individual):
    #print('Trade Function')
    close = data_frame.Close
    sma50 = data_frame.SMA50
    sma200 = data_frame.SMA200
    traits = []
    buy = 0
    sell = 1
    ret = 0
    capital = 10000

    #print(individual)

    for i in range(0, len(close)):
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
            # print('RSI buy interval', buy_value, 'Current RSI value', rsi_value_buy)
            # print(shares, ' shares bought at ', buy_price,)
            # print('Total capital spent: ', bought)

        elif rsi_value_buy >= buy_value and prev_buy_value <= buy_value and buy == 0:
            #print('Buy Logic 2')
            buy_price = close[i]
            shares = round(capital / buy_price) - 1
            bought = shares * buy_price
            buy = 1
            sell = 0
            # print('RSI buy interval', buy_value, 'Current RSI value', rsi_value_buy)
            # print(shares, ' shares bought at ', buy_price,)
            # print('Total capital spent: ', bought)

        elif rsi_value_sell >= sell_value and sell == 0:
            sold_price = close[i]
            sold = shares * sold_price
            ret = (sold - bought)
            capital = ret + capital
            buy = 0
            sell = 1
            # print('RSI sell interval', sell_value, 'Current RSI value', rsi_value_sell)
            # print(shares, ' shares sold at ', sold_price,)
            # print('Return: ', ret)
            # print('Total capital left: ', capital)   

        if capital <= 0:
            return 0

    final_return = capital
    #print('Total return: ', final_return, ' Capital: ', capital)

    if final_return <= 0:
        #print(final_return)
        return 0
    else:
        return final_return
        
