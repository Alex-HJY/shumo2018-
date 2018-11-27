import pandas as pd


def get_data():
    df = pd.read_csv('./data/datautf8.csv', encoding='utf-8-sig')
    df.set_index('DateTime',drop=True,inplace=True)
    df2 = pd.read_csv('./data/pb.csv', encoding='utf-8-sig')
    df2.set_index('DateTime', inplace=True)
    df3 = pd.read_csv('./data/rzrq.csv', encoding='utf-8-sig')
    df3.set_index('DateTime', inplace=True)
    del df['id']
    df=df.join(df2)
    df3.index = pd.DatetimeIndex(df3.index)
    df.index=pd.DatetimeIndex(df.index)
    df = df.join(df3)
    df4 = pd.read_csv('./data/bozhi.csv', encoding='utf-8-sig')
    df4.set_index('DateTime', inplace=True)
    df4.index = pd.DatetimeIndex(df4.index)
    df = df.join(df4)
    df=df.sort_index()
    df.to_csv('data_total.csv',encoding='utf-8-sig')
    return df


if __name__ == '__main__':
    print(get_data().head())
    print(get_data().tail())
