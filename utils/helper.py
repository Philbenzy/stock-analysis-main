from dateutil.rrule import rrule, DAILY
import akshare as ak
import pandas as pd
import os


    
def get_stock_dict():
    stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    stock_zh_a_spot_em_df = pd.DataFrame(stock_zh_a_spot_em_df)
    stock_dict = dict(zip(stock_zh_a_spot_em_df['代码'].tolist(), stock_zh_a_spot_em_df['名称'].tolist()))
    return stock_dict

def day2csv(source_dir, file_name, target_dir):
    """
    将通达信的日线文件转换成CSV格式保存函数。通达信数据文件32字节为一组
    :param source_dir: str 源文件路径
    :param file_name: str 文件名
    :param target_dir: str 要保存的路径
    :return: none
    """
    from struct import unpack
    from decimal import Decimal  # 用于浮点数四舍五入

    # 以二进制方式打开源文件
    source_path = source_dir + os.sep + file_name  # 源文件包含文件名的路径
    source_file = open(source_path, 'rb')
    buf = source_file.read()  # 读取源文件保存在变量中
    source_file.close()
    source_size = os.path.getsize(source_path)  # 获取源文件大小
    source_row_number = int(source_size / 32)
    # user_debug('源文件行数', source_row_number)

    # 打开目标文件，后缀名为CSV
    target_path = target_dir + os.sep + file_name[2:-4] + '.csv'  # 目标文件包含文件名的路径
    # user_debug('target_path', target_path)

    if not os.path.isfile(target_path):
        # 目标文件不存在。写入表头行。begin从0开始转换
        target_file = open(target_path, 'w', encoding="utf-8")  # 以覆盖写模式打开文件
        header = str('date') + ',' + str('code') + ',' + str('open') + ',' + str('high') + ',' + str('low') + ',' \
                 + str('close') + ',' + str('vol') + ',' + str('amount')
        target_file.write(header)
        begin = 0
        end = begin + 32
        row_number = 0
    else:
        # 不为0，文件有内容。行附加。
        # 通达信数据32字节为一组，因此通达信文件大小除以32可算出通达信文件有多少行（也就是多少天）的数据。
        # 再用readlines计算出目标文件已有多少行（目标文件多了首行标题行），(行数-1)*32 即begin要开始的字节位置

        target_file = open(target_path, 'a+', encoding="gbk")  # 以追加读写模式打开文件
        # target_size = os.path.getsize(target_path)  #获取目标文件大小

        # 由于追加读写模式载入文件后指针在文件的结尾，需要先把指针改到文件开头，读取文件行数。
        # user_debug('当前指针', target_file.tell())
        target_file.seek(0, 0)  # 文件指针移到文件头
        # user_debug('移动指针到开头', target_file.seek(0, 0))
        target_file_content = target_file.readlines()  # 逐行读取文件内容
        row_number = len(target_file_content)  # 获得文件行数
        # user_debug('目标文件行数', row_number)
        # user_debug('目标文件最后一行的数据', target_file_content[-1])
        target_file.seek(0, 2)  # 文件指针移到文件尾
        # user_debug('移动指针到末尾', target_file.seek(0, 2))
        # if row_number > source_row_number:
        #     user_debug('已是最新数据，跳过for循环')
        # else:
        #     user_debug('追加模式，从' + str(row_number + 1) + '行开始')

        if row_number == 0:  # 如果文件出错是0的特殊情况
            begin = 0
        else:
            row_number = row_number - 1  # 由于pandas的dataFrame格式索引从0开始，为下面for循环需要减1
            begin = row_number * 32

        end = begin + 32

    for i in range(row_number, source_row_number):
        # 由于pandas的dataFrame格式首行为标题行，第二行的索引从0开始，
        # 因此转换出来显示的行数比原本少一行，但实际数据一致
        #
        # 将字节流转换成Python数据格式
        # I: unsigned int
        # f: float
        # a[5]浮点类型的成交金额，使用decimal类四舍五入为整数
        a = unpack('IIIIIfII', buf[begin:end])
        # '\n' + str(i) + ','
        # a[0]  将’19910404'样式的字符串转为'1991-05-05'格式的字符串。为了统一日期格式
        a_date = str(a[0])[0:4] + '-' + str(a[0])[4:6] + '-' + str(a[0])[6:8]
        file_name[2:-4]
        line = '\n' + str(a_date) + ',' \
               + file_name[2:-4] + ',' \
               + str(a[1] / 100.0) + ',' \
               + str(a[2] / 100.0) + ',' \
               + str(a[3] / 100.0) + ',' \
               + str(a[4] / 100.0) + ',' \
               + str(a[6]) + ',' \
               + str(Decimal(a[5]).quantize(Decimal("1."), rounding="ROUND_HALF_UP"))
        target_file.write(line)
        begin += 32
        end += 32
    target_file.close()

