import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./data/test.csv', encoding='utf-8-sig',index_col='DateTime')
df.index=pd.DatetimeIndex(df.index)

def rate_day(df=pd.DataFrame(), x_name='PB_money'):

    d = (df[x_name] - df[x_name].shift(1)) / df[x_name].shift(1)
    b = (df['CLOSE'] - df['CLOSE'].shift(1)) / df['CLOSE'].shift(1)
    plt.plot(d.index, d.values,'b')
    # plt.plot(b.index, b.values, 'r')
    plt.show()


rate_day(df)
