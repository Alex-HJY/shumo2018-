# coding=utf-8
from copy import deepcopy
from datetime import datetime
from jqdata import macro
from jqdata import *
import matplotlib.pyplot as plt
from datetime import timedelta
import pandas as pd
from dateutil import parser
import numpy as np
import statsmodels.api as sm
from statsmodels import regression

df = pd.read_csv('./data/shouyi.csv', index_col='day')
df.index = pd.DatetimeIndex(df.index)
df = df['2009':'2016']


def calculate(name=''):
    # 年化收益率
    r = (df.ix[-1, name] * 1.0 / df.ix[0, name]) ** (250 * 1.0 / df.__len__()) - 1

    # 回撤
    d = 0
    t = df.ix[0, name]
    for i in range(1, df.__len__()):
        t = max(t, df.ix[i, name] * 1.0)
        d = max(d, 1 - df.ix[i, name] * 1.0 / t)
    # sharp
    rt = []
    for i in range(2009, 2017):
        rt.append((df[str(i)].ix[-1, name] - df[str(i)].ix[0, name]) * 1.0 / df[str(i)].ix[0, name] - 1)
    rt = np.array(rt)
    rt = rt * 100
    sigma = rt.std()
    sharp = (r - 0.028) * 100 / sigma

    # 胜率
    win = df[(df[name] - df[name].shift(-1)) > 0][name].count() * 1.0 / df.__len__()

    # beta alpha
    df[name + '_rtn'] = (df[name] - df[name].shift(-1)) / df[name] * 100
    df['hs300_rtn'] = (df['hs300_money'] - df['hs300_money'].shift(-1)) / df['hs300_money'] * 100
    beta = df[name + '_rtn'][:-1].cov(df['hs300_rtn'][:-1]) / df['hs300_rtn'][:-1].var()
    alpha = (r - 0.0284) - beta * (
            ((df.ix[-1, 'hs300_money'] * 1.0 / df.ix[0, 'hs300_money']) ** (250 * 1.0 / df.__len__
            ()) - 1) - 0.0284)

    print '策略收益=', str(((df.ix[-1, name] * 1.0 / df.ix[0, name])) * 100), '基准收益=', str(
        ((df.ix[-1, 'hs300_money'] * 1.0 / df.ix[0, 'hs300_money'])) * 100), \
        '策略收益率=' + str(r * 100) + '%', '回撤=' + str(d * 100) + '%', 'sharp=' + str(sharp), '上涨率=' + str(
        win), 'alpha=', alpha, 'beta=', beta


calculate('lundong_real_90_money')
