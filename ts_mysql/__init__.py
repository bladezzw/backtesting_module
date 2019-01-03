import time
import pymysql
import tushare as ts
import pandas as pd

now_ = time.strftime('%Y%m%d')

host="127.0.0.1"
port=3306
user='root'
passwd="318318"
db='stock_master'
token = ""
