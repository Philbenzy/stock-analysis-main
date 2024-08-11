import akshare as ak
import mplfinance as mpf
import pandas as pd
# sh601899 sh180501 sz300059 sz000725
# 时间区间 + 复权类型

target = 'sh601918'
start = '20240201'
end = '20240804'
stock_zh_a_daily_qfq_df = ak.stock_zh_a_daily(symbol=target, start_date= start, end_date= end, adjust="qfq")
df = pd.DataFrame(stock_zh_a_daily_qfq_df)

df['date'] = pd.to_datetime(df['date'])
print(df)
print(df.dtypes)
df = df.set_index(["date"])
#df = df["20240101": "20240706"]
mpf.plot(df, type="candle", mav=(3, 6, 9),volume=True, title = target ,show_nontrading=False)