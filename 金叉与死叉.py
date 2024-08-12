import pandas as pd
from  utils.MyTT import *
from utils.helper import get_stock_dict
import os
import pandas as pd


# 存放csv
folder_path = '/Users/zyw/Desktop/datatdx/lday_qfq'

day_file_list = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
stock_code = []
stock_dict = get_stock_dict()
golden_x = []

for day in day_file_list:
    code = str(day).replace('.csv', '')
    stock_code.append(code)

for csv in day_file_list:
    df = pd.read_csv(f'/Users/zyw/Desktop/lday_qfq/{csv}')
    
    CLOSE=df.close.values;  OPEN=df.open.values;   HIGH=df.high.values;   LOW=df.low.values   #基础数据定义
    MA5=MA(CLOSE,5)
    MA10=MA(CLOSE,10)
    CROSS_TODAY=RET(CROSS(MA5,MA10))
    CHANGE = (MA5[-1] - MA10[-1]) / MA10[-1]
    code = str(csv).replace('.csv', '').replace('sh', '')
    if  CHANGE > 0.005 and CROSS_TODAY:
        print(f'发现金叉: {stock_dict[code]}\t| {code}\t| 5日均线{round(MA5[-1],2)}\t| 10日均线 {round(MA10[-1],)}\t| 涨幅: {round(CHANGE*100, 2)}%')
        golden_x.append(code)
print(f'查找完毕：{len(golden_x)}个')
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - -')
die_x = []
for csv in day_file_list:
    df = pd.read_csv(f'/Users/zyw/Desktop/datatdx/lday_qfq/{csv}',encoding='GBK')
    CLOSE=df.close.values;  OPEN=df.open.values;   HIGH=df.high.values;   LOW=df.low.values   #基础数据定义
    MA5=MA(CLOSE,5)
    MA10=MA(CLOSE,10)
    CROSS_TODAY=RET(CROSS(MA10,MA5))
    CHANGE = (MA10[-1] - MA5[-1]) / MA5[-1]
    code = str(csv).replace('.csv', '').replace('sh', '')
    if  CHANGE > 0.005 and CROSS_TODAY:
        print(f'发现死叉: {stock_dict[code]}\t| {code}\t| 5日均线{round(MA5[-1],2)}\t| 10日均线 {round(MA10[-1],)}\t| 涨幅: {round(CHANGE*100, 2)}%')
        die_x.append(code)
print(f'查找完毕：{len(die_x)}个')
