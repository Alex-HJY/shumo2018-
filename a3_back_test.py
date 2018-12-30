from copy import deepcopy

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from a1_getdata import get_data


dff = get_data()

START_MONEY = 1000000


def back_test(d=pd.DataFrame(), y_name='', start_year='2017', end_year='2018',ma1=5,ma2=10,ma3=5,ma4=15):
    money = 1000000
    share = 0
    df = deepcopy(d)
    df = df[start_year:end_year]
    df = df[[y_name, 'CLOSE']]

    df['bench'] = START_MONEY
    share = START_MONEY / df.iloc[29].loc['CLOSE']
    df[y_name + '_share'] = 0
    df[y_name + '_money'] = START_MONEY
    df[y_name + '_hold'] = False
    for i in range(30, len(df)):
        # print(i)
        df.ix[i,'bench'] = share * df.ix[i, 'CLOSE']
        if df[y_name][i - ma1 - 1:i - 1].mean() > df[y_name][i - ma2 - 1:i - 1].mean() and df[y_name][ i - ma1:i].mean()\
                < df[ y_name][ i - ma2:i].mean() and not \
                df[y_name + '_hold'].iloc[i - 1]:
            df.ix[i, y_name + '_hold'] = True
            df.ix[i, y_name + '_share'] = df.ix[i - 1, y_name + '_money'] / df.ix[i, 'CLOSE']
            df.ix[i, y_name + '_money'] = df.ix[i - 1, y_name + '_money']
            continue
        if df[y_name][i - ma3 - 1:i - 1].mean() < df[y_name][i - ma4 - 1:i - 1].mean() and df[y_name][i - ma3:i].mean()\
                > df[y_name][i - ma4:i].mean() and \
                df[y_name + '_hold'].iloc[i - 1]:
            df.ix[i, y_name + '_hold'] = False
            df.ix[i, y_name + '_money'] = df.ix[i - 1, y_name + '_share'] * df.ix[i, 'CLOSE']
            df.ix[i, y_name + '_share'] = 0
            continue

        df.ix[i, y_name + '_hold'] = df.ix[i-1, y_name + '_hold']
        if df.ix[i, y_name + '_hold']:
            df.ix[i, y_name + '_share'] = df.ix[i - 1, y_name + '_share']
            df.ix[i, y_name + '_money'] = df.ix[i, y_name + '_share'] * df.ix[i, 'CLOSE']
        else:
            df.ix[i, y_name + '_money'] = df.ix[i - 1, y_name + '_money']
            df.ix[i, y_name + '_share'] = df.ix[i - 1, y_name + '_share']

    dff = df[[y_name + '_share',y_name + '_money',y_name + '_hold']]
    # print(dff.head())

    plt.plot(df.index, df[y_name + '_money'], label=y_name)
    plt.plot(df.index, df['bench'], label='HS300', c='r')
    plt.legend()
    # plt.xticks(rotation=45)
    plt.show()

    return dff


if __name__ == '__main__':
    back_test(dff, 'VOLUME')
    back_test(dff, 'total_balance')
    back_test(dff, 'PE')

    dff.to_csv('test.csv', encoding='utf-8-sig')
