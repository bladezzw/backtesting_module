from ts_mysql import * #获取包的全局参数

from ts_mysql import data_transfer
# %% get data from mysql
import time


def select_sql(key='*',table='',where=''):    

    sql = """select {key} from {table} where {where} ; """.format(key = key, table = table, where = where)
    return sql

def get_allSymbolInMysql():
    """
    return a dict of symbols
    """
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    # 更改获取数据结果的数据类型,默认是元组,可以改为字典等:conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    row_ = cursor.execute("select ts_code from symbol")  # this can be a function
    all_ = cursor.fetchall()

    li = []
    [li.append(all_[i]['ts_code']) for i in range(len(all_))]
    cursor.close()
    conn.close()
    return li

def get_allIndexesInMysql():
    """
    return a dict of symbols
    """
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    # 更改获取数据结果的数据类型,默认是元组,可以改为字典等:conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    row_ = cursor.execute("select ts_code from indexes")  # this can be a function
    all_ = cursor.fetchall()

    li = []
    [li.append(all_[i]['ts_code']) for i in range(len(all_))]
    cursor.close()
    conn.close()
    return li


def get_1stockdailyInMysql(symbol='', start_date='19900101', end_date=now_):
    """symbol,str,eg:'000001.SZ';
       start_date,str,eg:'19910101'or'1991-01-01' ;
       end_date,str ,eg:format same as start_date
        """
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    # select * from daily where ts_code='000001.SZ' and trade_date>'2018-1-27' and trade_date<'2018-02-06'
    sql = select_sql( table = 'daily', 
                     where="""ts_code='{symbol_}'
                         and trade_date>'{start_}'
                         and trade_date<'{end_}'""".format(symbol_=symbol, start_=start_date, end_=end_date))
    row_ = cursor.execute(sql)  # this can be a function

    if row_:
        all_ = cursor.fetchall()

        data_T = pd.Series(all_[0])
        for i, j in enumerate(all_):
            if i > 0:
                data_temp = pd.Series(all_[i])
                data_T = pd.concat([data_T, data_temp], axis=1, join='outer')
        data = data_T.T

        # get the column names of data
        sql_1 = """ desc {table_name} """.format(table_name='daily')
        row_2 = cursor.execute(sql_1)  # this can be a function
        desc_ = cursor.fetchall()
        title = []
        [title.append(desc_[i][0]) for i in range(len(desc_))]
        data.rename(columns=pd.Series(title), inplace=True)  # add columns' name

    cursor.close()
    conn.close()
    return data

def get_1indexdailyInMysql(symbol='', start_date='19900101', end_date=now_):
    """symbol,str,eg:'000001.SZ';
       start_date,str,eg:'19910101'or'1991-01-01' ;
       end_date,str ,eg:format same as start_date
        """
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    # select * from daily where ts_code='000001.SZ' and trade_date>'2018-1-27' and trade_date<'2018-02-06'
    sql = select_sql( table = 'index_daily', 
                     where="""ts_code='{symbol_}'
                         and trade_date>'{start_}'
                         and trade_date<'{end_}'""".format(symbol_=symbol, start_=start_date, end_=end_date))
    row_ = cursor.execute(sql)  # this can be a function

    if row_:
        all_ = cursor.fetchall()

        data_T = pd.Series(all_[0])
        for i, j in enumerate(all_):
            if i > 0:
                data_temp = pd.Series(all_[i])
                data_T = pd.concat([data_T, data_temp], axis=1, join='outer')
        data = data_T.T

        # get the column names of data
        sql_1 = """ desc {table_name} """.format(table_name='daily')
        row_2 = cursor.execute(sql_1)  # this can be a function
        desc_ = cursor.fetchall()
        title = []
        [title.append(desc_[i][0]) for i in range(len(desc_))]
        data.rename(columns=pd.Series(title), inplace=True)  # add columns' name
    else:
        raise Exception
    
    cursor.close()
    conn.close()
    return data


def get_anystockdailyInMysql(symbols=[], start_date='19900101', end_date=now_):
    """
    !unfinish
    obtain several symbols' daily data.
    :symbols,list
    :
    """
    print('obtain data,please wait.')
    data_ = get_1stockdailyInMysql(symbol=symbols[0], start_date=start_date, end_date=end_date)

    for k in range(len(symbols)):
        if k > 0:
            data_temp = get_1stockdailyInMysql(symbol=symbols[k], start_date=start_date, end_date=end_date)
            if data_temp:
                data_ = pd.concat([data_, data_temp], axis=0, join='outer')
        print(int(k * 100 / len(symbols)), "% finish!")
    return data_

def get_last_date_of_ts_code(ts_code='',table=''):
    sql = select_sql(key='max(trade_date)', table=table, where = """ts_code = '{ts_code}'""".format(ts_code=ts_code))
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    # 更改获取数据结果的数据类型,默认是元组,可以改为字典等:conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    row_ = cursor.execute(sql)  # this can be a function
    all_ = cursor.fetchall()
    cursor.close()
    conn.close()
    date = all_[0]['max(trade_date)'].strftime("%Y%m%d")
    
    return date
    
if __name__ == '__main__':
    print("mysql_api module".center(20,'-'))

    # #the line below is to fetch daily data of a certain stock from mysql
#    df = get_1stockdailyInMysql(symbol=input(""""please input the ts_cose(e.g. '000001.SZ'): """))
#    print(df)
    
    # #the line below is to fetch index_daily data of a certain index from mysql
    try:
        df = get_1indexdailyInMysql(symbol=input(""""please input the ts_cose(e.g. '000001.SH'): """))
        print()
    except Exception as ee:
        print(ee)


    # #得到symbols from mysql
    # df = get_anystockdailyInMysql(symbols=input(""""please input the ts_cose: e.g. '000001.SH'"""))
    # print(df)

    # get the ts_code name eg:'000001.SZ','000002.SZ'...

    ##得到mysql中的股票列表
    # symbols = get_allSymbolInMysql()
    # print(symbols)

    ##得到存在数据库中某ts_code的最后一个日期
    # df = get_last_date_of_ts_code(ts_code=input(""""please input the ts_cose: e.g. '000001.SH'"""),table=input("""please input the table in tushare: e.g. 'index_daily'"""))
    # print(df)


    #将数据输出为CSV文件
    data_transfer.df2csv(df,input("""please input the datapath_name(e.g. '~/xxx.csv'):"""))