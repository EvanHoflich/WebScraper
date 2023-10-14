import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
import re
from num2words import num2words
import shutil
import numpy as np
badDealTable = PrettyTable()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyttsx3
engine = pyttsx3.init()

#------------------------Settings to change-----------------------
goodMultiplier = 2.6
balance = 103.57   #Maxmimum item price the auto buyer will purchase
exchangeRate = 1.6986729
summaryFrequency = 5  #Once every 5 refreshes
autoBuyBool = True  #Turn this setting on so the bot will automatically purchase good deals
autoDepositBool = False  #Turn on if you want sy
# stem to auto deposit item - this takes control of mouse
findLinkBool = True
#Turn on if finding link is having issues
myItem = ['AWP | Chromatic Aberration (Minimal Wear)']
itemsIDontWant = ['MP9 | Goo (Field-Tested)', 'M4A1-S | Flashback (Field-Tested)']
slot = 3
audio = True
audio2 = False
waitTime = 2
returnToWhere = 'pycharm'
#-----------------------------------------------------------------

#-----------Variables-----------
Sum = 0
store_not_empty = 0
mac = 0             #What operating system I am using
empty = True
bundles = False
bundleMismatch = False
itemSound = False
myItemBool = False
goodDeal = False
itemHasBeenInStore = False
itemInStore = False
cheapBundle = False
if autoDepositBool == True:
    trackItem = True  # Turn on if I want to track  pycharm
else:
    trackItem = False  # Turn on if I want to track item
position = 320 + (140*slot)
#--------------------------------

ua = UserAgent()
service = Service()
options = Options()

if mac == 1:
    #------------Dont Open A Browser (Mac)----------------
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    options.add_experimental_option("detach", True)
    options.add_argument("user-agent="+ua.random)
else:
    #----------Dont Open A Browser (Windows)--------------
    options.add_argument("--headless") # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized') #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")

driver = webdriver.Chrome(service=service, options=options)

# driver = webdriver.Chrome(service=Service(ChromeDriverManager(version='114.0.5735.90').install()), options=options)
# driver = webdriver.Chrome(service=Service('/Users/evanhoflich/PycharmProjects/pythonProject4/chromedriver'), options=options)
# driver.set_window_position(970,0)

#----------------Lists----------------
myList = []
prices = []
skinList = []
discount_price = []
new_list = []
priceList = []
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
DealTableSkinLog = []
DealTablePriceLog = []
checkList = [0, 0]
checkListData = []
#--------------------------------------

#---------Counts-----------
count = 0
count2 = 0
goneCount = 0
trackingCount = 0
notInStoreCount = 0
goodDealIndex = 0
goodDealCount = 0
#--------------------------

def loggedData():
    global DealTableSkinLog
    global DealTablePriceLog
    global checkListData

    with open("data.txt", "r") as input_file, open("temp.txt", "w") as output_file:
        for line in input_file:
            modified_line = re.sub(r'#\d+\s*', '', line).strip()
            output_file.write(modified_line + "\n")
    shutil.move("temp.txt", "data.txt")

    with open("data.txt", "r") as input_file, open("temp.txt", "w") as output_file:
        lines = input_file.readlines()
        if lines:
            output_file.write(lines[0])  # Keep the first line as is
        if len(lines) == 0 and count < 2:
            print('Loaded empty txt file')
            with open("temp.txt", "w") as file:
                file.write('                 -----Descending Order For Skin Values-----\n')
                file.write('sample data@2\n')
                file.write('sample data@3\n')
        if len(lines) > 0:
            print('                                                              <- Successfully loaded', len(lines)-1, 'line(s) of data ->')

        checkListData = [len(lines)-1, len(lines)-1]

        for line in lines[1:]:
            if line.strip():  # Check if the line is not empty
                modified_line = line[:-1]  # Remove the last character
                output_file.write(modified_line + "\n")
            else:
                output_file.write("\n")  # If the line is empty, write a newline character

    shutil.move("temp.txt", "data.txt")

    DealTableSkinLog.clear()
    DealTablePriceLog.clear()

    with open('data.txt', 'r') as file:
        for line in file:
            parts = line.strip().split('@')

            if len(parts) >= 2:
                skin = parts[0].strip()
                price_str = parts[1].strip()
                DealTableSkinLog.append(skin)
                DealTablePriceLog.append(float(price_str))


def returnToPyCharm():
    pyautogui.keyDown('command')
    pyautogui.keyDown('space')
    pyautogui.keyUp('command')
    pyautogui.keyUp('space')
    pyautogui.write(returnToWhere)
    pyautogui.press('enter')

def reset():
    myList.clear()
    skinList.clear()
    discount_price.clear()
    new_list.clear()
    priceList.clear()
    xpath_list.clear()
    temp_list_integer.clear()
    temp_list_string.clear()
    bundle_list.clear()
    evans_list.clear()
    second_list.clear()
    statement.clear()

def autoDeposit(depositItem):
    if audio == True:
        # os.system(f'say "Depositing {depositItem}"')
        os.system('say "Depositing"')
    webbrowser.open_new('https://www.wtfskins.com/deposit/steam/p2p')
    time.sleep(5.5)  #Wait for browser to load
    pyautogui.click(x=position, y=530, clicks=1, button='left')  # Click on skin
    time.sleep(0.2)
    pyautogui.click(x=1300, y=350, clicks=1, button='left')  # Click on discount box
    time.sleep(1)
    pyautogui.click(x=1300, y=585, clicks=1, button='left')  # Choose 10% Discount  y=585 for bottom,y=385 for top
    time.sleep(0.2)
    pyautogui.click(x=1417, y=357, clicks=1, button='left')  # Click 'Deposit'
    returnToPyCharm()

def saveData(DealTableSkinLogD, DealTablePriceLogD):
    file_to_delete = open("data.txt", 'w')
    float_list = [float(x) if isinstance(x, (int, float, str)) else x for x in DealTablePriceLogD]
    zipped_data_log = list(zip(DealTableSkinLogD, float_list))
    sorted_data_smallest_log = sorted(zipped_data_log, key=lambda x: x[1])
    sorted_data_largest_log = sorted(zipped_data_log, key=lambda x: x[1], reverse=True)
    smallest_4_data_log = sorted_data_smallest_log[:]
    largest_4_data_log = sorted_data_largest_log[:]
    smallest_names_log, smallest_numbers_log = zip(*smallest_4_data_log)
    largest_names_log, largest_numbers_log = zip(*largest_4_data_log)
    #Clean the data to remove doubleups
    unique_data = {}
    for name, price in zip(smallest_names_log, smallest_numbers_log):
        if name not in unique_data:
            unique_data[name] = price
    unique_names_log = list(unique_data.keys())
    unique_numbers_log = list(unique_data.values())


    checkListData.append(len(unique_names_log))
    if len(checkListData) > 2:
        checkListData.pop(0)
    if checkListData[0] != checkListData[1] and checkListData[0] != 0:
        print(Fore.GREEN + '                                                                   Added',
              num2words(checkListData[1] - checkListData[0]), 'new item(s) to data.txt!')

    #Write the new data to data.txt file
    combined_data = [f"#{i+1} {skin}   @{price}" for i, (skin, price) in enumerate(zip(unique_names_log, unique_numbers_log))]
    with open("data.txt", "w") as file:
        file.write('                 -----Descending Order For Skin Values-----\n')
        file.write('\n'.join(combined_data))

def autoBuyWindows(autoBuyIndexW):
    if autoBuyIndexW == 0:
        webbrowser.open_new('https://www.wtfskins.com/withdraw')
        html_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "html")))  # Wait for the page to load
        time.sleep(1)
        pyautogui.moveTo(-1498, 715, 0.1)
        time.sleep(0.25)
        pyautogui.click(button='left')
        time.sleep(0.25)
        pyautogui.moveTo(-1505, 715, 0.1)
        time.sleep(0.25)
        pyautogui.click(button='left')
        time.sleep(0.8)
        pyautogui.click(button='left')
        time.sleep(0.4)
        pyautogui.click(button='left')
        time.sleep(5)
        if audio == True:
            engine.say("Purchasing item in first slot")
            engine.runAndWait()
    if autoBuyIndexW == 1:
        webbrowser.open_new('https://www.wtfskins.com/withdraw')
        html_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "html")))  # Wait for the page to load
        time.sleep(1)
        pyautogui.moveTo(-1328, 715, 0.1)
        time.sleep(0.25)
        pyautogui.click(button='left')
        time.sleep(0.25)
        pyautogui.moveTo(-1335, 715, 0.1)
        time.sleep(0.25)
        pyautogui.click(button='left')
        time.sleep(0.8)
        pyautogui.click(button='left')
        time.sleep(0.4)
        pyautogui.click(button='left')
        time.sleep(5)
        if audio == True:
            engine.say("Purchasing item in second slot")
            engine.runAndWait()
    if autoBuyIndexW == 1:
        webbrowser.open_new('https://www.wtfskins.com/withdraw')
        html_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "html")))  # Wait for the page to load
        time.sleep(1)
        pyautogui.moveTo(-1158, 715, 0.1)
        time.sleep(0.25)
        pyautogui.click(button='left')
        time.sleep(0.25)
        pyautogui.moveTo(-1165, 715, 0.1)
        time.sleep(0.25)
        pyautogui.click(button='left')
        time.sleep(0.8)
        pyautogui.click(button='left')
        time.sleep(0.4)
        pyautogui.click(button='left')
        time.sleep(5)
        if audio == True:
            engine.say("Purchasing item in third slot")
            engine.runAndWait()
    if autoBuyIndexW == 1:
        webbrowser.open_new('https://www.wtfskins.com/withdraw')
        html_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "html")))  # Wait for the page to load
        time.sleep(1)
        pyautogui.moveTo(-988, 715, 0.1)
        time.sleep(0.25)
        pyautogui.click(button='left')
        time.sleep(0.25)
        pyautogui.moveTo(-995, 715, 0.1)
        time.sleep(0.25)
        pyautogui.click(button='left')
        time.sleep(0.8)
        pyautogui.click(button='left')
        time.sleep(0.4)
        pyautogui.click(button='left')
        time.sleep(5)
        if audio == True:
            engine.say("Purchasing item in fourth slot")
            engine.runAndWait()
    if autoBuyIndexW == 1:
        webbrowser.open_new('https://www.wtfskins.com/withdraw')
        html_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "html")))  # Wait for the page to load
        time.sleep(1)
        pyautogui.moveTo(-818, 715, 0.1)
        time.sleep(0.25)
        pyautogui.click(button='left')
        time.sleep(0.25)
        pyautogui.moveTo(-825, 715, 0.1)
        time.sleep(0.25)
        pyautogui.click(button='left')
        time.sleep(0.8)
        pyautogui.click(button='left')
        time.sleep(0.4)
        pyautogui.click(button='left')
        time.sleep(5)
        if audio == True:
            engine.say("Purchasing item in fifth slot")
            engine.runAndWait()
    if autoBuyIndexW == 1:
        webbrowser.open_new('https://www.wtfskins.com/withdraw')
        html_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "html")))  # Wait for the page to load
        time.sleep(1)
        pyautogui.moveTo(-648, 715, 0.1)
        time.sleep(0.25)
        pyautogui.click(button='left')
        time.sleep(0.25)
        pyautogui.moveTo(-655, 715, 0.1)
        time.sleep(0.25)
        pyautogui.click(button='left')
        time.sleep(0.8)
        pyautogui.click(button='left')
        time.sleep(0.4)
        pyautogui.click(button='left')
        time.sleep(5)
        if audio == True:
            engine.say("Purchasing item in fifth slot")
            engine.runAndWait()
    if autoBuyIndexW == 1:
        webbrowser.open_new('https://www.wtfskins.com/withdraw')
        html_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "html")))  # Wait for the page to load
        time.sleep(1)
        pyautogui.moveTo(-478, 715, 0.1)
        time.sleep(0.25)
        pyautogui.click(button='left')
        time.sleep(0.25)
        pyautogui.moveTo(-485, 715, 0.1)
        time.sleep(0.25)
        pyautogui.click(button='left')
        time.sleep(0.8)
        pyautogui.click(button='left')
        time.sleep(0.4)
        pyautogui.click(button='left')
        time.sleep(5)
        if audio == True:
            engine.say("Purchasing item in sixth slot")
            engine.runAndWait()


def autoBuy(autoBuyIndex):
    if autoBuyIndex == 0:
        webbrowser.open_new('https://www.wtfskins.com/withdraw')
        html_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "html")))  #Wait for the page to load
        time.sleep(0.4)
        pyautogui.moveTo(430, 760, 0.1)
        time.sleep(0.25)
        pyautogui.click(button='left')
        time.sleep(0.25)
        pyautogui.moveTo(410,760, 0.1)
        time.sleep(0.25)
        pyautogui.click(button='left')
        time.sleep(0.8)
        pyautogui.click(button='left')
        time.sleep(0.4)
        pyautogui.click(button='left')
        time.sleep(5)
        if audio == True:
            os.system('say "Purchasing item in first slot"')
        # returnToPyCharm()
    if autoBuyIndex == 1:
        webbrowser.open_new('https://www.wtfskins.com/withdraw')
        html_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "html")))
        time.sleep(0.4)
        pyautogui.moveTo(600, 760, 0.1)  #Move to buy button
        time.sleep(0.45)
        pyautogui.click(button='left')   #Click Buy button
        time.sleep(0.25)
        pyautogui.moveTo(580, 760, 0.1)  #Move to confirm button
        time.sleep(0.45)
        pyautogui.click(button='left')   #Click confirm button
        time.sleep(0.8)
        pyautogui.click(button='left')
        time.sleep(0.4)
        pyautogui.click(button='left')
        time.sleep(5)
        if audio == True:
            os.system('say "Purchasing item in second slot"')
        # returnToPyCharm()
    if autoBuyIndex == 2:
        #os.system('say "Purchasing item in third slot"')
        webbrowser.open_new('https://www.wtfskins.com/withdraw')
        html_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "html")))
        time.sleep(0.4)
        pyautogui.moveTo(770, 760, 0.1)
        time.sleep(0.45)
        pyautogui.click(button='left')
        time.sleep(0.25)
        pyautogui.moveTo(750, 760, 0.1)
        time.sleep(0.45)
        pyautogui.click(button='left')
        time.sleep(0.8)
        pyautogui.click(button='left')
        time.sleep(0.4)
        pyautogui.click(button='left')
        # time.sleep(5)
        # returnToPyCharm()
    if autoBuyIndex == 3:
        webbrowser.open_new('https://www.wtfskins.com/withdraw')
        html_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "html")))
        time.sleep(0.4)
        pyautogui.moveTo(940, 760, 0.1)
        time.sleep(0.25)
        pyautogui.click(button='left')
        time.sleep(0.25)
        pyautogui.moveTo(920, 760, 0.1)
        time.sleep(0.45)
        pyautogui.click(button='left')
        time.sleep(0.8)
        pyautogui.click(button='left')
        time.sleep(0.4)
        pyautogui.click(button='left')
        if audio == True:
            os.system('say "Purchasing item in Fourth slot"')
        # time.sleep(5)
        # returnToPyCharm()
    if autoBuyIndex == 4:
        webbrowser.open_new('https://www.wtfskins.com/withdraw')
        html_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "html")))
        time.sleep(0.4)
        pyautogui.moveTo(1100, 760, 0.1)
        time.sleep(0.45)
        pyautogui.click(button='left')
        time.sleep(0.25)
        pyautogui.moveTo(1080, 760, 0.1)
        time.sleep(0.45)
        pyautogui.click(button='left')
        time.sleep(0.8)
        pyautogui.click(button='left')
        time.sleep(0.4)
        pyautogui.click(button='left')
        if audio == True:
            os.system('say "Purchasing item in Fifth slot"')
        # time.sleep(5)
        # returnToPyCharm()
    if autoBuyIndex == 5:
        webbrowser.open_new('https://www.wtfskins.com/withdraw')
        html_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "html")))
        time.sleep(0.4)
        pyautogui.moveTo(1270, 760, 0.1)
        time.sleep(0.45)
        pyautogui.click(button='left')
        time.sleep(0.25)
        pyautogui.moveTo(1250, 760, 0.1)
        time.sleep(0.45)
        pyautogui.click(button='left')
        time.sleep(0.8)
        pyautogui.click(button='left')
        time.sleep(0.4)
        pyautogui.click(button='left')
        if audio == True:
            os.system('say "Purchasing item in sixth slot"')
        # time.sleep(5)
        # returnToPyCharm()

def filterList(numbers, names):
    if not numbers or not names:
        print(Fore.YELLOW,"                                                                          No Store History" + Style.RESET_ALL,)
        return [], []
    zipped_data = list(zip(numbers, names))
    sorted_data_smallest = sorted(zipped_data, key=lambda x: x[0])
    sorted_data_largest = sorted(zipped_data, key=lambda x: x[0], reverse=True)
    smallest_4_data = sorted_data_smallest[:4]
    largest_4_data = sorted_data_largest[:4]
    smallest_numbers, smallest_names = zip(*smallest_4_data)
    largest_numbers, largest_names = zip(*largest_4_data)
    print('[This Code Run Skin History Summary - Evaluating',Fore.GREEN + str(len(numbers)) + Style.RESET_ALL, 'Unique Skin(s)]')
    badDealTable.field_names = ['Num', Fore.RED + "Bad Skins" + Style.RESET_ALL,Fore.RED + "Multiplier" + Style.RESET_ALL," ", "Num.", Fore.GREEN + "Good Skins" + Style.RESET_ALL,Fore.GREEN + "Multiplier" + Style.RESET_ALL]
    if len(numbers) == 1:
        badDealTable.add_row(["1. (Worst)", smallest_names[0], smallest_numbers[0] + 'x'," ","1. (Best)", largest_names[0], largest_numbers[0] + 'x'])
    if len(numbers) == 2:
        badDealTable.add_row(["1. (Worst)", smallest_names[0], smallest_numbers[0] + 'x'," ", "1. (Best)", largest_names[0], largest_numbers[0] + 'x'])
        badDealTable.add_row(["2.", smallest_names[1], smallest_numbers[1] + 'x'," ", "2.", largest_names[1], largest_numbers[1] + 'x'])
    if len(numbers) >= 3:
        badDealTable.add_row(["1. (Worst)", smallest_names[0], smallest_numbers[0] + 'x'," ", "1. (Best)", largest_names[0], largest_numbers[0] + 'x'])
        badDealTable.add_row(["2.", smallest_names[1], smallest_numbers[1] + 'x'," ", "2.", largest_names[1], largest_numbers[1] + 'x'])
        badDealTable.add_row(["3.", smallest_names[2], smallest_numbers[2] + 'x'," ", "3.", largest_names[2], largest_numbers[2] + 'x'])
    print(badDealTable)
    badDealTable.clear()

def autoDataLog(numbers, names):
    if not numbers or not names:
        saveData(DealTableSkinLog, DealTablePriceLog)
        return [], []
    dataZipped = list(zip(numbers, names))
    smallestDataSorted = sorted(dataZipped, key=lambda x: x[0])
    largestDataSorted = sorted(dataZipped, key=lambda x: x[0], reverse=True)
    smallestFourData = smallestDataSorted[:]
    largestFourData = largestDataSorted[:]
    smallNums, smallNames = zip(*smallestFourData)
    largestNums, largestNames = zip(*largestFourData)
    arraySummedName = DealTableSkinLog + list(smallNames)
    arraySummedPrice = DealTablePriceLog + list(smallNums)
    saveData(arraySummedName, arraySummedPrice)


def steamMarketWorking():
    try:
        item = sm.get_csgo_item('AK-47 | Frontside Misty (Field-Tested)', currency='USD')
    except requests.exceptions.ConnectionError:
        print("Connection error occurred.")
    if item is None:
        print(Fore.RED + "                                                             -----Steam Market Library Currently Down-----" + Style.RESET_ALL)
        main()
    else:
        print(Fore.GREEN + "                                                               -----Steam Market Working As Expected-----")
        print(Style.RESET_ALL)

def findLink(name):
    global findLinkBool
    if findLinkBool == True:
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
            new_link = 'Unknown'
            findLinkBool = False
    else:
        new_link = 'No Link :('

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

    num_bundles = len(size_list) - len(skinList)

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
    prices.append(NZDPrice)  #To Calculate total
    myList.clear()

def printsStatement():
    for e in range(len(skinList)):
        findLink(skinList[e])
        if skinList[e] != 'Bundle                              ':  #Calculating how good a deal this is (multiplier)
            multiplier = float(prices[e])/float(priceList[e])
            checkMultiplier = multiplier
            multiplier = str(round(multiplier, 2))
        if skinList[e] == 'Bundle                              ':
            statement.append(Fore.YELLOW + 'Bundle')
        elif (float(priceList[e]) * goodMultiplier) > prices[e]:
            statement.append(Fore.RED + 'BAD DEAL - ' + multiplier + 'x')
        else:
            statement.append(Fore.GREEN +'GOOD DEAL - ' + multiplier + 'x')
            global goodDeal
            global goodDealCount
            if mac == 1 and goodDeal == False and float(priceList[e]) < float(balance):
                if checkMultiplier < 4:
                    goodDealCount = goodDealCount + 1
                    if audio == True:
                        os.system('say "Good Deal Spotted"')
                if audio == True and checkMultiplier >=4.3:
                    os.system('say "Deal spotted with high multiplier"')
                goodDeal = True
                if autoBuyBool == True and checkMultiplier < 4.3 and e not in itemsIDontWant:
                    autoBuy(e)
            #BUYING WITH WINDOWS COMPUTER
            if mac == 0 and goodDeal == False and float(priceList[e]) < float(balance):
                if checkMultiplier < 4:
                    goodDealCount = goodDealCount + 1
                    if audio == True:
                        engine.say("Good Deal Spotted")
                        engine.runAndWait()
                if audio == True and checkMultiplier >= 4.3:
                    engine.say("Deal spotted with high multiplier")
                    engine.runAndWait()
                goodDeal = True
                if autoBuyBool == True and checkMultiplier < 4.3 and e not in itemsIDontWant:
                    autoBuyWindows(e)
        print(Style.RESET_ALL)
        if prices[e] == 0.0000 or prices[e] == '      No Suggested Price                ':
            prices[e] = '      No Suggested Price                '
            print((str(skinList[e]) + '\t' + 'Site Price: $' + priceList[e]).expandtabs(27), prices[e], statement[e])
        else:
            for t in range(len(myItem)):
                if skinList[e] == myItem[t]:
                    print((Fore.GREEN + '(My item) ' + Style.RESET_ALL + str(skinList[e]) + '\t' + 'Site Price: $' + priceList[e]).expandtabs(3), '     Suggested Steam Price: $', "{:.2f}".format(prices[e]),'    ', statement[e], '       ', new_link)
                else:
                    print((str(skinList[e]) + '\t' + 'Site Price: $' + priceList[e]).expandtabs(58), '     Suggested Steam Price: $', "{:.2f}".format(prices[e]), '    ', statement[e], '       ', new_link)
        if skinList[e] not in goodDealTableSkin and 'Bundle' not in skinList[e]:
            goodDealTableSkin.append(skinList[e])
            goodDealTablePrice.append(multiplier)
            badDealTableSkin.append(skinList[e])
            badDealTablePrice.append(multiplier)

        global cheapBundle   #Notify me if there is a cheap bundle
        if skinList[e] == 'Bundle                              ' and float(priceList[e]) <= cheapBundle and cheapBundle != True:
            if audio == True:
                os.system('say "Cheap Bundle spoted"')
            cheapBundle = True
        if 'Bundle                              ' not in skinList:
            cheapBundle = False

    global trackItem
    if trackItem == True:
        global myItemBool
        global goneCount
        global trackingCount
        global itemHasBeenInStore
        global notInStoreCount
        print(Style.RESET_ALL)
        for y in range(len(myItem)):
            if myItem[y] not in skinList and autoDepositBool == True:   #Deposit Skin After 2 Refreshes of not being there
                notInStoreCount = notInStoreCount + 1
                if notInStoreCount <= 5:
                    print('                                                                    depositing item in', 5-notInStoreCount, 'refresh(s)')
                if notInStoreCount == 5 and myItemBool == False:
                    autoDeposit(myItem[y])
            if myItem[y] not in skinList and myItemBool == False and count != 0 and itemHasBeenInStore == True:
                goneCount = goneCount + 1
                trackingCount = 0
                itemInStore = False
                if goneCount == 10 and itemInStore == False:  #Give four extra refresh to account for incorrect reading
                    print("                                                                                     ")
                    print(Fore.GREEN + "                                                     WE SOLD THAT ITEM LETS GOOOOOOOOOOOOOOOOO!")
                    print("                                                     OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                    print("                                                     OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO" + Style.RESET_ALL)
                    if audio2 == True:
                        os.system('say "Hooray, Item Sold!"')
                    myItemBool = True
            if myItem[y] in skinList:
                itemHasBeenInStore = True
                myItemBool = False
                trackingCount = trackingCount + 1
                goneCount = 0
                notInStoreCount = 0

    if 'GOOD DEAL' not in str(statement):
        goodDeal = False

    print(Style.RESET_ALL)
    print('\n')
    priceList.clear()
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
        skinList.append(name.text)

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
        priceList.append(newResult.replace(",", ""))
    for g in range(len(priceList)):
        size_list.append(priceList[g])

    if goodDealCount == 0:
        placeholder = '                 No good deals yet :(' + '                     '
    if goodDealCount > 0:
        placeholder = '             {:.2f}mins/multiplier'.format((time.time() - start) / 60 / goodDealCount) + Fore.GREEN + '(' + str(goodDealCount) +')' + Style.RESET_ALL + '                         '

    print(
        '+-----------------------------------------------------------------+----------------------------------+-----------------------------------------------------------------+')
    print('|               Time Elapsed: ',round(time.time() - start, 2) ,'s / ' ,round((time.time() - start)/60, 2), 'min                 |    Refreshing, Refresh #', count, '      |     ', placeholder, '|')
    print(
        '+-----------------------------------------------------------------+----------------------------------+-----------------------------------------------------------------+')
    if count % 1000 == 0 and count != 0:  # Every 100 check to ensure steam market is working
        steamMarketWorking()
    if count % summaryFrequency == 0 and count != 0: #This runs the summary table
        filterList(badDealTablePrice, badDealTableSkin)
    if count % 1 == 0:  #This runs the auto data log
        autoDataLog(badDealTablePrice, badDealTableSkin)
    if count % 100 == 0 and count != 0 and count != 1:
        loggedData()

    newerer_list = priceList
    res = [eval(i) for i in newerer_list]
    Sum = sum(res)
    checkList.append(Sum)
    if len(checkList) > 2:
        checkList.pop(0)

    if len(skinList) > 0 or len(priceList) > 0:
        global itemSound
        if itemSound == True and mac == 1:
            itemSound = False
    else:
        print('                                                              --> Store empty, Refreshing Momentarily <--')
        itemSound = True

    if checkList[0] != checkList[1]:
        prices.clear()
        if count != 0 and checkList[1] > checkList[0]:
            print('                                                                 ----- Different Skins, Rechecking -----')
        for i in range(len(skinList)):
            skinCheck(skinList[i])
        bundleFinder()
        for e in range(len(item_discount_price)):
            if len(skinList) != len(priceList):
                for i in range(len(bundleCount)):
                    if bundleCount[i] == 'Bundle':
                        skinList.insert(i, bundleCount[i] + '                              ')
                        prices.insert(i, 0.0000)
        printsStatement()
        reset()
    else:   #If store doesn't change
        bundleFinder()
        for e in range(len(item_discount_price)):
            if len(skinList) != len(priceList):
                for i in range(len(bundleCount)):
                    if bundleCount[i] == 'Bundle':
                        skinList.insert(i, bundleCount[i] + '                              ')
        printsStatement()

    if len(item_discount_price) != 0:
        global empty
        empty = False
        return empty
    else:
        empty = True
        return empty

print('                                              ******************* Starting...... - Code By Evan Holfich *******************')
start = time.time()
steamMarketWorking()
loggedData()
try:
    driver.get("https://www.wtfskins.com/withdraw")
except requests.exceptions.ConnectionError:
    print("Connection error occurred.")
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
