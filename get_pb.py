import  tushare as ts
from dateutil import  parser
from datetime import datetime
from datetime import timedelta
import pandas as pd
from WindPy import *
w.start()

d=pd.DataFrame([])

for i in range(2005,2019):
    df=w.wses("1000000090000000", "sec_pb_overall_chn", str(i)+"-01-01", str(i)+"-12-31", "ruleType=2;excludeRule=1",usedf=True)
    d=d.append(df[1])

print(d.__len__())
d.to_csv('pb.csv',encoding='utf-8-sig')
w.close()


