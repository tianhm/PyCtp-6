# import os
# os.chdir('Z:\williamyizhu On My Mac\Documents\workspace\PyCtp')
# os.getcwd()

from configparser import SafeConfigParser
config = SafeConfigParser()

# ------------------- simulation account -------------------
config.add_section('sim1')
config.set('sim1', 'BrokerID', '9999')
config.set('sim1', 'UserID', '031237')
config.set('sim1', 'Password', '12345678')
config.set('sim1', 'q_ip', 'tcp://218.202.237.33:10012')
config.set('sim1', 't_ip', 'tcp://218.202.237.33:10002')

config.add_section('sim2')
config.set('sim2', 'BrokerID', '9999')
config.set('sim2', 'UserID', '037589')
config.set('sim2', 'Password', '12345678')
config.set('sim2', 'q_ip', 'tcp://218.202.237.33:10012')
config.set('sim2', 't_ip', 'tcp://218.202.237.33:10002')

config.add_section('sim3')
config.set('sim3', 'BrokerID', '9999')
config.set('sim3', 'UserID', '062805')
config.set('sim3', 'Password', '12345678')
config.set('sim3', 'q_ip', 'tcp://218.202.237.33:10012')
config.set('sim3', 't_ip', 'tcp://218.202.237.33:10002')

config.add_section('sim_ht')
config.set('sim_ht', 'BrokerID', '8000')
config.set('sim_ht', 'UserID', '41003276')
config.set('sim_ht', 'Password', '260519')
config.set('sim_ht', 'q_ip', 'tcp://180.168.212.79:31213')
config.set('sim_ht', 't_ip', 'tcp://180.168.212.79:31205')

# ------------------- real account, real_xx2 is after market close inquiry -------------------
config.add_section('real_eb1')
config.set('real_eb1', 'BrokerID', '6000')
config.set('real_eb1', 'UserID', '01301321')
config.set('real_eb1', 'Password', '123456')
config.set('real_eb1', 'q_ip', 'tcp://101.231.162.58:41213')
config.set('real_eb1', 't_ip', 'tcp://101.231.162.58:41205')

config.add_section('real_eb2')
config.set('real_eb2', 'BrokerID', '6000')
config.set('real_eb2', 'UserID', '01301321')
config.set('real_eb2', 'Password', '123456')
config.set('real_eb2', 'q_ip', 'tcp://180.166.132.69:41213')
config.set('real_eb2', 't_ip', 'tcp://180.166.132.69:41205')

config.add_section('real_xh1')
config.set('real_xh1', 'BrokerID', '6090')
config.set('real_xh1', 'UserID', '16805660')
config.set('real_xh1', 'Password', '756482')
config.set('real_xh1', 'q_ip', 'tcp://116.228.171.216:41213')
config.set('real_xh1', 't_ip', 'tcp://116.228.171.216:41205')

config.add_section('real_xh2')
config.set('real_xh2', 'BrokerID', '6090')
config.set('real_xh2', 'UserID', '16805660')
config.set('real_xh2', 'Password', '756482')
config.set('real_xh2', 'q_ip', 'tcp://116.228.171.220:51213')
config.set('real_xh2', 't_ip', 'tcp://116.228.171.220:51205')

config.add_section('real_ht1')
config.set('real_ht1', 'BrokerID', '8000')
config.set('real_ht1', 'UserID', '70000542')
config.set('real_ht1', 'Password', '123456')
config.set('real_ht1', 'q_ip', 'tcp://180.168.212.75:41213')
config.set('real_ht1', 't_ip', 'tcp://180.168.212.75:41205')

config.add_section('real_ht2')
config.set('real_ht2', 'BrokerID', '8000')
config.set('real_ht2', 'UserID', '70000542')
config.set('real_ht2', 'Password', '123456')
config.set('real_ht2', 'q_ip', 'tcp://210.5.151.249:51213')
config.set('real_ht2', 't_ip', 'tcp://210.5.151.249:51205')

# ------------------- mongodb -------------------
config.add_section('mongodb1')
config.set('mongodb1', 'ip1', 'mongodb://root:Xhmz372701@114.55.54.144:3717')
config.set('mongodb1', 'ip2', 'mongodb://root:Xhmz372701@114.55.54.144:3718')
config.set('mongodb1', 'db', 'CtpData')

config.add_section('mongodb2')
config.set('mongodb2', 'ip1', 'mongodb://root:Xhmz372701@114.215.252.135:3717')
config.set('mongodb2', 'ip2', 'mongodb://root:Xhmz372701@114.215.252.135:3718')
config.set('mongodb2', 'db', 'CtpData')

config.add_section('mongodbi')
config.set('mongodbi', 'ip1', 'mongodb://root:Xhmz372701@dds-bp1affea778ad1842.mongodb.rds.aliyuncs.com:3717,dds-bp1affea778ad1841.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-1401299')
config.set('mongodbi', 'ip2', 'mongodb://root:Xhmz372701@dds-bp1affea778ad1842.mongodb.rds.aliyuncs.com:3717,dds-bp1affea778ad1841.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-1401299')
config.set('mongodbi', 'db', 'CtpData')

with open('config.ini', 'w') as f:
    config.write(f)
