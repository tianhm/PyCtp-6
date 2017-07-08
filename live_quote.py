import os
import sys
import argparse
import pandas as pd
import datetime as dt
import pytz
from configparser import SafeConfigParser
# mpath = os.path.join(os.path.abspath('..'), 'hf_py_ctp')
mpath = os.path.join(os.path.abspath('..'), 'hf_ctp_py_proxy')
sys.path.append(mpath)
from py_ctp.ctp_struct import *
from py_ctp.trade import Trade
from py_ctp.quote import Quote
mpath = os.path.join(os.path.abspath('..'), 'PyShare\\PyShare')
sys.path.append(mpath)
import Mongo

class Test:
	def __init__(self, args):
		print(dt.datetime.today(), '---- __init__ ----')
# 		self.rootdir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
		self.rootdir = os.getcwd()
# 		parse command line input args
		self.ProductClass2 = list() if args.product is None else [x.upper() for x in args.product]
		self.ExchangeID2 = list() if args.exchange is None else [x.upper() for x in args.exchange]
		self.ProductID2 = list() if args.underlying is None else [x.upper() for x in args.underlying]
		account = 'real_eb1' if args.account is None else args.account[0]
		mongodb = 'mongodb1' if args.mongodb is None else args.mongodb[0]
# 		print(self.ProductClass2)
# 		print(self.ExchangeID2)
# 		print(self.ProductID2)
# 		print(account)
# 		print(mongodb)
		
# 		ctp connection, current path is '...\PyCtp'			
		config = SafeConfigParser()
		ctp_path = os.path.join(os.path.abspath('..'), 'PyShare', 'config', 'ctp_connection.ini')
		config.read(ctp_path)		
		self.BrokerID = config.get(account, 'BrokerID')
		self.UserID = config.get(account, 'UserID')
		self.Password = config.get(account, 'Password')
		self.q_ip = config.get(account, 'q_ip')
		self.t_ip = config.get(account, 't_ip')
		self.Session = ''
		self.q = Quote()
		self.t = Trade()
		self.contract = list()
		self.contractdf = pd.DataFrame()
		self.TradingDay = ''

# 		create connection to mongodb, make sure it is primary connection
		mongo_path = os.path.join(os.path.abspath('..'), 'PyShare', 'config', 'mongodb_connection.ini')
		self.mdb = Mongo.MongoDB(mongo_path)
		mdb_connection_result = self.mdb.connect(mongodb)
			
# ----------------- quote related method -----------------

	def q_OnFrontConnected(self):
		print(dt.datetime.today(), '---- q_OnFrontConnected ----')
# 		when q_ip is reached, start user login, can be anonymous
# 		self.q.ReqUserLogin(BrokerID=self.BrokerID, UserID=self.UserID, Password=self.Password)
		self.q.ReqUserLogin()
		
	def q_OnFrontDisconnected(self, nReason = int):
		print(dt.datetime.today(), '---- q_OnFrontDisconnected ----')
# 		time.sleep(60)
		
	def q_OnRspUserLogin(self, pRspUserLogin = CThostFtdcRspUserLoginField, pRspInfo = CThostFtdcRspInfoField, nRequestID = int, bIsLast = bool):
		print(dt.datetime.today(), '---- q_OnRspUserLogin ----')
# 		print(pRspUserLogin)
# 		print(pRspInfo)
# 		print(nRequestID)
# 		print(bIsLast)
		if pRspInfo.getErrorID() == 0:
			self.TradingDay = pRspUserLogin.getTradingDay()			
			self.contractdf = pd.read_csv(os.path.join(self.rootdir, 'contract.csv'))
# 	 		print(self.contractdf)		
			ff = pd.Series.repeat(pd.Series([True]), self.contractdf.shape[0])		
			p_idx = ff if len(self.ProductClass2)==0 else self.contractdf['ProductClass2'].isin(self.ProductClass2)
			e_idx = ff if len(self.ExchangeID2)==0 else self.contractdf['ExchangeID2'].isin(self.ExchangeID2)
			u_idx = ff if len(self.ProductID2)==0 else self.contractdf['ProductID2'].isin(self.ProductID2)				
			idx = [a and b and c for a, b, c in zip(p_idx, e_idx, u_idx)]		
			gg = self.contractdf.loc[idx]
			print('ProductClass', self.ProductClass2)
			print('Exchange', self.ExchangeID2)
			print('Underlying', self.ProductID2)
			print('TradingDay', self.TradingDay)
			print(dt.datetime.today(), '---- total number of selected symbol', gg.shape[0], '----')			
			if (not any(idx)):
				input('no matched symbols, press enter key to exit')
				sys.exit(2)
			else:
				print(dt.datetime.today(), '---- SubscribeMarketData ----')
				for index, row in gg.iterrows():
# 					print(row['InstrumentID'], row['Symbol'])
# 	 				** create index in mongodb for faster query, removed, using single python script instead **
# 					self.mdb.create_index_once(row['Symbol'], 'TradingDay', True)
# 	 		 		case sensitive, e.g., IF1612 is not the same as if1612
					self.q.SubscribeMarketData(row['InstrumentID'])	
				print(dt.datetime.today(), '---- SubscribeMarketData finished ----')
		else:
			print('OnRspUserLogin Error', pRspInfo)
							
	def q_OnRtnDepthMarketData(self, pDepthMarketData = CThostFtdcDepthMarketDataField):
# 		print(dt.datetime.today(), '---- q_OnRtnDepthMarketData ----')
# 		print(pDepthMarketData)		
		tk = pDepthMarketData

# 		ExchangeID --> ExchangeID2, InstrumentID --> Instrumentid2, e.g., Symbol = 'SHFE.CU1612'
		kk = self.contractdf.loc[self.contractdf['InstrumentID']==tk.getInstrumentID()]			
		cc = kk['Symbol'].values.tolist()[0]
			
# 		convert TradingDay='20161115' to TradingDay='2016-11-15' format, e.g., _id = 2016-11-15 13:26:00
# 		dt.datetime.strptime(tk.getTradingDay(),'%Y%m%d').strftime('%Y-%m-%d')
# 		' '.join([dt.datetime.today().strftime('%Y-%m-%d'), tk.getUpdateTime()])
# 		dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')
# 		'TradingDay':dt.datetime.strptime(tk.getTradingDay(),'%Y%m%d').strftime('%Y-%m-%d'), 'UpdateTime':tk.getUpdateTime(), 'UpdateMillisec':tk.getUpdateMillisec()
# 		self.TradingDay = pRspUserLogin.getTradingDay(), use TradingDay from pRspUserLogin
# 		print(self.TradingDay, tk.getTradingDay())		
		CTPTIME = pytz.timezone('Asia/Shanghai').localize(
			dt.datetime.strptime(' '.join([tk.getTradingDay(),tk.getUpdateTime(),str(tk.getUpdateMillisec())]),'%Y%m%d %H:%M:%S %f'))		
		sdd = {'_id':dt.datetime.utcnow(),
			'BID':tk.getBidPrice1(), 'ASK':tk.getAskPrice1(), 'BVOL':int(tk.getBidVolume1()), 'AVOL':int(tk.getAskVolume1()),
			'LAST':tk.getLastPrice(), 'VOLUME':int(tk.getVolume()), 'OI':int(tk.getOpenInterest()),
			'TradingDay':self.TradingDay, 'CTPTIME':CTPTIME}

		if sdd['BID']>1e32 and sdd['ASK']>1e32 and sdd['BVOL']==0 and sdd['AVOL']==0:
# 			do not record these points
			print('U', end='', flush=True)
		else:
# 	 		price used for charting
			print('x', end='', flush=True)
			if sdd['BVOL'] > 0:
				sdd['PRICE'] = sdd['BID']
			else:
				if sdd['AVOL'] > 0:
					sdd['PRICE'] = sdd['ASK']
				else:
					if sdd['VOLUME'] > 0:
						sdd['PRICE'] = sdd['LAST']
					else:
						sdd['PRICE'] = tk.getPreSettlementPrice()
			
# 	 		check if a collection exists, upsert = update + insert, trust the latest data is the correct data, even if the previous data maybe correct
			result = self.mdb.upsert_dict(cc, sdd, '_id')

	def q_OnRspSubMarketData(self, pSpecificInstrument = CThostFtdcSpecificInstrumentField, pRspInfo = CThostFtdcRspInfoField, nRequestID = int, bIsLast = bool):
# 		print(dt.datetime.today(), '---- q_OnRspSubMarketData ----')
# 		print(pSpecificInstrument)
# 		print(pRspInfo)
# 		print(nRequestID)
# 		print(bIsLast)
		pass
	
	def StartQuote(self):
		print(dt.datetime.today(), '---- StartQuote ----')
		api = self.q.CreateApi()
		spi = self.q.CreateSpi()
		self.q.RegisterSpi(spi)

		self.q.OnFrontConnected = self.q_OnFrontConnected
		self.q.OnFrontDisconnected = self.q_OnFrontDisconnected
		self.q.OnRspUserLogin = self.q_OnRspUserLogin
		
# 		market data subscription and return depth data
		self.q.OnRtnDepthMarketData = self.q_OnRtnDepthMarketData
		self.q.OnRspSubMarketData = self.q_OnRspSubMarketData
		
# 		initiate connection to quote server
		self.q.RegCB()
		self.q.RegisterFront(self.q_ip)
		self.q.Init()
		self.q.Join()

# ----------------- trade related method -----------------

	def OnFrontConnected(self):
		print(dt.datetime.today(), '---- OnFrontConnected ----')
		self.t.ReqUserLogin(BrokerID=self.BrokerID, UserID=self.UserID, Password=self.Password)

	def OnFrontDisconnected(self, nReason = int):
		print(dt.datetime.today(), '---- OnFrontDisconnected ----')
# 		time.sleep(60)
		
	def OnRspUserLogin(self, pRspUserLogin = CThostFtdcRspUserLoginField, pRspInfo = CThostFtdcRspInfoField, nRequestID = int, bIsLast = bool):
		print(dt.datetime.today(), '---- OnRspUserLogin ----')
# 		print(pRspUserLogin)
# 		print(pRspInfo)
# 		print(nRequestID)
# 		print(bIsLast)
		if pRspInfo.getErrorID() == 0:
			self.Session = pRspUserLogin.getSessionID()
			self.t.ReqSettlementInfoConfirm(BrokerID=self.BrokerID, InvestorID=self.UserID)
			self.TradingDay = pRspUserLogin.getTradingDay()
		else:
			print('OnRspUserLogin Error', pRspInfo)

	def OnRspUserLogout(self, pUserLogout = CThostFtdcUserLogoutField, pRspInfo = CThostFtdcRspInfoField, nRequestID = int, bIsLast = bool):
		print(dt.datetime.today(), '---- OnRspUserLogout ----')
# 		print(pUserLogout)
# 		print(pRspInfo)
# 		print(nRequestID)
# 		print(bIsLast)
		
	def OnRtnOrder(self, pOrder = CThostFtdcOrderField):
# 		print(dt.datetime.today(), '---- OnRtnOrder ----')
# 		print(pOrder)
		pass
		
	def OnErrRtnOrderInsert(self, pInputOrder = CThostFtdcInputOrderField, pRspInfo = CThostFtdcRspInfoField):
# 		print(dt.datetime.today(), '---- OnErrRtnOrderInsert ----')
# 		print(pInputOrder)
# 		print(pRspInfo)
		pass

	def OnErrRtnOrderAction(self, pOrderAction = CThostFtdcOrderActionField, pRspInfo = CThostFtdcRspInfoField):
# 		print(dt.datetime.today(), '---- OnErrRtnOrderAction ----')
# 		print(pOrderAction)
# 		print(pRspInfo)
		pass
		
	def OnRtnTrade(self, pTrade = CThostFtdcTradeField):
# 		print(dt.datetime.today(), '---- OnRtnTrade ----')
# 		print(pTrade)
		pass

	def OnRtnQueryBankBalanceByFuture(self, pNotifyQueryAccount = CThostFtdcNotifyQueryAccountField):
# 		print(dt.datetime.today(), '---- OnRtnQueryBankBalanceByFuture ----')
# 		print(pNotifyQueryAccount)
		pass

	def OnRtnFromBankToFutureByFuture(self, pRspTransfer = CThostFtdcRspTransferField):
# 		print(dt.datetime.today(), '---- OnRtnFromBankToFutureByFuture ----')
# 		print(pRspTransfer)
		pass
	
	def OnRtnFromFutureToBankByFuture(self, pRspTransfer = CThostFtdcRspTransferField):
# 		print(dt.datetime.today(), '---- OnRtnFromFutureToBankByFuture ----')
# 		print(pRspTransfer)
		pass
	
	def OnRtnTradingNotice(self, pTradingNoticeInfo = CThostFtdcTradingNoticeInfoField):
# 		print(dt.datetime.today(), '---- OnRtnTradingNotice ----')
# 		print(pTradingNoticeInfo)
		pass	
				
	def OnRtnInstrumentStatus(self, pInstrumentStatus = CThostFtdcInstrumentStatusField):
# 		print(dt.datetime.today(), '---- OnRtnInstrumentStatus ----')
# 		print(pInstrumentStatus)
		pass
	
	def OnRspSettlementInfoConfirm(self, pSettlementInfoConfirm = CThostFtdcSettlementInfoConfirmField, pRspInfo = CThostFtdcRspInfoField, nRequestID = int, bIsLast = bool):
		print(dt.datetime.today(), '---- OnRspSettlementInfoConfirm ----')
# 		print(pSettlementInfoConfirm)
# 		print(pRspInfo)
# 		print(nRequestID)
# 		print(bIsLast)
		self.t.ReqQryInstrument()
		
	def OnRspQryInstrument(self, pInstrument = CThostFtdcInstrumentField, pRspInfo = CThostFtdcRspInfoField, nRequestID = int, bIsLast = bool):
# 		print(dt.datetime.today(), '---- OnRspQryInstrument ----')
# 		if pInstrument.getInstrumentID()=='SR709C7000' or pInstrument.getInstrumentID()=='m1709-P-2800':
# 			print(pInstrument)
# 		print(pRspInfo)
# 		print(nRequestID)
# 		print(bIsLast)
# 		StartQuote after getting all the contract information, ctp InstrumentID has a mixture of upper and lower case
# 		contract definition, * is not used
# 		exchange, underlying, contract, expiration
# 		[base]: base_exchange, base_underlying(*), base_contract
# 		[pricing]: pricing_exchange, pricing_underlying(*), pricing_contract
# 		[hedging]: hedging_exchange, hedging_underlying(*), hedging_contract
		mm = [pInstrument.getInstrumentID(), pInstrument.getExchangeID(), pInstrument.getProductID(), str(pInstrument.getProductClass()).split('.')[1], pInstrument.getExchangeID(), pInstrument.getUnderlyingInstrID()]
		nn = [x.upper() for x in mm]
		tt = [pInstrument.getPriceTick(), pInstrument.getExpireDate()]
		self.contract.append(mm + nn + tt)		
		if bIsLast:
			print(dt.datetime.today(), '---- OnRspQryInstrument Completed ----')
			self.contractdf = pd.DataFrame(self.contract, columns=['InstrumentID','ExchangeID','ProductID','ProductClass','UnderlyingExchangeID','UnderlyingInstrID',
																'InstrumentID2','ExchangeID2','ProductID2','ProductClass2','UnderlyingExchangeID2','UnderlyingInstrID2',
																'PriceTick','ExpireDate'])
			sg = self.contractdf[['ExchangeID2','InstrumentID2']]
			self.contractdf['Symbol'] = ['.'.join(x) for x in sg.values.tolist()]
# 		    change CZCE SRC and SRP underlying symbol to SR_O, may extend this list in the future
			idx = [row['ExchangeID2']=='CZCE' and row['ProductID2'] in ['SRC','SRP'] for index,row in self.contractdf.iterrows()]
			self.contractdf.loc[idx,'ProductID'] = 'SR_O'
			self.contractdf.loc[idx,'ProductID2'] = 'SR_O'
# 			export to a csv file, so it can be read by market data quote functions 
			self.contractdf.to_csv(os.path.join(self.rootdir, 'contract.csv'), index=False)				
			self.contract = list()
			print(dt.datetime.today(), '---- total number of ctp symbol', self.contractdf.shape[0], '----')			
# 			self.StartQuote()
			
	def Run(self):
		print(dt.datetime.today(), '---- Run ----')
		api = self.t.CreateApi()
		spi = self.t.CreateSpi()
		self.t.RegisterSpi(spi)

# 		rewrite default api interface
		self.t.OnFrontConnected = self.OnFrontConnected
		self.t.OnFrontDisconnected = self.OnFrontDisconnected
		self.t.OnRspUserLogin = self.OnRspUserLogin
		self.t.OnRspUserLogout = self.OnRspUserLogout
		
# 		have to confirm settlement result before moving to the next step
# 		run self.StartQuote() after settlement information is confirmed
		self.t.OnRspSettlementInfoConfirm = self.OnRspSettlementInfoConfirm
		
# 		order related
		self.t.OnRtnOrder = self.OnRtnOrder
		self.t.OnErrRtnOrderInsert = self.OnErrRtnOrderInsert
		self.t.OnErrRtnOrderAction = self.OnErrRtnOrderAction
		self.t.OnRtnTrade = self.OnRtnTrade
		
# 		FCM bank transfer, trading notice
		self.t.OnRtnQueryBankBalanceByFuture = self.OnRtnQueryBankBalanceByFuture
		self.t.OnRtnFromBankToFutureByFuture = self.OnRtnFromBankToFutureByFuture
		self.t.OnRtnFromFutureToBankByFuture = self.OnRtnFromFutureToBankByFuture		
		self.t.OnRtnTradingNotice = self.OnRtnTradingNotice
		
# 		get underlying (a.k.a instrument) status
		self.t.OnRtnInstrumentStatus = self.OnRtnInstrumentStatus
		
# 		return contract information
		self.t.OnRspQryInstrument = self.OnRspQryInstrument	

# 		initiate connection to trade server
		self.t.RegCB()
		self.t.RegisterFront(self.t_ip)
		self.t.Init()
		self.t.Join()

def main():
	parser = argparse.ArgumentParser(usage='Get CTP tick data')
	parser.add_argument('-m', '--mode', nargs='*', action="store")
	parser.add_argument('-p', '--product', nargs='*', action="store")
	parser.add_argument('-e', '--exchange', nargs='*', action="store")
	parser.add_argument('-u', '--underlying', nargs='*', action="store")
	parser.add_argument('-a', '--account', nargs='*', action="store")
	parser.add_argument('-d', '--mongodb', nargs='*', action="store")
	args = parser.parse_args()	
# 	print(args.mode)
# 	print(args.exchange is None)
# 	print(type(args.underlying))
	t = Test(args)
	try:
		if args.mode[0]=='t':
			t.Run()
		elif args.mode[0]=='q':
			t.StartQuote()
		else:
			input('unknown -m --mode argument, press enter key to exit')
	except:
		input('missing -m --mode argument, press enter key to exit')
		
if __name__ == "__main__":
	main()


# cd 'Z:\williamyizhu On My Mac\Documents\workspace\PyCtp'
# python .\live_quote.py -m t -a real_eb1 -d ctp_mongodb2
# python .\live_quote.py -m t -a real_xh1 -d ctp_mongodb2
# python .\live_quote.py -m t -a real_ht1 -d ctp_mongodb2
# python .\live_quote.py -m q -p futures -e dce -a real_eb1 -d ctp_mongodb2
# python .\live_quote.py -m q -p options -e dce -a real_eb1 -d ctp_mongodb2
