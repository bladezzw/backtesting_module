from ts_mysql import * #获取包的全局参数
"""
#%% create database and tables
"""

def excute_sql(sql):
    conn = pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def create_tables_daily():
    sql = """CREATE TABLE daily (
id int NOT NULL AUTO_INCREMENT,
ts_code varchar(255) NOT NULL,
trade_date datetime NULL,
open decimal(19,4) NULL,
high decimal(19,4)NULL,
low decimal(19,4)NULL,
close decimal(19,4)NULL,
`change` decimal(19,4) NULL,
pre_close decimal(9,4)NULL,
pct_chg decimal(9,4)NULL,
vol decimal(19,4)NULL,
amount decimal(19,4)NULL,
create_date datetime NOT NULL,
PRIMARY KEY (`id`,`ts_code`)

) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8; """
    excute_sql(sql)

def create_talbes_Indexes():
    sql = """CREATE TABLE indexes (
    id int NOT NULL AUTO_INCREMENT,
    ts_code varchar(255) NOT NULL,
    name varchar(255) NULL,
    market varchar(255) NULL,
    publisher varchar(255) NULL,
    category varchar(255) NULL,
    base_date varchar(255) NULL,
    base_point decimal(16,2) NULL,
    list_date varchar(255) NULL,
    create_date datetime NOT NULL,
    PRIMARY KEY (id,ts_code)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8; """
    excute_sql(sql)

def create_tables_Index_daily():
    sql = """CREATE TABLE index_daily (
    id int NOT NULL AUTO_INCREMENT,
    ts_code varchar(255) NOT NULL,
    trade_date datetime NULL,
    open decimal(19,4) NULL,
    high decimal(19,4)NULL,
    low decimal(19,4)NULL,
    close decimal(19,4)NULL,
    pre_close decimal(9,4)NULL,
    pct_chg decimal(9,4)NULL,
    vol decimal(19,4)NULL,
    amount decimal(19,4)NULL,
    create_date datetime NOT NULL,
    PRIMARY KEY (`id`,`ts_code`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8; """
    excute_sql(sql)

def create_tables_symbol():
    sql = """CREATE TABLE symbol (
  id int NOT NULL AUTO_INCREMENT ,
  ts_code varchar(255) NOT NULL unique,
  name varchar(255) NULL,
  symbol varchar(255) NULL,
  industry varchar(255) NULL,
  area varchar(255) NULL,
  fullname varchar(255) NULL,
  enname varchar(255) NULL,
  market varchar(255) NULL,
  exchange varchar(255) NULL,
  curr_type varchar(255) NULL,
  list_status varchar(255) NULL,
  list_date varchar(255) NULL,
  delist_date varchar(255) NULL,
  create_date datetime NOT NULL,  

  PRIMARY KEY (`id`,`ts_code`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8; """
    excute_sql(sql)

if __name__ == '__main__':
    print("create_tables_module".center(20,'-'))
    try:
        create_tables_daily()#create table daily in mysql
    except Exception as ee:
        print('table daily Already exist')
    try:
        create_talbes_Indexes()
    except Exception as ee:
        print('table indexes Already exist')
    try:
        create_tables_Index_daily()
    except Exception as ee:
        print('table index_daily Already exist')
    try:
        create_tables_symbol()
    except Exception as ee:
        print('table symbol Already exist')