import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import bs4
import steammarket as sm
from decimal import *
from colorama import Fore, Back, Style
from forex_python.converter import CurrencyRates
import os
import pyshorteners

c = CurrencyRates()

#-----------Variables-----------
Sum = 0
exchangeRate = 1.62
correctionFactor = 1
goodMultiplier = 2.8
empty = True
bundles = False
bundleMismatch = False
itemSound = False
store_not_empty = 0
#--------------------------------

options = Options()

#------------Dont Open A Browser (Mac)----------------
options.add_argument("--headless")  # Runs Chrome in headless mode.
options.add_argument('--no-sandbox')  # Bypass OS security model
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
options.add_experimental_option("detach", True)

#----------Dont Open A Browser (Windows)--------------
#options.add_argument("--headless") # Runs Chrome in headless mode.
#options.add_argument('--no-sandbox') # Bypass OS security model
#options.add_argument('--disable-gpu')  # applicable to windows os only
#options.add_argument('start-maximized') #
#options.add_argument('disable-infobars')
#options.add_argument("--disable-extensions")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.set_window_position(970,0)
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
xpath_list = []
temp_list_integer = []
temp_list_string = []
bundle_list = []
evans_list = []
second_list = []
statement = []
gunNameList = []
skinNameList = []
skinWearList = []
checkList = [0, 0]
#--------------------------------------

count = 0
count2 = 0

def reset():
    list.clear()
    store_name.clear()
    discount_price.clear()
    new_list.clear()
    newer_list.clear()
    size_list.clear()
    xpath_list.clear()
    temp_list_integer.clear()
    temp_list_string.clear()
    bundle_list.clear()
    evans_list.clear()
    second_list.clear()
    statement.clear()

def steamMarketWorking():
    item = sm.get_csgo_item('AK-47 | Frontside Misty (Field-Tested)', currency='USD')
    if item is None:
        print(Fore.RED + "                                                             -----Steam Market Library Currently Down-----")
        print(Style.RESET_ALL)
        main()
    else:
        print(Fore.GREEN + "                                                               -----Steam Market Working As Expected-----")
        print(Style.RESET_ALL)

def findLink(name):

    gunNameList.clear()
    skinNameList.clear()
    skinWearList.clear()

    if name == 'Bundle':
        name = 'MAC-10 | Monkeyflage (Well-Worn)'

    vanilla = False
    knife = False
    IndexGunName = 0
    counters = 0
    x = name.split()

    for i in range(len(x)):
        if '★' in x and len(x) < 2:
            x.remove(x[0])
            vanilla = True
        if '★' in x and len(x) < 2:
            knife = True

    for i in range(len(x)):
        if x[i] == '|':
            IndexGunName = i

    if IndexGunName != 0:
        for i in range(IndexGunName):  # Find Gun Name
            gunNameList.append(x[i])

    for j in range(len(x)):  # Find where skin wear index is
        if "(" in x[j]:
            skinWearIndex = j
            break
        else:
            skinWearIndex = 0

    for i in range(skinWearIndex, len(x)):  # Adds skin wear to list
        skinWearList.append(x[i])

    for i in range(IndexGunName + 1, skinWearIndex):  # Adds gun name to list
        skinNameList.append(x[i])

    for i in range(len(gunNameList) - 1):
        counters = counters + 1
        gunNameList.insert(i + counters, '%20')

    for l in range(len(skinNameList) - 1):
        l = l + 1
        skinNameList.insert(l, '%20')

    for i in range(len(skinWearList) - 1):
        i = i + 1
        skinWearList.insert(i, '%20')

    gunName = ''.join(gunNameList)
    skinName = ''.join(skinNameList)
    skinWear = ''.join(skinWearList)

    if 'Minimal' in skinWearList[0]:
        a = 'https://steamcommunity.com/market/listings/730/' + gunName + '%20%7C%20' + skinName + '%20(Minimal%20Wear)'
    elif 'Factory' in skinWearList[0]:
        a = 'https://steamcommunity.com/market/listings/730/' + gunName + '%20%7C%20' + skinName + '%20%28Factory%20New%29'
    elif vanilla == True:
        a = 'https://steamcommunity.com/market/listings/730/%E2%98%85%20' + skinWear
    elif knife == True:
        a = 'https://steamcommunity.com/market/listings/730/%E2%98%85%20' + gunName + '%20%7C%20' + skinName + '%20' + skinWear
    else:
        skinWear = skinWear.replace('(', '')
        skinWear = skinWear.replace(')', '')
        a = 'https://steamcommunity.com/market/listings/730/' + gunName + '%20%7C%20' + skinName + '%20%28' + skinWear + '%29'

    shortener = pyshorteners.Shortener()
    global new_link
    new_link = shortener.tinyurl.short(a)

def openBoxes():
    for x in range(len(size_list)):
        finalString = "listing[" + str(x + 1) + "]"
        temp_list_integer.append(finalString)

    for element in temp_list_integer:
        temp_list_string.append(str(element))

    for p in range(len(size_list)):
        string = "/html/body/app-root/div/div[1]/div/div/app-csgo-market/div[2]/app-p2p2-trading-market/div/app-p2p-trading-listing-container/div/app-p2p-trading-listing[1]/div/div[2]/button"
        new_string = string.replace("listing[1]", temp_list_string[p])
        xpath_list.append(new_string)

    for i in range(len(size_list)):
        button = driver.find_element(By.XPATH, xpath_list[i])
        button.click()

def bundleFinder():
    for x in range(len(bundleSoup)):
        stringCheck = str(bundleSoup[x])
        stringCheck2 = stringCheck.find("item")
        bundle_list.append(stringCheck[stringCheck2 : 40])

    for i in range(len(bundle_list)):
        if bundle_list[i] != 'item small':
            bundle_list[i] = 'item large'

    c = 0  # counter variable
    bundle = False
    lastBundle = False
    global bundleCount
    bundleCount = []  # empty list
    for x in bundle_list:
        if x == 'item small':
            lastBundle = False
            c += 1
            bundle = True
        elif (bundle == False and x == 'item large') or (lastBundle == True and x == 'item large'):
            c = 0
            bundleCount.append(c)  # appending the current value of c which contains total number of small items
        elif x == 'item large':
            bundleCount.append(c)  # appending the current value of c which contains total number of small items
            c = 0
            bundleCount.append(c)
            lastBundle = True
    if len(bundle_list)!=0:
        if bundle_list[-1] == 'item small':  # to check if there are any small item left
            bundleCount.append(c)

    m = 0
    for i in range(len(bundleCount)): #Count number of bundles
        if bundleCount[i] > 0:
            m = m+1

    num_bundles = len(size_list) - len(store_name)

    if num_bundles != m:
        for i in range(num_bundles-m):
            bundleMismatch = True
            indexOfMax = bundleCount.index(max(bundleCount))
            bundleCount.insert(indexOfMax + 1, 2)

    for y in range(len(bundleCount)):
        if bundleCount[y] == 0:
            bundleCount[y] = 'Single'
        else:
            bundleCount[y] = 'Bundle'


def skinCheck(name):
    print('                                                                   ----- New Skins, Rechecking -----')
    item = sm.get_csgo_item(name, currency='USD')
    if item is None:
        print(                                                         "Skin Library is down, Try again later :(")
        for g in range(5):
            print(5-g)
            time.sleep(1)
        exit()
    item_price = item.values()
    for key in item.keys():
        if item[key] == False:
            print("Item Not Found")
            return
        list.append(item[key])
    USDPrice = list[1][1:]
    USDPrice = USDPrice.replace(",", "")
    NZDPrice = Decimal(USDPrice) * Decimal(exchangeRate) * Decimal(correctionFactor)
    prices.append(NZDPrice) #To Calculate total
    list.clear()

def printsStatement():
    for e in range(len(store_name)):
        findLink(store_name[e])
        multiplier = float(prices[e])/float(newer_list[e])
        multiplier = str(round(multiplier, 2))
        if store_name[e] == 'Bundle                              ':
            statement.append(Fore.YELLOW + 'Bundle')
        elif (float(newer_list[e]) * goodMultiplier) > prices[e]:
            statement.append(Fore.RED + 'BAD DEAL - ' + multiplier + 'x')
        else:
            statement.append(Fore.GREEN +'GOOD DEAL - ' + multiplier + 'x')
            os.system('say "Good Deal Spotted"')
        print(Style.RESET_ALL)
        if prices[e] == 0.0000:
            prices[e] = '      No Suggested Price                '
            print((str(store_name[e]) + '\t' + 'Site Price: $' + newer_list[e]).expandtabs(27),prices[e], statement[e])
        else:
            print((str(store_name[e]) + '\t' + 'Site Price: $' + newer_list[e]).expandtabs(54), '     Suggested Steam Price: $', "{:.2f}".format(prices[e]), '    ', statement[e], '       ' ,new_link)
    print(Style.RESET_ALL)
    newer_list.clear()
    reset()

def main():
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, "html.parser")
    global bundleSoup
    bundleSoup = soup.find_all("div",{"class":"item"})
    item_discount_price = soup.find_all("div", {"class": "listing-footer text-center"})
    item_store_name = soup.find_all("div", {"class": "item-name"})

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

    newerer_list = newer_list
    res = [eval(i) for i in newerer_list]
    Sum = sum(res)
    checkList.append(Sum)
    if len(checkList) > 2:
        checkList.pop(0)

    if len(store_name) > 0 or len(newer_list) > 0:
        #print('                                            Number of single items:', len(store_name))
        #print('                                            Number of bundles:     ', len(size_list) - len(store_name))
        global itemSound
        if itemSound == True:
            os.system('say "Item Found"')
            itemSound = False
    else:
        print('                                                                Store empty, Refreshing Momentarily....')
        itemSound = True

    if checkList[0] != checkList[1]:
        prices.clear()
        for i in range(len(store_name)):
            skinCheck(store_name[i])
        bundleFinder()
        for e in range(len(item_discount_price)):
            if len(store_name) != len(newer_list):
                for i in range(len(bundleCount)):
                    if bundleCount[i] == 'Bundle':
                        store_name.insert(i, bundleCount[i] + '                              ')
                        prices.insert(i, 0.0000)
        printsStatement()
        reset()
    else:
        bundleFinder()
        for e in range(len(item_discount_price)):
            if len(store_name) != len(newer_list):
                for i in range(len(bundleCount)):
                    if bundleCount[i] == 'Bundle':
                        store_name.insert(i, bundleCount[i] + '                              ')
                        prices.insert(i, 0.0000)
        printsStatement()

    if len(item_discount_price) != 0:
        global empty
        empty = False
        return empty
    else:
        empty = True
        return empty

print('                                           ******************* Code Starting - Code By Evan Holfich *******************')
steamMarketWorking()
driver.get("https://www.wtfskins.com/withdraw")
time.sleep(0.5)
#driver.minimize_window()
main()
openBoxes()

def loop():
    for window in Windows:
        driver.switch_to.window(window)
        driver.refresh()
        time.sleep(0.5)
        main()
        openBoxes()
        if count % 20 == 0:  #Every 100 check to ensure steam market is working
            steamMarketWorking()

while True:
    time.sleep(1)  # sleep for 5 seconds
    count = count + 1
    Windows = driver.window_handles
    print('+-----------------------------------------------------------------+----------------------------------+-----------------------------------------------------------------+')
    print('|                                                                 |     Refreshing, Refresh #', count,'     |                                                                  |')
    print('+-----------------------------------------------------------------+----------------------------------+-----------------------------------------------------------------+')
    loop()
