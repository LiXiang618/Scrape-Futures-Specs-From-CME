from contextlib import closing
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time

with open("symbols.txt") as f:
    symbols = f.readlines()
symbols = [x.strip().upper() for x in symbols]

class FutureClass:
    def __init__(self,symbol):
        self.symbol = symbol
        self.url = None
        self.productName = None
        self.clearing = None
        self.globex = None
        self.floor = None
        self.clearPort = None
        self.exchange = None
        self.productGroup = None
        self.clearedAs = None
        self.volume = None
        self.openInterest = None

        self.contractUnit = None
        self.priceQuotation = None
        self.tradingHours = None
        self.tradingHoursGlobex = None
        self.tradingHoursClearPort = None
        self.minimumPriceFluctuation = None
        self.productCode = None
        self.listedContracts = None
        self.settlementMethod = None
        self.floatingPrice = None
        self.terminationOfTrading = None
        self.settlementProcedures = None
        self.positionLimits = None
        self.exchangeRulebook = None
        self.blockMinimum = None
        self.priceLimitOrCircut = None
        self.vendorCodes = None

        self.errorFlag = None

ls = []

with closing(Chrome()) as browser:
    for i in range(len(symbols)):
        tmp = FutureClass(symbols[i])
        browser.get('http://www.cmegroup.com/search/?q='+symbols[i])
        elements = browser.find_elements_by_xpath("//tbody//tr[td/text()='"+symbols[i]+"' and contains(td,'Futures')]//td")
        if not elements:
            print(tmp.symbol+": No such symbol!")
            tmp.errorFlag = 1
            ls.append(tmp)
            continue

        tmp.productName = elements[0].text
        tmp.clearing = elements[1].text
        tmp.globex = elements[2].text
        tmp.floor = elements[3].text
        tmp.clearPort = elements[4].text
        tmp.exchange = elements[5].text
        tmp.productGroup = elements[6].text
        tmp.clearedAs = elements[7].text
        tmp.volume = elements[8].text
        tmp.openInterest = elements[9].text

        # elements[0].click()#The first qualified element
        linkElement = browser.find_elements_by_xpath("//tbody//tr[td/text()='"+symbols[i]+"' and contains(td,'Futures')]//td/a")
        linkElement[0].click()
        tmp.url = browser.current_url

        elements2 = browser.find_elements_by_xpath("//tbody/tr/td[@class='prodSpecAtribute']/../..//tr//td[2]")
        if not elements2:
            print(tmp.symbol+": Page not jump!")
            tmp.errorFlag = 2
            ls.append(tmp)
            continue

        elements2 = browser.find_elements_by_xpath("//tbody/tr/td[text()='Contract Unit']/../td")
        if elements2:
            tmp.contractUnit = elements2[1].text

        elements2 = browser.find_elements_by_xpath("//tbody/tr/td[text()='Price Quotation']/../td")
        if elements2:
            tmp.priceQuotation = elements2[1].text

        elements2 = browser.find_elements_by_xpath("//tbody/tr/td[text()='Trading Hours']/../td")
        if elements2:
            if len(elements2) == 2:
                tmp.tradingHours = elements2[1].text
            else:
                tmp.tradingHoursGlobex = elements2[2].text
                tmp.tradingHoursClearPort = browser.find_elements_by_xpath("//tbody/tr/td[text()='CME ClearPort:']/../td")[1].text

        elements2 = browser.find_elements_by_xpath("//tbody/tr/td[text()='Minimum Price Fluctuation']/../td")
        if elements2:
            tmp.minimumPriceFluctuation = elements2[1].text

        elements2 = browser.find_elements_by_xpath("//tbody/tr/td[text()='Product Code']/../td")
        if elements2:
            tmp.productCode = elements2[1].text

        elements2 = browser.find_elements_by_xpath("//tbody/tr/td[text()='Listed Contracts']/../td")
        if elements2:
            tmp.listedContracts = elements2[1].text

        elements2 = browser.find_elements_by_xpath("//tbody/tr/td[text()='Settlement Method']/../td")
        if elements2:
            tmp.settlementMethod = elements2[1].text

        elements2 = browser.find_elements_by_xpath("//tbody/tr/td[text()='Floating Price']/../td")
        if elements2:
            tmp.floatingPrice = elements2[1].text

        elements2 = browser.find_elements_by_xpath("//tbody/tr/td[text()='Termination Of Trading']/../td")
        if elements2:
            tmp.terminationOfTrading = elements2[1].text

        elements2 = browser.find_elements_by_xpath("//tbody/tr/td[text()='Settlement Procedures']/../td")
        if elements2:
            tmp.settlementProcedures = elements2[1].text

        elements2 = browser.find_elements_by_xpath("//tbody/tr/td[text()='Position Limits']/../td")
        if elements2:
            tmp.positionLimits = elements2[1].text

        elements2 = browser.find_elements_by_xpath("//tbody/tr/td[text()='Exchange Rulebook']/../td")
        if elements2:
            tmp.exchangeRulebook = elements2[1].text

        elements2 = browser.find_elements_by_xpath("//tbody/tr/td[text()='Block Minimum']/../td")
        if elements2:
            tmp.blockMinimum = elements2[1].text

        elements2 = browser.find_elements_by_xpath("//tbody/tr/td[text()='Price Limit Or Circuit']/../td")
        if elements2:
            tmp.priceLimitOrCircut = elements2[1].text

        elements2 = browser.find_elements_by_xpath("//tbody/tr/td[text()='Vendor Codes']/../td")
        if elements2:
            tmp.vendorCodes = elements2[1].text

        ls.append(tmp)
        # print(str(i)+": "+symbols[i])

import pickle
with open("results.txt",'wb') as f:
    pickle.dump(ls,f)
with open("results.txt","rb") as f:
    ls2 = pickle.load(f)

import pandas as pd
df = pd.DataFrame(columns=list(ls2[0].__dict__.keys()))
for i in range(len(ls2)):
    df = df.append(pd.DataFrame([list(ls2[i].__dict__.values())],columns=list(ls2[0].__dict__.keys())))
    print(i)

df.to_csv("resuls.csv")