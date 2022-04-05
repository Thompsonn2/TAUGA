import pandas_datareader.data as pdr

def generate(data_frame):
    #Difference between current and previous data frames
    
    close = data_frame.Close
    
    delta = close.diff()

    #Current is more than the previous value
    up = delta.clip(lower = 0)

    #Current is less than the previous value
    down = -1 * delta.clip(upper = 0)

    for i in range(5, 21):
        #Calculate EMAs of up and down differences
        ema_up = up.ewm(com = i - 1, adjust = False).mean()
        ema_down = down.ewm(com = i - 1, adjust = False).mean()

        #Calculate Relative Strength and RSI
        rs = ema_up/ema_down
        rsi = 'RSI' + str(i)
        data_frame[rsi] = 100 - (100/(1 + rs))
    
    return data_frame 

