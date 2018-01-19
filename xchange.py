import sys
import json
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

showboldStart = '\033[1;37;40m'
showboldEnd = '\033[0m'

def cex_INR_on_deposit(dollars):
	return (1.035*dollars+0.25)*one_usd_in_inr

def cex_bitcoin_for_dollars(dollars,cex_btc_USD):
	return round(((1-0.0016)*dollars)/cex_btc_USD,8)

def after_transfer(btc):
	return round((btc-0.001),8)

one_usd_in_inr = 67.5

def conversion_cex_zebpay_koinex():
	# CEX
	print('\n')
	cex_url = 'https://cex.io/btc-usd'
	cex_btc_usd_response = requests.get(cex_url)
	cex_btc_usd_soup = BeautifulSoup(cex_btc_usd_response.content,'html.parser')
	cex_btc_USD = float(cex_btc_usd_soup.find('span',{'id':'ticker-BTC-USD-price'}).text.strip())
	print('Cex.io 1 BTC in dollar ',showboldStart,cex_btc_USD,showboldEnd)
	print('Cex.io 1 BTC in rupees to pay ',cex_INR_on_deposit(cex_btc_USD))

	# Zebpay
	zebpay_url = 'https://www.zebapi.com/api/v1/market/ticker/btc/inr'
	zebpay_btc_INR = requests.get(zebpay_url).json()['sell']
	print('Zebpay 1 BTC in rupees ',zebpay_btc_INR)

	driver = webdriver.Firefox()
	koinex_url = 'https://koinex.in/api/dashboards/ticker'
	driver.get(koinex_url)
	time.sleep(5)
	soup =BeautifulSoup(driver.page_source,'html.parser')
	btc_span = soup.find(id='/BTC').find('span',{'class' : 'objectBox objectBox-string'})
	koinex_btc_INR = float(btc_span.text.replace('"','').strip())
	driver.close()
	print('Koinex 1 BTC in rupees ',koinex_btc_INR)

	# 0.2% transactin fee on that fee 18% GST = 0.236 % fee
	Zebpay_CEX_ratio = ((1-0.00236)*0.99*zebpay_btc_INR)/cex_INR_on_deposit(cex_btc_USD)
	Zebpay_percent_profit = (Zebpay_CEX_ratio-1)*100;
	print('\033[1;37;40m',round(Zebpay_percent_profit,2),'% \033[0m Profit on selling on Zebpay')

	# 0.2% transaction fee // don't know about GST take it 18% GST = 0.236% fee
	# Koinex_CEX_ratio = ((0.998)*0.99*koinex_btc_INR)/cex_INR_on_deposit(cex_btc_USD)
	Koinex_CEX_ratio = ((1-0.00236)*0.99*koinex_btc_INR)/cex_INR_on_deposit(cex_btc_USD)
	Koinex_percent_profit = (Koinex_CEX_ratio-1)*100;
	print('\033[1;37;40m',round(Koinex_percent_profit,2),'% \033[0m Profit on selling on Koinex')

	if(len(sys.argv)>1):
		deposited_in_dollars = float(sys.argv[1])
		INR_of_Dollars  = cex_INR_on_deposit(deposited_in_dollars)
		print('INR value for deposited dollars  : ',INR_of_Dollars)
		bitcoin = cex_bitcoin_for_dollars(deposited_in_dollars,cex_btc_USD)
		bitcoin_after_transfer = after_transfer(bitcoin)
		print('Got BTC on cex.io for',deposited_in_dollars,'$ : ',bitcoin)
		print('\n')
		print('On Zebpay Got INR value on selling ',bitcoin_after_transfer,'bitcoins on Zebpay : Rs',bitcoin_after_transfer*zebpay_btc_INR*(1-0.00236))
		print('On Zebpay , Profit in Rs \033[1;37;40m',(bitcoin_after_transfer*zebpay_btc_INR)-INR_of_Dollars,'\033[0m')
		print('\n')
		print('On Koinex Got INR value on selling ',bitcoin_after_transfer,'bitcoins on Koinex : Rs',bitcoin_after_transfer*koinex_btc_INR*(1-0.00236))
		print('On Koinex , Profit in Rs \033[1;37;40m',(bitcoin_after_transfer*koinex_btc_INR)-INR_of_Dollars,'\033[0m')

	print('\n')
	return 'Working'


conversion_cex_zebpay_koinex()
	

