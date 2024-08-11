import akshare as ak
import pandas as pd
import datetime

df_all = pd.DataFrame()
list_symbol = ["创月新低", "半年新低", "一年新低", "历史新低"]
df_all = pd.DataFrame()
for symbol in list_symbol:
    stock_rank_cxd_ths = ak.stock_rank_cxd_ths(symbol=symbol)
    df = pd.DataFrame(stock_rank_cxd_ths)
    df.insert(0, '新高类别', symbol)
    df.insert(1,"当前数据日期", datetime.datetime.now().strftime("%Y-%m-%d"))
    df_all = pd.concat([df_all, df], ignore_index=False)


print(df_all)
df_all.to_excel('新低数据.xlsx', index=False)

# test
