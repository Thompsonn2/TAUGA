import pandas_datareader.data as pdr

def trade_function(data_frame, individual):
    close = data_frame.Close
    sma50 = data_frame.SMA50
    sma200 = data_frame.SMA200
    traits = []
    buy = 0
    sell = 1
    ret = 0
    capital = 10000

    for i in range(0, len(close)):
        if sma50[i] > sma200[i]: #Uptrend
            traits = individual[4:8]
        elif sma200[i] > sma50[i]: #Downtrend
            traits = individual[0:4]
        
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

        #Buy and sell actions
        if rsi_value_buy == buy_value and buy == 0:
            buy_price = close[i]
            shares = round(capital / buy_price) - 1
            bought = shares * buy_price
            buy = 1
            sell = 0

        elif rsi_value_buy >= buy_value and prev_buy_value <= buy_value and buy == 0:
            buy_price = close[i]
            shares = round(capital / buy_price) - 1
            bought = shares * buy_price
            buy = 1
            sell = 0

        elif rsi_value_sell >= sell_value and sell == 0:
            sold_price = close[i]
            sold = shares * sold_price
            ret = (sold - bought)
            capital = ret + capital
            buy = 0
            sell = 1

        #Strategy losses all capital
        if capital <= 0:
            return 0

    final_return = capital

    if final_return <= 0:
        return 0
    else:
        return final_return
        
