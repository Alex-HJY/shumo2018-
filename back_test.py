from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
from dateutil import parser
from datetime import datetime


class back_test_system:
    def __init__(self, close_df=pd.DataFrame(), bench_mark='', start_money=1000000, save_dir=''):
        """

        :param close_df: 收盘价数据
        :param bench_mark: 基准收益标的名称
        :param start_money: 起始现金
        :param save_dir: 储存目录
        """
        self.close_df = deepcopy(close_df)
        self.bench_mark = bench_mark
        self.start_money = start_money
        self.save_dir = save_dir
        self.result = pd.DataFrame()

    def calc_bench(self, start_date='', end_date=''):
        """
        计算基本收益率
        :param start_date: 起始日期 datetime
        :param end_date: 结束日期 datetime
        :return: DataFrame, columns = [cash,money,portfolio]
        """
        close_df = self.close_df
        df = pd.DataFrame()
        one_day = timedelta(days=1)
        date_now = start_date
        while date_now < end_date:
            if date_now not in close_df.index:
                date_now = date_now + one_day
            else:
                break

        share = self.start_money / close_df.loc[date_now, self.bench_mark]

        while date_now < end_date:
            if date_now in close_df.index:
                df = df.append(
                    pd.DataFrame(
                        data=[
                            [share * close_df.loc[date_now, self.bench_mark], {self.bench_mark: share}, 0]],
                        index=[date_now],
                        columns=[self.bench_mark + '_money', self.bench_mark + '_portfolio',
                                 self.bench_mark + '_cash']))
            date_now = date_now + one_day

        return df

    def back_test_by_day(self, strategy_name='', trade_func='', start_date='', end_date=''):
        """

        :param strategy_name: 策略名称
        :param trade_func: 交易函数，函数参数为close_data, today,  money, cash, portfolio
        :param start_date: 起始日期
        :param end_date: 结束日期
        :return: df 包含策略的 CASH,MONEY,PORTFOLIO
        """

        # 设定初始参数
        close_data = self.close_df
        money = self.start_money
        cash = self.start_money
        portfolio = {}
        df_to_today = pd.DataFrame()
        result = self.result
        one_day = timedelta(days=1)
        start_date = parser.parse(start_date)
        end_date = parser.parse(end_date)
        today = start_date
        bench_mark = self.bench_mark

        result[strategy_name + '_money'] = ''
        result[strategy_name + '_cash'] = ''
        result[strategy_name + '_portfolio'] = ''
        # 按天回测df
        while today < end_date:
            if today in close_data.index:
                df_to_today = df_to_today.append(close_data.loc[today])
                money, cash, portfolio = trade_func(df_to_today, today, money, cash, portfolio)
                result.loc[today, strategy_name + '_money'] = money
                result.loc[today, strategy_name + '_cash'] = cash
                result.loc[today, strategy_name + '_portfolio'] = portfolio.__str__()
            today = today + one_day

        if bench_mark != '' and (bench_mark+'_money') not in result.columns:
            bench_profit = self.calc_bench(start_date, end_date)
            result = result.join(bench_profit)
            # print(bench_profit)
        # 计算基准收益并整合

        # 输出文件
        # result.to_csv(self.save_dir + strategy_name + '.csv', encoding='utf-8-sig')
        self.result = result
        return result

    def show(self, df, strategies_name=[]):
        """
        :param df:
        :param strategies_name:
        :return:
        """
        for strategy in strategies_name:
            plt.plot(df.index, df[strategy + '_money'], label=strategy)
        plt.plot(df.index, df[self.bench_mark + '_money'], label=self.bench_mark)
        plt.legend()
        plt.show()
        return None

    def get_indexes(self,df, strategies_name=[]):
        indexes = pd.DataFrame()
        for name in strategies_name:
            # 年化收益率
            r = (df.iloc[-1][name] * 1.0 / df.iloc[0][name]) ** (250 * 1.0 / df[name].__len__()) - 1

            # 回撤
            d = 0
            t = df.iloc[0][name]
            for i in range(1, df[name].__len__()):
                t = max(t, df.iloc[i][name] * 1.0)
                d = max(d, 1 - df.iloc[i][name] * 1.0 / t)
            # sharp
            rt = []
            for i in range(df.index[0].year, df.index[-1].year):
                rt.append((df[str(i)].ix[-1, name] - df[str(i)].ix[0, name]) * 1.0 / df[str(i)].ix[0, name] - 1)
            rt = np.array(rt)
            rt = rt * 100
            sigma = rt.std()
            sharp = (r - 0.028) * 100 / sigma

            # 胜率
            win = df[(df[name] - df[name].shift(-1)) > 0][name].count() * 1.0 / df.__len__()

            # beta alpha
            df[name + '_rtn'] = (df[name] - df[name].shift(-1)) / df[name] * 100

            df[self.bench_mark + '_rtn'] = (df[self.bench_mark + '_money'] - df[self.bench_mark + '_money'].shift(-1)) / \
                                           df[self.bench_mark + '_money'] * 100
            df[name + '_rtn'] = df[name + '_rtn'].map(float)
            df[self.bench_mark + '_rtn']=df[self.bench_mark + '_rtn'].map(float)
            beta = df[name + '_rtn'][:-1].cov(df[self.bench_mark + '_rtn'][:-1]) / df[self.bench_mark + '_rtn'][:-1].var()
            alpha = (r - 0.0284) - beta * (
                    ((df.iloc[-1][self.bench_mark + '_money'] * 1.0 / df.iloc[0][self.bench_mark + '_money']) ** (
                            250 * 1.0 / df.__len__()) - 1) - 0.0284)

            index = {'策略收益': [str(((df.iloc[-1][name] * 1.0 / df.iloc[0][name])) * 100)],
                     '基准收益': [str(((df.iloc[-1][self.bench_mark + '_money'] * 1.0 / df.iloc[0][
                         self.bench_mark + '_money'])) * 100)],

                     '策略收益率': [str(r * 100) + '%'],
                     '回撤': [str(d * 100) + '%'],
                     'sharp': [str(sharp)],
                     '上涨率': [str(win)],
                     'alpha': [alpha],
                     'beta': [beta]}
            index = pd.DataFrame(index)
        indexes = indexes.append(index)
        return indexes
