import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests

class scraper():
    
    
    def __init__(self):
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.javascriptEnabled"] = True
        cap["phantomjs.page.settings.loadImages"] = True
        cap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
        self.driver = webdriver.PhantomJS('/Users/cyian/Desktop/NYU/FALL2017/DS-GA1007/Project/phantomjs-2.1.1-macosx/bin/phantomjs')
        self.ref = 0
        #driver = webdriver.Chrome('/mnt/d/Academic/Nyu/DS1007/project/chromedriver.exe')
    
    def bitfinex(self,st):
        btc_price = 0
        self.driver.delete_all_cookies()
        self.driver.get('https://www.bfxdata.com/')
        time.sleep(st)
        
        html = self.driver.page_source
        soup = BeautifulSoup(html, "lxml")
        #import pdb; pdb.set_trace()
        lines = soup.findAll('p',{"class":  'price_text', "id":  'priceBTCUSD'})
        btc_price = float(lines[0].get_text().replace(",",""))
        
        if btc_price == 0:
            raise AttributeError
        return btc_price
    
    def bittrex(self,st):
        btc_price = 0
        self.driver.delete_all_cookies()
        self.driver.get('https://bittrex.com/Market/Index?MarketName=USDT-BTC')
        time.sleep(st)
        
        html = self.driver.page_source
        soup = BeautifulSoup(html, "lxml")
        #import pdb; pdb.set_trace()
        lines = soup.findAll('span', {"data-bind": "text: summary.displayLast()"})
        btc_pl = lines[0]                          
        btc_price = float(btc_pl.get_text())

        if btc_price == 0:
            raise AttributeError
        return btc_price

    def gdax(self,st):
        btc_price = 0
        self.driver.delete_all_cookies()
        self.driver.get('https://www.gdax.com/')
        time.sleep(st)
        html = self.driver.page_source

        soup = BeautifulSoup(html, "lxml")
        lines = soup.findAll('li', {"class":  'ProductsList_product_3cAY6'})
        #import pdb; pdb.set_trace()
        for dl in lines:
            if dl.a.get_text() == 'BTC/USD':
            #import pdb; pdb.set_trace()
                btc_pl = dl.span
                btc_price = float(btc_pl.get_text().replace(",",""))
                break
        if btc_price == 0:
            raise AttributeError
        return btc_price
    
    def bitstamp(self,st):
        btc_price = 0
        self.driver.delete_all_cookies()
        self.driver.get('https://www.bitstamp.net/')
        time.sleep(st)
        html = self.driver.page_source

        soup = BeautifulSoup(html, "lxml")
        lines = soup.findAll('h3', {"id":  'last-price'})
        #import pdb; pdb.set_trace()
        for dl in lines:
            if dl.attrs['data-pair'] == 'btcusd':
                btc_price = float(dl.strong.get_text())
                break
        if btc_price == 0:
            raise AttributeError
        return btc_price
    
    def bithumb(self,st):
        self.url = 'https://api.bithumb.com/public/ticker/btc'
        r = requests.get(self.url).text
        dt = r.split(",")
        btc_price = float(dt[2].split(':')[1][1:-1]) / 1083.48
        return btc_price

    def fetch(self, name, data_list):
        func_dict = {'Bitfinex': self.bitfinex, 'Bittrex': self.bittrex, 'Gdax': self.gdax, 'Bitstamp': self.bitstamp,   
                     'Bithumb': self.bithumb}
        try:
            data_list.append(func_dict[name](1))
            if self.ref == 0:
                self.ref = func_dict[name](1)
        except AttributeError:
            try:
                if len(data_list) == 0:
                    data_list.append(func_dict[name](7.5))
                else:
                    data_list.append(func_dict[name](3))
            except AttributeError:
                if len(data_list) == 0:
                    data_list.append(self.ref)
                else:
                    data_list.append(data_list[-1])
                  
              
                  
         
            