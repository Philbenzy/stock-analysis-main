from typing import Dict
import akshare as ak
import pandas as pd
from decimal import Decimal, getcontext
import numpy as np
import datetime
import matplotlib.pyplot as plt
from dateutil.rrule import rrule, DAILY
import matplotlib.text as text

def calculate_total_stock_volumn(start_date: datetime.datetime, end_date: datetime.datetime, X:int) -> Dict[str, float]:
    """
    计算给定日期范围内A股成交额，并返回成交额字典。

    Args:
    start_date: 开始日期
    end_date: 结束日期
    X: 前X家公司

    Returns:
    Dict[str, float]: 包含日期和成交额的字典
    """
    X = X
    rpt_dates = [dt.strftime('%Y%m%d') for dt in rrule(DAILY, dtstart=start_date, until=end_date) if dt.weekday() < 5]
    total_stock_volumn_dict = {}

    for rpt_date in rpt_dates:
        try:
            getcontext().prec = 4
            stock_zh_a_spot_em = ak.stock_zh_a_spot_em()
            df = pd.DataFrame(stock_zh_a_spot_em)
            df = df.sort_values(by="成交额", ascending=False)
            top_X = df.head(X)
            top_X_volumn = Decimal(top_X['成交额'].sum() / 100000000)

            stock_sse_deal_daily_df = ak.stock_sse_deal_daily(date=rpt_date)
            df_summary_sh = pd.DataFrame(stock_sse_deal_daily_df)
            total_stock_volumn_sh = df_summary_sh.loc[df_summary_sh['单日情况'] == '成交金额', '股票'].values

            df_summary_sz = ak.stock_szse_summary(date=rpt_date)
            df_summary_sz = pd.DataFrame(df_summary_sz)
            total_stock_volumn_sz = np.around(df_summary_sz.loc[df_summary_sz['证券类别'] == '股票', '成交金额'].values / 100000000, 2)

            total_stock_volumn = total_stock_volumn_sh + total_stock_volumn_sz
            top_X_percentage = float(top_X_volumn) / total_stock_volumn[0]

            top_X.to_csv(f'/Users/zyw/stock-price/csv/top_{X}_volumn_companies_{rpt_date}.csv', index=False)

            total_stock_volumn_dict[rpt_date] = round(float(total_stock_volumn[0]), 2)
            print(f"{rpt_date}，A股成交总额: {total_stock_volumn} 亿元\n"
              f"上海交易所，股票总成交额: {total_stock_volumn_sh} 亿元\n"
              f"深圳交易所，股票总成交额: {total_stock_volumn_sz} 亿元\n"
              f"前{X}家公司总成交额: {int(top_X_volumn)} 亿元\n"
              f"今日成交额top{X}公司占A股总成交额 : {top_X_percentage * 100}%")
        except Exception as e:
            print(f"Error occurred on date: {rpt_date}")
            continue

    return total_stock_volumn_dict

from typing import Dict

def plot_stock_volumn(total_stock_volumn_dict: Dict[str, float]):
    """
    Plot the A股成交总额 for the first half of 2024.

    Args:
    total_stock_volumn_dict (Dict[str, float]): A dictionary containing dates as keys and corresponding total stock volumes as values.

    Returns:
    None
    """
    dates = [date[4:] for date in total_stock_volumn_dict.keys()]
    print(dates)
    volumns = list(total_stock_volumn_dict.values())
    print(volumns)

    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    plt.figure(figsize=(10, 6))
    plt.bar(dates, volumns, color='tab:blue', alpha=0.8)
    plt.title(f'「{dates[0]}-{dates[-1]}」A股成交总额', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('总成交额 (亿元)', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='-.')

    watermark = text.Text(x=2, y=0, text='王月0', color='gray', alpha=0.5, fontsize=50, rotation=20)
    plt.gca().add_artist(watermark)
    for i, v in enumerate(volumns):
        plt.text(i, v, str(v), ha='center', va='bottom', fontsize=8)

    plt.savefig(f'A_volumns_{dates[0]}_{dates[-1]}.png', dpi=300)
    plt.show()

# 调用
start_date = datetime.datetime(2024, 7, 1)
end_date = datetime.datetime(2024, 8, 8)
X = 50
total_stock_volumn_dict = calculate_total_stock_volumn(start_date, end_date,X)
plot_stock_volumn(total_stock_volumn_dict)

123