import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import bs4
import steammarket as sm
from decimal import *
from colorama import Fore, Back, Style
from forex_python.converter import CurrencyRates

c = CurrencyRates()

#-----------Variables-----------
exchangeRate = 1.62
correctionFactor = 1
goodMultiplier = 2.35
empty = True
bundles = False
store_not_empty = 0
#--------------------------------

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
ua = UserAgent()
opts = Options()
opts.add_argument("user-agent="+ua.random)

#----------------Lists----------------
list = []
prices = []
store_name = []
discount_price = []
new_list = []
newer_list = []
size_list = []
#--------------------------------------

count = 0

def reset():
    store_name.clear()
    discount_price.clear()
    new_list.clear()
    newer_list.clear()
    size_list.clear()

def main():
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, "html.parser")

    item_store_name = soup.find_all("div",{"class":"item-name"})
    item_discount_price = soup.find_all("div",{"class":"listing-footer text-center"})

    for name in item_store_name:
        store_name.append(name.text)

    for discount in item_discount_price:
        discount_price.append(discount.text)

    #Clean up the price
    for j in range(len(discount_price)):
        my_str = discount_price[j]
        result = my_str[my_str.find('\n') + 1: my_str.rfind('\n')]
        result = result.strip()
        new_list.append(result)
        if '%' in new_list[j]:  # Filtering listing with discount
            newResult = result[result.find('\n') + 11: result.rfind('\n')]
        else:  # Filtering listing without discount
            newResult = result[result.find('\n') + 11: 20]
        newer_list.append(newResult)

    for g in range(len(newer_list)):
        size_list.append(newer_list[g])


    print('Number of single items:', len(store_name))
    print('Number of bundles:     ', len(size_list) - len(store_name))
    print('***********************************************')

    def skinCheck(name):
        item = sm.get_csgo_item(name, currency='USD')
        item_price = item.values()
        for key in item.keys():
            if item[key] == False:
                ErrorMessage = "Item Not Found"
                print(ErrorMessage)
                return
            list.append(item[key])
        USDPrice = list[1][1:]
        USDPrice = USDPrice.replace(",", "")
        NZDPrice = Decimal(USDPrice) * Decimal(exchangeRate) * Decimal(correctionFactor)
        prices.append(NZDPrice) #To Calculate total
        list.clear()

    for i in range(len(store_name)):
        skinCheck(store_name[i])

    #Print Full List
    for e in range(len(item_discount_price)):
        if len(store_name) != len(newer_list):
            bundles = True
            print('BUNDLE DETECTED, CODE ABORTED')
            break
        else:
            if (float(newer_list[e]) * goodMultiplier) > prices[e]:
                statement = Fore.RED + 'BAD DEAL'
            else:
                statement = Fore.GREEN +'GOOD DEAL'
            print(Style.RESET_ALL)
            print(('Item: ' + str(store_name[e]) + '\t' + 'Price: $' + newer_list[e]).expandtabs(25), '           Suggested Steam Price: $', "{:.2f}".format(prices[e]), '    ', statement)
        print(Style.RESET_ALL)
    newer_list.clear()

    if len(item_discount_price) != 0: #THIS LINE CAUSING ISSUES
        global empty
        empty = False
        return empty
    else:
        empty = True
        return empty


driver.get("https://www.wtfskins.com/withdraw")
time.sleep(0.5)
main()
reset()

while True:
    time.sleep(5)  # sleep for 2 seconds
    count = count + 1
    Windows = driver.window_handles
    print('***********************************************\n')
    print('Refreshing, Refresh #', count)
    for window in Windows:
        driver.switch_to.window(window)
        driver.refresh()
        time.sleep(0.5)
        main()
        reset()
