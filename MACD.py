#Other types of prices can be used
#Fifty observances
closing_prices = [89, 88, 88, 87, 84, 83, 84, 86, 88, 89, 90, 90, 91, 87, 87, 88, 87, 88, 87, 80, 81, 80, 
            79, 78, 78, 77, 76, 74, 75, 75, 75, 74, 75, 74, 75, 76, 76, 75, 77, 76, 77, 77, 78, 78, 77, 80, 80, 81, 80, 81]

#26 and 12 day EMAs
def simple_moving_average(length, list):
    sum_of_prices = 0
    for i in range(length):
        sum_of_prices = list[i] + sum_of_prices 
    sma = sum_of_prices / length
    return sma

def exponential_moving_average(length, list, past_value):
    multiplier = 2 / (length + 1)
    interval = length
    ema_list = []
    for i in range (interval, len(list)):
        ema = list[i] * multiplier + past_value * (1 - multiplier) #SMA after first calculation becomes previous EMA value
        ema_list.append(ema)
    return ema_list
    #print(ema, closing_prices[interval], multiplier, sma, '\n')

#Used to start Exponential Moving Averages
sma_26days = simple_moving_average(26, closing_prices) #26 day simple moving average
sma_12days = simple_moving_average(12, closing_prices) #12 day simple moving average 

#Inital EMA established for calculations
ema_26days_list = []
ema_12days_list = []
ema_26days_list = exponential_moving_average(26, closing_prices, sma_26days)
ema_12days_list = exponential_moving_average(12, closing_prices, sma_12days)
#Take the first 14 values from 12 day averageto match with 26 day average
del ema_12days_list[:14] 
#print('\nSimple Moving Averages: (26 then 12)')
#print(sma_26days, sma_12days, '\n')
#print('Exponential Moving Averages: (26 then 12)')
#print(ema_26days, ema_12days, '\n')

MACD_list = []
print(26, '\t\t\t', 12, '\t\t\t', 'MACD')
for i in range(len(ema_26days_list)):
    MACD = ema_12days_list[i] - ema_26days_list[i]
    MACD_list.append(float(MACD))
    print(ema_26days_list[i], '\t', ema_12days_list[i], '\t', MACD_list[i])

#print(len(ema_26days_list), '\t', type(ema_26days_list), '\n')
#print(len(ema_12days_list), '\t', type(ema_12days_list), '\n')
#print(len(MACD_list), '\t', type(MACD_list), '\n')
print('\n')

signal_line_list = []
signal_line_sma = simple_moving_average(9, MACD_list)
signal_line_list = exponential_moving_average(9, MACD_list, signal_line_sma)

del ema_26days_list[:9]
del ema_12days_list[:9]
del MACD_list[:9]

#for i in range(len(signal_line_list)):
    #print(signal_line_list[i])
#print(len(signal_line_list))

Interval_list = []
print('\t', 26, '\t\t\t', 12, '\t\t\t', 'MACD', '\t\t\t', 'SigLine')
for i in range(len(ema_26days_list)):
    Interval_list.append(i+1)
    print(Interval_list[i], '\t', ema_26days_list[i], '\t', ema_12days_list[i], '\t', MACD_list[i], '\t', signal_line_list[i])
print('\n')

#print(len(ema_26days_list), '\t', type(ema_26days_list), '\n')
#print(len(ema_12days_list), '\t', type(ema_12days_list), '\n')
#print(len(MACD_list), '\t', type(MACD_list), '\n')
#print(len(signal_line_list), '\t', type(signal_line_list), '\n')

#Plot MACD and Signal Line to see swings in price levels

