import numpy as np
import pandas as pd
import a1_getdata
import matplotlib.pyplot as plt


def print_pic(df=pd.DataFrame([]), x_name='CLOSE', y_name='VOLUME'):
    df=df[[x_name,y_name]]
    df=df.dropna()
    ax1 = plt.figure().add_subplot(111)
    ax2 = ax1.twinx()
    ax1.plot(df.index, df[x_name], label=x_name)
    ax1.legend(loc=2)
    for i in ax1.get_xticklabels():
        i.set_rotation(45)
    ax2.plot(df.index, df[y_name], label=y_name, c='r')
    ax2.legend()
    plt.show()
    df[y_name] = df[y_name].shift(3)
    pearson = df[[x_name, y_name]].corr()
    spearman = df[[x_name, y_name]].corr('spearman')
    return pearson.loc[x_name, y_name], spearman.loc[x_name, y_name]


if __name__ == '__main__':
    df = a1_getdata.get_data()
    pearson, spearman = print_pic(df['2015':], y_name='000188_Close')
    print(pearson, spearman)
