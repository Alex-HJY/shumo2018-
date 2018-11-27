from copy import deepcopy

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from a1_getdata import get_data


ma1=5
ma2=30

dff = get_data()

START_MONEY=1000000
def back_test(d=pd.DataFrame(), y_name='', start_year='2011', end_year='2018'):
    money = 1000000
    share = 0
    df=deepcopy(d)
    df=df[start_year:end_year]
    df=df[[y_name,'CLOSE']]
    df=df.dropna()
    df['bench']=START_MONEY
    share=START_MONEY/df.iloc[49].loc['CLOSE']
    df[y_name + '_share'] = 0
    df[y_name + '_money'] = START_MONEY
    df[y_name+'_hold'] = False
    df = df.dropna()
    for i in range(50,len(df)):
        # print(i)
        df['bench'].iloc[i]=share*df.iloc[i].loc['CLOSE']
        if df[y_name][i-ma1-1:i-1].mean() < df[y_name][i-ma2-1:i-1].mean() and df[y_name][i-ma1:i].mean() > df[y_name][i-ma2:i].mean() and not df[y_name+'_hold'].iloc[i-1]:
            df[y_name+'_hold'].iloc[i] = True
            df[y_name + '_share'].iloc[i] = df[y_name + '_money'].iloc[i - 1] / df['CLOSE'].iloc[i]
            df[y_name + '_money'].iloc[i] = df[y_name + '_money'].iloc[i - 1]
            continue
        if df[y_name][i-ma1-1:i-1].mean() > df[y_name][i-ma2-1:i-1].mean() and df[y_name][i-ma1:i].mean() < df[y_name][i-ma2:i].mean() and df[y_name+'_hold'].iloc[i-1]:
            df[y_name+'_hold'].iloc[i] = False
            df[y_name + '_money'].iloc[i] = df[y_name + '_share'].iloc[i - 1] * df['CLOSE'].iloc[i]
            df[y_name + '_share'].iloc[i] = 0
            continue

        df[y_name+'_hold'].iloc[i] = df[y_name+'_hold'].iloc[i - 1]
        if df[y_name+'_hold'].iloc[i]:
            df[y_name + '_share'].iloc[i] = df[y_name + '_share'].iloc[i - 1]
            df[y_name + '_money'].iloc[i] = df[y_name + '_share'].iloc[i] * df['CLOSE'].iloc[i]
        else:
            df[y_name + '_money'].iloc[i] = df[y_name + '_money'].iloc[i - 1]
            df[y_name + '_share'].iloc[i] = df[y_name + '_share'].iloc[i - 1]

    global dff
    dff = dff.join(df[y_name + '_share'],)
    dff = dff.join(df[y_name + '_money'])
    dff = dff.join(df[y_name + '_hold'])
    print(dff.head())

    plt.plot(df.index, df[y_name+'_money'], label=y_name)
    plt.plot(df.index, df['bench'], label='HS300', c='r')
    plt.legend()
    # plt.xticks(rotation=45)
    plt.show()



if __name__ == '__main__':
    back_test(dff, '000188_Close')
    # back_test(dff, 'VOLUME')
    # back_test(dff, 'total_balance')
    # back_test(dff, 'PE')
    # back_test(dff, 'PB')
    dff.to_csv('test.csv',encoding='utf-8-sig')
