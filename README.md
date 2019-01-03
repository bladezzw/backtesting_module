# myengine
According to a book on Quantopion, Successful Algorithmic Trading, I sorted out a little offline backtest engine to do the Chinese stock market backtest. Just for fun! 

# TODO: Connecting to CTP to test online.
# 1.Install mysql. 安装mysql
## Ubuntu: 
  using:
 -    `sudo apt-get install mysql-server mysql-common`
  configure your mysql-api on myengine.ts_mysql.__init__.py
# 2.Requirement(需要的python包):
-  `pip install pymysql`
-  `pip install tushare`
# 3.Sign up in tushare to get a token, setting it in myengine.ts_mysql.__init__.py
-  在tushare上注册一个账号，免费滴，获取token设置在myengine.ts_mysql.__init__.py里面  
# 4.Sun create_table.py in ts_mysql.建立表
 - `python create_table.py`
# 5.Download data.下载中国股票市场的日线数据
-  根据需要运行ts_tomysqldb.py
# 6.Backtesting.当数据库中存有数据的时候就能够进行回测。
-  runing backtest:
    `python run.py`  
# 7.When backtesting is done, a 'equity.csv' will created.
-  当运行完成后，会产生一个'equity.csv'的回测文件。
