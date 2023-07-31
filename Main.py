import time
import requests
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
import os
import pyshorteners
from selenium.common.exceptions import NoSuchElementException
import webbrowser
import pyautogui
from prettytable import PrettyTable
badDealTable = PrettyTable()

#------------------------Settings to change-----------------------
autoDeposit = False  #Turn on if you want system to auto deposit item - this takes control of mouse
mac = 1             #What operating system I am using
trackItem = False    #Turn on if I want to track item
myItem = 'Five-SeveN | Case Hardened (Well-Worn)'
goodMultiplier = 2.8
exchangeRate = 1.6240422
#-----------------------------------------------------------------

#-----------Variables-----------
Sum = 0
store_not_empty = 0
empty = True
bundles = False
bundleMismatch = False
itemSound = False
myItemBool = False
goodDeal = False
itemHasBeenInStore = False
itemInStore = False
#--------------------------------

options = Options()

if mac == 1:
    #------------Dont Open A Browser (Mac)----------------
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    options.add_experimental_option("detach", True)
else:
    #----------Dont Open A Browser (Windows)--------------
    options.add_argument("--headless") # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized') #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")

driver = webdriver.Chrome(service=Service(ChromeDriverManager(version='114.0.5735.90').install()), options=options)
driver.set_window_position(970,0)
ua = UserAgent()
opts = Options()
opts.add_argument("user-agent="+ua.random)

#----------------Lists----------------
myList = []
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
goodDealTableSkin = []
goodDealTablePrice = []
badDealTableSkin = []
badDealTablePrice = []
checkList = [0, 0]
#--------------------------------------

#---------Counts-----------
count = 0
count2 = 0
goneCount = 0
trackingCount = 0
notInStoreCount = 0
#--------------------------

def reset():
    myList.clear()
    store_name.clear()
    discount_price.clear()
    new_list.clear()
    newer_list.clear()
    xpath_list.clear()
    temp_list_integer.clear()
    temp_list_string.clear()
    bundle_list.clear()
    evans_list.clear()
    second_list.clear()
    statement.clear()

def deposit():
    # os.system('say "Depositing Skin"')
    webbrowser.open_new('https://www.wtfskins.com/deposit/steam/p2p')
    time.sleep(4)  #Wait for browser to load
    pyautogui.click(x=900, y=500, clicks=1, button='left')  # Click on skin
    time.sleep(0.2)
    pyautogui.click(x=1300, y=350, clicks=1, button='left')  # Click on discount box
    time.sleep(1)
    pyautogui.click(x=1300, y=586, clicks=1, button='left')  # Choose 10% Discount
    time.sleep(0.2)
    pyautogui.click(x=1417, y=357, clicks=1, button='left')  # Click 'Deposit'

def filterList(numbers, names):
    if not numbers or not names:
        print(Fore.YELLOW,"                                                                          No Store History" + Style.RESET_ALL,)
        return [], [], [], []
    zipped_data = list(zip(numbers, names))
    sorted_data_smallest = sorted(zipped_data, key=lambda x: x[0])
    sorted_data_largest = sorted(zipped_data, key=lambda x: x[0], reverse=True)
    smallest_3_data = sorted_data_smallest[:3]
    largest_3_data = sorted_data_largest[:3]
    smallest_numbers, smallest_names = zip(*smallest_3_data)
    largest_numbers, largest_names = zip(*largest_3_data)
    print('[Skin History Summary]')
    badDealTable.field_names = ['Num', Fore.RED + "Bad Skins" + Style.RESET_ALL,Fore.RED + "Multiplier" + Style.RESET_ALL,"Number", Fore.GREEN + "Good Skins" + Style.RESET_ALL,Fore.GREEN + "Multiplier" + Style.RESET_ALL]
    if len(numbers) == 1:
        badDealTable.add_row(["1.", smallest_names[0], smallest_numbers[0] + 'x',"1.", largest_names[0], largest_numbers[0] + 'x'])
    if len(numbers) == 2:
        badDealTable.add_row(["1.", smallest_names[0], smallest_numbers[0] + 'x',"1.", largest_names[0], largest_numbers[0] + 'x'])
        badDealTable.add_row(["2.", smallest_names[1], smallest_numbers[1] + 'x',"2.", largest_names[1], largest_numbers[1] + 'x'])
    if len(numbers) >= 3:
        badDealTable.add_row(["1.", smallest_names[0], smallest_numbers[0] + 'x',"1.", largest_names[0], largest_numbers[0] + 'x'])
        badDealTable.add_row(["2.", smallest_names[1], smallest_numbers[1] + 'x',"2.", largest_names[1], largest_numbers[1] + 'x'])
        badDealTable.add_row(["3.", smallest_names[2], smallest_numbers[2] + 'x',"3.", largest_names[2], largest_numbers[2] + 'x'])
    print(badDealTable)
    badDealTable.clear()

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
    try:
        new_link = shortener.tinyurl.short(a)
    except requests.exceptions.Timeout:
        print("Timeout occurred")
        new_link = 'Unknown'

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
        driver.refresh()
        driver.implicitly_wait(0.1)
        try:
            button = driver.find_element(By.XPATH, xpath_list[i])
            button.click()
        except NoSuchElementException:
            print(Style.RESET_ALL)

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
    item = sm.get_csgo_item(name, currency='USD')
    if item is None:
        print("                                                         Skin Library is down, Try again later :(")
        for g in range(5):
            print(5-g)
            time.sleep(1)
        loop()
    item_price = item.values()
    for key in item.keys():
        if item[key] == False and mac == 1:
            print("Item Not Found")
            return
        myList.append(item[key])
    USDPrice = myList[1][1:]
    USDPrice = USDPrice.replace(",", "")
    NZDPrice = Decimal(USDPrice) * Decimal(exchangeRate)
    prices.append(NZDPrice) #To Calculate total
    myList.clear()

def printsStatement():
    for e in range(len(store_name)):
        findLink(store_name[e])
        if store_name[e] != 'Bundle                              ':  #Calculating how good a deal this is (multiplier)
            multiplier = float(prices[e])/float(newer_list[e])
            multiplier = str(round(multiplier, 2))
        if store_name[e] == 'Bundle                              ':
            statement.append(Fore.YELLOW + 'Bundle')
        elif (float(newer_list[e]) * goodMultiplier) > prices[e]:
            statement.append(Fore.RED + 'BAD DEAL - ' + multiplier + 'x')
        else:
            statement.append(Fore.GREEN +'GOOD DEAL - ' + multiplier + 'x')
            global goodDeal
            if mac == 1 and goodDeal == False:
                os.system('say "Good Deal Spotted"')
                goodDeal = True
        print(Style.RESET_ALL)
        if prices[e] == 0.0000 or prices[e] == '      No Suggested Price                ':
            prices[e] = '      No Suggested Price                '
            print((str(store_name[e]) + '\t' + 'Site Price: $' + newer_list[e]).expandtabs(27),prices[e], statement[e])
        else:
            print((str(store_name[e]) + '\t' + 'Site Price: $' + newer_list[e]).expandtabs(54), '     Suggested Steam Price: $', "{:.2f}".format(prices[e]), '    ', statement[e], '       ' ,new_link)
        if store_name[e] not in goodDealTableSkin and store_name[e] != 'Bundle':
            goodDealTableSkin.append(store_name[e])
            goodDealTablePrice.append(multiplier)
            badDealTableSkin.append(store_name[e])
            badDealTablePrice.append(multiplier)


    global trackItem
    if trackItem == True:
        global myItemBool
        global goneCount
        global trackingCount
        global itemHasBeenInStore
        global notInStoreCount
        print(Style.RESET_ALL)
        if myItem not in store_name and autoDeposit == True:   #Deposit Skin After 5 Refreshes of not being there
            notInStoreCount = notInStoreCount + 1
            if notInStoreCount <= 1:
                print('                                                                    depositing item in', 1-notInStoreCount, 'refresh(s)')
            if notInStoreCount == 1 and myItemBool == False:
                deposit()
        if myItem not in store_name and myItemBool == False and count != 0 and itemHasBeenInStore == True:
            goneCount = goneCount + 1
            trackingCount = 0
            itemInStore = False
            print('Item in store = ', itemInStore)
            if goneCount == 5 and itemInStore == False:  #Give four extra refresh to account for incorrect reading
                os.system('say "Hooray, item sold!')
                myItemBool = True
        if myItem in store_name:
            itemHasBeenInStore = True
            myItemBool = False
            trackingCount = trackingCount + 1
            goneCount = 0
            notInStoreCount = 0

    if 'GOOD DEAL' not in str(statement):
        goodDeal = False

    print(Style.RESET_ALL)
    print('\n')
    newer_list.clear()
    reset()

def main():
    print(Style.RESET_ALL)
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
        newer_list.append(newResult.replace(",", ""))
    for g in range(len(newer_list)):
        size_list.append(newer_list[g])

    print(
        '+-----------------------------------------------------------------+----------------------------------+-----------------------------------------------------------------+')
    print('|               Time Elapsed: ',round(time.time() - start, 2) ,'s / ' ,round((time.time() - start)/60, 2), 'min               |   Refreshing, Refresh #', count,
          '     |   Items in store =', len(size_list), '                                           |')
    print(
        '+-----------------------------------------------------------------+----------------------------------+-----------------------------------------------------------------+')
    if count % 50 == 0 and count != 0 and count != 1:  # Every 100 check to ensure steam market is working
        steamMarketWorking()
    if count % 100 == 0 and count != 0 and count != 1:
        filterList(badDealTablePrice, badDealTableSkin)

    newerer_list = newer_list
    res = [eval(i) for i in newerer_list]
    Sum = sum(res)
    checkList.append(Sum)
    if len(checkList) > 2:
        checkList.pop(0)

    if len(store_name) > 0 or len(newer_list) > 0:
        global itemSound
        if itemSound == True and mac == 1:
            itemSound = False
    else:
        print('                                                             --> Store empty, Refreshing Momentarily <--')
        itemSound = True

    if checkList[0] != checkList[1]:
        prices.clear()
        if count != 0:
            print('                                                                 ----- Different Skins, Rechecking -----')
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
    else:   #If store doesn't change
        bundleFinder()
        for e in range(len(item_discount_price)):
            if len(store_name) != len(newer_list):
                for i in range(len(bundleCount)):
                    if bundleCount[i] == 'Bundle':
                        store_name.insert(i, bundleCount[i] + '                              ')
        printsStatement()

    if len(item_discount_price) != 0:
        global empty
        empty = False
        return empty
    else:
        empty = True
        return empty

print('                                              ******************* Code Starting - Code By Evan Holfich *******************')
start = time.time()
steamMarketWorking()
driver.get("https://www.wtfskins.com/withdraw")
time.sleep(0.5)
main()
print(Style.RESET_ALL)
openBoxes()

def loop():
    for window in Windows:
        driver.switch_to.window(window)
        driver.refresh()
        time.sleep(0.5)
        main()
        print(Style.RESET_ALL)
        openBoxes()

while True:
    count = count + 1
    Windows = driver.window_handles
    size_list.clear()
    loop()
