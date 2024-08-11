import akshare as ak
import pandas as pd
import datetime

df_all = pd.DataFrame()
list_symbol = ["创月新高", "半年新高", "一年新高", "历史新高"]
df_all = pd.DataFrame()
for symbol in list_symbol:
    stock_rank_cxg_ths_df = ak.stock_rank_cxg_ths(symbol=symbol)
    df = pd.DataFrame(stock_rank_cxg_ths_df)
    df.insert(0, '新高类别', symbol)
    df.insert(1,"当前数据日期", datetime.datetime.now().strftime("%Y-%m-%d"))
    df_all = pd.concat([df_all, df], ignore_index=False)


print(df_all)
df_all.to_excel('创新高.xlsx', index=False)

## 测试

