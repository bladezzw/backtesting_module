from ts_mysql import *
from ts_mysql import data_preparation as dp #数据预处理
import pandas as pd
#tushare上下载的数据为pandas.DataFrame格式

pro = ts.pro_api()

#该模块用来获取tushare的数据

def initial_token(token):
    """set your token"""
    ts.set_token(token)

initial_token()
#%% get data from tushare
def get_symbolIntushare():
    """从tushare上得到基本股票列表及信息"""
    code = pro.stock_basic()
    return dp.none2str_0(code)

def get_index_of_certain_market(market=''):
    """
    obtain the Index of certain market
    市场代码 	说明
    MSCI 	MSCI指数
    CSI 	中证指数
    SSE 	上交所指数
    SZSE 	深交所指数
    CICC 	中金所指数
    SW 	申万指数
    CNI 	国证指数
    OTH 	其他指数
    """
    df = pro.index_basic(market = market)
    return dp.none2str_0(df)

def get_index_allInTushare():
    market_list = ['MSCI','CSI','SSE','SZSE','CICC']
    df = get_index_of_certain_market('OTH')
    for mk in market_list:
        data_temp = get_index_of_certain_market(mk)
        df = pd.concat([df, data_temp], axis=0, join='outer')
#        try:
#            del df['list_date']
#        except Exception as ee:
#            print(ee)
    return dp.none2str_0(df)

def get_1stock_daily_data(ts_code='',start_date='19900101',end_date=now_):
    """
    :param ts_code:str
    :param trade_date\end_date:str yyyymmdd
    """
#    if not end_date:
#        end_date = time.strftime('%Y%m%d')
#    if not start_date:
#        start_date='19990101'
    df = pro.daily(ts_code=ts_code,start_date=start_date,end_date=end_date)
    d = df.drop(['change'],axis=1)#change is mysql key word,cant use
    return d

def get_1index_daily(ts_code='',start_date='19900101',end_date=now_):
    """
    """
    df = pro.index_daily(ts_code=ts_code,start_date=start_date,end_date=end_date)
    d = df.drop(['change'],axis=1)#change is mysql key word,cant use
   
    return dp.none2str_0(d)


def get_1stock_daily_dataInTushare(ts_code='',start_date='19900101',end_date=now_):
    """
    :param ts_code:str
    :param trade_date\end_date:str yyyymmdd
    """
#    if not end_date:
#        end_date = time.strftime('%Y%m%d')
#    if not start_date:
#        start_date='19990101'
    df = pro.daily(ts_code=ts_code,start_date=start_date,end_date=end_date)
    d = df.drop(['change'],axis=1)
    return d

if __name__ == '__main__':
    print("tushare_api module".center(20,'-'))
    #initial_token()  # inidal token to get access

    #get daily data of '000001.SZ' from '20180101' to '20181126'
    # df = get_1stock_daily_data(ts_code='000001.SZ',start_date='20180101',end_date='20181126')
    # print(df)

    #get all indexes in tushare
    #df = get_index_allInTushare()
    
    #get_1 index daily data
    df = get_1index_daily(ts_code='399300.SZ')
    print(df)

