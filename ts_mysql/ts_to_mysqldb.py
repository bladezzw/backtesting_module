import time
from ts_mysql import * #获取包的全局参数
from ts_mysql import tushare_api as ts_api
from ts_mysql import data_preparation as dp
from ts_mysql import mysql_api as ms_api
import threading
from  multiprocessing import Process,Pool


"""
该模块用来将tushare的数据插入mysql
"""
# from sqlalchemy import create_engine
# import tushare as ts
#
# df = ts.get_tick_data('600848', date='2014-12-22')
# engine = create_engine('mysql://user:passwd@127.0.0.1/db_name?charset=utf8')
#
# #存入数据库
# df.to_sql('tick_data',engine)
#
# #追加数据到现有表
# #df.to_sql('tick_data',engine,if_exists='append')



def mysql_insertsql(table_name = '',keys='',value=[]):
    """
    :param table_name: str
    :param keys: list
    :param value: list  在tushare中是df.iloc[i],row value of df. 
    :return:
    """
    sql = "insert into {tab_name}{keys} values {values};" \
        .format(tab_name=table_name, keys=keys, values=tuple(value))
    return sql

#%% insert data into mysql
def insert_df2mysql(df,table=''): 
    """
    :param df:DataFrame with columns'name
    :param table: str,table_name of your databases(default:'stock_market')
    This will be collected into a class (mysql_insert) in the future
    """
    conn = pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db)
    cursor = conn.cursor()

    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
#    if len(df) < 1e10:
#        df_date = dp.create_pd_Series(values=time.strftime('%Y%m%d'), length_=len(df), name='create_date')  # 日期列
#        df = pd.concat([df, df_date], axis=1)
#        col_name = list(df.columns)  # column titles of data
#        keys = str(tuple(col_name)).replace("'", '')
#        print(keys)
#        for i in range(len(df)):
#            # will be updated to a efficient way!
#            temp = list(df.iloc[i])
#            sql = mysql_insertsql(table, keys, value=temp)
#            # value may be None,
#            # print(sql)
#            cursor.execute(sql)
#            if i >10 :break

    # else:
    col_name = list(df.columns)  # column titles of data
    col_name.extend(['create_date'])  # add keys: 'create_date' ,'last_update_date'
    # table_name's formation like '(ts_code, symbol, name, area, industry, market, list_date)'
    date = time.strftime('%Y-%m-%d')
    keys = str(tuple(col_name)).replace("'", '')
    for i in range(len(df)):
         # will be updated to a efficient way!
         temp = list(df.iloc[i])
         temp.extend([date])
         sql = mysql_insertsql(table, keys, value=temp)
         cursor.execute(sql)
        # print(int(i*100/len(symbol)),'%')
    #    print('finish!')
    conn.commit()
    cursor.close()
    conn.close()

#def insert_alldaily2mysql1(symbols=[]):
#    """
#    This could use the threading method,will be modifed in the future.
#    but,may cause discontinuous daily
#    """
#    print('Start all !')
#    for i in range(len(symbols)):
#        try:
#            insert_df2mysql(ts_api.get_1stock_daily_dataInTushare(ts_code=symbols[i]),'daily')
#        except Exception as ee:
#            print(ee)
#            print('something wrong with stock: {}'.format(symbols[i]))
##        if i%200 == 199:
##            time.sleep(60)
#        print(i,'%d %'%(int(i*100/len(symbols))))
#    print('Finish all!')

def get_and_insert1data2mysql(ts_code='',start_date='20180101',end_date = now_,table = ''):
    """
    :param symbol: ts_code
    :param start_date:
    :param end_date:
    :param table: 插入的表
    :return:
    """
    try:
        if table == 'daily':
            df = ts_api.get_1stock_daily_dataInTushare(ts_code,start_date=start_date,end_date=now_)
        if table == 'index_daily':
            df = ts_api.get_1index_daily(ts_code, start_date=start_date, end_date=now_)
        insert_df2mysql(df, table=table)
    except Exception as ee:
        print(ee)

def insert_alldaily2mysql(symbols=[],start_date='20180101',end_date = now_,table = ''):
    """
    插入symbol对应的股票进入
    """
    if table:
        thre = []
        semaphore = threading.Semaphore(4)
        for i in range(len(symbols)):
            thre.append(threading.Thread(target=get_and_insert1data2mysql,args=(symbols.iloc[i],start_date,end_date,table,)))
        for t in thre:
            t.start()
            print('thread %s start!'%t)

def insert_alldaily2mysql_with_pool(symbol=[],start_date='19900101', now_=now_, table=''):
    """
    untested
    :param args: symbols symbols[i]
    :param kwargs: e.g. start_date = '19900101' ,now_ = 'time.strftime(%Y%m%d)' , table = 'daily'
    :return:
    """
    #symbols = ms_api.get_allSymbolInMysql()
    thre = []
    pool = Pool()
    for i in range(len(symbol)):
        pool.apply_async(func=get_and_insert1data2mysql, args=(symbol[i], start_date, now_, table,))

    pool.close()
    pool.join()         # join与close调用顺序是固定的
    print('end')

def delete_duplicate_data():
    delete from index_daily where id in (select id from (select min(id) id  from index_daily group by ts_code,trade_date having count(*)>1)id );
    pass

def update_daily():
    pass

def update_all_daily():
    pass

def update_1_index_daily(ts_code='',last_date='',table=''):
    """
    :param ts_code:  需要更新数据的股票
    :param last_date: 其在mysql中最后的日期
    :param table:  需要更新的表
    :return:
    """
    if not last_date:
        last_date = ms_api.get_last_date_of_ts_code(ts_code=ts_code, table=table)
    df = ts_api.get_1index_daily(ts_code=ts_code,start_date=last_date,end_date=now_)
    insert_df2mysql(df,table=table)
    pass

def update_all_index_daily():
    pass

if __name__ == '__main__':
    print("ts_mysql_module".center(20,'-'))
    ## get and insert Comprehensive Index of ShangHai into index_daily
    df = ts_api.get_1index_daily(ts_code='000001.SH',start_date='19900101',end_date=now_)
    insert_df2mysql(df, table='index_daily')
    ## update Comprehensive Index of ShangHai into index_daily
    update_1_index_daily(ts_code='000001.SH',table='index_daily')

    
    
    
    ##
    #
    # ddf = ts_api.get_symbolIntushare()
    # # print(ddf.iloc[:,1].iloc[0:16])
    # symbols = ddf.iloc[:, 1].iloc[0:16]
    # print(symbols)
    # print('start threading ')
    # insert_alldaily2mysql(symbols = symbols,table='daily')

    # #insert symbols into mysqldb's table'symbol'
#    try:
#        df = ts_api.get_symbolIntushare()
#        #2.insert into mysql
#        insert_df2mysql(df,'symbol')
#    except Exception as ee:
#        print('already have')
            
    #insert indexes into mysqldb's table'indexes'
#    try:
#        df_indexes = ts_api.get_index_allInTushare()
#        insert_df2mysql(df_indexes,table = 'indexes')
#    except Exception as ee:
#        print('already have')

    #insert_df2mysql(df,table='indexes')
    #get_and_insert1data2mysql(ts_code='399300.SZ', start_date='20180101', end_date=now_, table='index_daily')


    ##the line below is to insert a daily data of a certain stock
    # get_and_insert1data2mysql(symbol='000001.SZ',table='daily')


    ##多线程实现insert all daily of all stocks recorded in mysql
    # ddf = ms_api.get_allSymbolInMysql()
    # symbols = ddf[:10]
    #
    # thre = []
    #
    # semaphore = threading.Semaphore(16)
    # for i in range(len(symbols)):
    #     thre.append(
    #         threading.Thread(target=get_and_insert1data2mysql, args=(symbols[i],'19900101', now_, 'daily',)))
    # for t in thre:
    #     t.start()
    #     print('thread %s start!' % t)

    #多进程实现insert all daily of all stocks recorded in mysql
#    ddf = ms_api.get_allIndexesInMysql()
#    symbols = ddf[1000:1100]
#    thre = []
#    pool = Pool(16)
#    for i in range(len(symbols)):
#        pool.apply_async(func=get_and_insert1data2mysql, args=(symbols[i],'19900101', now_, 'index_daily',))
#        print(i*100/len(symbols),'%')
#    pool.close()
#    pool.join()         # join与close调用顺序是固定的
#
#    print('end')


    ##串行实现insert all daily of all stocks recorded in mysql
    # ddf = ms_api.get_allSymbolInMysql()
    # symbols = ddf[0:4]
    # insert_alldaily2mysql1(symbols)
